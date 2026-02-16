const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const multer = require('multer');
const path = require('path');
const { PythonShell } = require('python-shell');
const morgan = require('morgan');
const fs = require('fs');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5001;

// Middleware
app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

// Configure Multer for Audio/CSV uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = path.join(__dirname, '../uploads');
    if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir, { recursive: true });
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname || 'audio.webm'}`);
  }
});
const upload = multer({ storage });

// Check for local venv
// Check for local venv, otherwise use system python
const venvPath = path.join(__dirname, '../.venv/Scripts/python.exe');
const pythonPath = fs.existsSync(venvPath) ? venvPath : (process.platform === 'win32' ? 'py' : 'python3');

// Route for Voice Transcription
app.post('/api/transcribe', upload.single('audio'), (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'No audio file uploaded' });

  const options = {
    mode: 'json',
    pythonPath: pythonPath,
    scriptPath: path.join(__dirname, '../src'),
    args: [req.file.path]
  };

  PythonShell.run('voice_bridge.py', options).then(results => {
    res.json(results[0]);
  }).catch(err => {
    console.error(err);
    res.status(500).json({ error: err.message });
  });
});

app.post('/api/insights', (req, res) => {
  const { date_range, current_taxonomy, transcripts } = req.body;

  if (!transcripts || !Array.isArray(transcripts)) {
    return res.status(400).json({ error: 'Invalid transcripts data' });
  }

  const options = {
    mode: 'json',
    pythonPath: pythonPath, // Re-use the pythonPath variable
    scriptPath: path.join(__dirname, '../src'),
  };

  const pyshell = new PythonShell('generate_insights.py', options);

  pyshell.send({
    date_range,
    current_taxonomy,
    transcripts
  });

  pyshell.on('message', function (message) {
    // received a message sent from the Python script (a simple "print" statement)
    res.json(message);
  });

  pyshell.end(function (err) {
    if (err) {
      console.error('PythonShell Error:', err);
      if (!res.headersSent) res.status(500).json({ error: err.message });
    }
  });
});

// Routes
app.get('/api/status', (req, res) => {
  res.json({ status: 'Server is running', platform: 'Node.js' });
});

// Route to run Python Tag Extractor (Turbo)
app.post('/api/analyze', upload.single('file'), (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'No file uploaded' });

  const previewOptions = {
    mode: 'json',
    pythonPath: pythonPath,
    scriptPath: path.join(__dirname, '../'),
    args: [req.file.path]
  };

  PythonShell.run('src/file_preview.py', previewOptions).then((previewResults) => {
    const preview = Array.isArray(previewResults) && previewResults.length > 0 ? previewResults[0] : {};
    const taxonomyOptions = {
      mode: 'json',
      pythonPath: pythonPath,
      scriptPath: path.join(__dirname, '../'),
      args: [req.file.path]
    };

    PythonShell.run('src/file_taxonomy.py', taxonomyOptions).then((taxonomyResults) => {
      const taxonomyPayload = Array.isArray(taxonomyResults) && taxonomyResults.length > 0 ? taxonomyResults[0] : {};
      const taxonomyRows = Array.isArray(taxonomyPayload?.taxonomy_rows) ? taxonomyPayload.taxonomy_rows : [];

      const options = {
        mode: 'text',
        pythonPath: pythonPath,
        scriptPath: path.join(__dirname, '../'),
        args: ['--input', req.file.path]
      };

      // Run legacy pipeline too; keep app usable even if this heavy pass fails.
      PythonShell.run('main.py', options).then((results) => {
        res.json({ success: true, preview, taxonomy_rows: taxonomyRows, results });
      }).catch((pipelineErr) => {
        console.error(pipelineErr);
        res.json({
          success: true,
          preview,
          taxonomy_rows: taxonomyRows,
          results: [],
          warning: pipelineErr?.message || 'Le pipeline complet a echoue, mais la visualisation est disponible.'
        });
      });
    }).catch((taxonomyErr) => {
      console.error(taxonomyErr);
      res.status(500).json({
        error: 'Extraction taxonomique impossible pour ce fichier.',
        details: taxonomyErr?.message || 'Erreur inconnue'
      });
    });
  }).catch(err => {
    console.error(err);
    res.status(500).json({
      error: 'Analyse impossible pour ce fichier.',
      details: err?.message || 'Erreur inconnue'
    });
  });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
