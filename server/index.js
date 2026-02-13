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
    if (!fs.existsSync(uploadDir)) fs.mkdirSync(uploadDir);
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname || 'audio.webm'}`);
  }
});
const upload = multer({ storage });

// Route for Voice Transcription
app.post('/api/transcribe', upload.single('audio'), (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'No audio file uploaded' });

  const options = {
    mode: 'json',
    pythonPath: 'python3',
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

// Routes
app.get('/api/status', (req, res) => {
  res.json({ status: 'Server is running', platform: 'Node.js' });
});

// Route to run Python Tag Extractor (Turbo)
app.post('/api/analyze', upload.single('file'), (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'No file uploaded' });

  const options = {
    mode: 'text',
    pythonPath: 'python3', // Use the system python3
    scriptPath: path.join(__dirname, '../'),
    args: [req.file.path]
  };

  // We will create a bridge script to call your existing tag_extractor.py
  PythonShell.run('main.py', options).then(results => {
    res.json({ success: true, results });
  }).catch(err => {
    console.error(err);
    res.status(500).json({ error: err.message });
  });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
