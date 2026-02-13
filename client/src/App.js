import React, { useRef, useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Upload,
  Layout,
  Palette,
  BrainCircuit,
  Mic,
  History,
  Database,
  LogOut,
  Settings,
  Loader2,
  Search,
  Calendar,
  CheckCircle2,
  AlertCircle,
  Clock3,
  Eye,
  EyeOff
} from 'lucide-react';

const styles = {
  loginWrapper: {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100vw',
    height: '100vh',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000
  },
  fullBg: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundImage: 'url("/assets/images/background.png")',
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    filter: 'blur(1.5px)',
    zIndex: -1
  },
  loginContainer: {
    width: '400px',
    backgroundColor: 'rgba(255, 255, 255, 0.75)',
    backdropFilter: 'blur(20px)',
    borderRadius: '24px',
    padding: '30px 40px',
    boxShadow: '0 20px 40px rgba(0,0,0,0.2)',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    border: '1px solid rgba(255,255,255,0.4)'
  },
  circle: {
    width: '100px',
    height: '100px',
    borderRadius: '50%',
    overflow: 'hidden',
    border: '2px solid #000',
    backgroundColor: '#fff',
    marginBottom: '6px'
  },
  logoImg: {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
    objectPosition: '48% 50%'
  },
  card: {
    backgroundColor: 'rgba(255,255,255,0.95)',
    borderRadius: '18px',
    padding: '22px',
    border: '1px solid rgba(0,0,0,0.04)',
    boxShadow: '0 12px 28px rgba(0,0,0,0.05)'
  },
  label: {
    display: 'block',
    marginBottom: '8px',
    fontWeight: 700,
    color: '#444',
    textTransform: 'uppercase',
    letterSpacing: '0.4px',
    fontSize: '13px'
  },
  input: {
    width: '100%',
    padding: '14px 16px',
    fontSize: '16px',
    borderRadius: '12px',
    border: '1px solid #d1d5db',
    outline: 'none',
    boxSizing: 'border-box'
  }
};

function App() {
  const [auth, setAuth] = useState({ isAuthenticated: false, user: null });
  const [activeTab, setActiveTab] = useState('data');
  const [loginForm, setLoginForm] = useState({ username: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [showHelp, setShowHelp] = useState(false);
  const [sidebarHovered, setSidebarHovered] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleLogin = (e) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      if (
        (loginForm.username === 'analyste' && loginForm.password === 'analyste123') ||
        (loginForm.username === 'vendeur' && loginForm.password === 'vendeur123')
      ) {
        setAuth({
          isAuthenticated: true,
          user: { name: loginForm.username.toUpperCase(), role: loginForm.username }
        });
        setActiveTab(loginForm.username === 'vendeur' ? 'voice' : 'data');
      } else {
        alert('Identifiants incorrects');
      }
      setLoading(false);
    }, 500);
  };

  if (!auth.isAuthenticated) {
    return (
      <div style={styles.loginWrapper}>
        <div style={styles.fullBg} />
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} style={styles.loginContainer}>
          <div style={styles.circle}>
            <img src="/assets/images/loewe_logo.png" alt="Logo" style={styles.logoImg} />
          </div>
          <p
            style={{
              color: '#000',
              marginTop: 0,
              marginBottom: '8px',
              textAlign: 'center',
              fontWeight: 400,
              fontSize: '32px',
              fontFamily: '"Times New Roman", Times, serif',
              letterSpacing: '2px',
              textTransform: 'uppercase'
            }}
          >
            Loewe
          </p>

          <form onSubmit={handleLogin} style={{ width: '100%', marginTop: '6px' }}>
            <div style={{ marginBottom: '14px' }}>
              <label style={{ ...styles.label, fontSize: '14px' }}>Utilisateur</label>
              <input
                type="text"
                placeholder="analyste / vendeur"
                value={loginForm.username}
                onChange={(e) => setLoginForm({ ...loginForm, username: e.target.value })}
                style={{ ...styles.input, height: '52px' }}
              />
            </div>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ ...styles.label, fontSize: '14px' }}>Mot de passe</label>
              <div style={{ position: 'relative' }}>
                <input
                  type={showPassword ? 'text' : 'password'}
                  placeholder="....."
                  value={loginForm.password}
                  onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                  autoComplete="current-password"
                  style={{
                    ...styles.input,
                    height: '52px',
                    fontSize: showPassword ? '16px' : '26px',
                    textIndent: '1px',
                    paddingRight: '48px'
                  }}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((v) => !v)}
                  style={{
                    position: 'absolute',
                    right: '16px',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    border: 'none',
                    background: 'transparent',
                    cursor: 'pointer',
                    color: '#6b7280',
                    padding: 0,
                    display: 'flex',
                    alignItems: 'center'
                  }}
                  aria-label={showPassword ? 'Masquer le mot de passe' : 'Afficher le mot de passe'}
                >
                  {showPassword ? <Eye size={18} /> : <EyeOff size={18} />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              style={{
                width: '100%',
                padding: '14px',
                borderRadius: '12px',
                border: 'none',
                backgroundColor: '#000',
                color: '#fff',
                fontWeight: 700,
                fontSize: '16px',
                cursor: 'pointer'
              }}
              disabled={loading}
            >
              {loading ? 'Connexion...' : 'Se connecter'}
            </button>

            <div
              onClick={() => setShowHelp((v) => !v)}
              style={{
                marginTop: '15px',
                textAlign: 'center',
                fontSize: '14px',
                fontWeight: 600,
                cursor: 'pointer',
                color: '#4b5563',
                display: 'flex',
                alignItems: 'center'
              }}
            >
              <div style={{ height: '2px', flex: 1, backgroundColor: '#9ca3af' }} />
              <span style={{ padding: '0 12px', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '1px' }}>Aide</span>
              <div style={{ height: '2px', flex: 1, backgroundColor: '#9ca3af' }} />
            </div>

            <AnimatePresence>
              {showHelp && (
                <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} style={{ overflow: 'hidden' }}>
                  <div
                    style={{
                      marginTop: '15px',
                      fontSize: '16px',
                      color: '#444',
                      backgroundColor: '#f9f9f9',
                      padding: '15px',
                      borderRadius: '12px',
                      border: '1px solid #eee',
                      fontWeight: 500,
                      textAlign: 'center'
                    }}
                  >
                    vendeur / vendeur123 | analyste / analyste123
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </form>
        </motion.div>
      </div>
    );
  }

  const sidebarExpanded = sidebarHovered;
  const isVendeur = auth?.user?.role === 'vendeur';

  return (
    <div style={{ display: 'flex', height: '100vh', background: '#f4f7f6', color: '#1a1a1a', fontFamily: 'Inter, system-ui, sans-serif' }}>
      <div
        onMouseEnter={() => setSidebarHovered(true)}
        onMouseLeave={() => setSidebarHovered(false)}
        style={{
          width: sidebarExpanded ? '220px' : '70px',
          backgroundColor: 'white',
          borderRight: '1px solid #e5e7eb',
          display: 'flex',
          flexDirection: 'column',
          boxShadow: '4px 0 20px rgba(0,0,0,0.02)',
          transition: 'width 0.22s ease'
        }}
      >
        <div
          style={{
            padding: sidebarExpanded ? '40px 30px' : '24px 12px',
            display: 'flex',
            justifyContent: 'center',
            transform: sidebarExpanded ? 'none' : 'translateX(-4px)'
          }}
        >
          {auth.user.role === 'vendeur' ? (
            sidebarExpanded ? (
              <h2
                style={{
                  margin: 0,
                  fontSize: '32px',
                  color: '#000',
                  fontWeight: 400,
                  fontFamily: '"Times New Roman", Times, serif',
                  letterSpacing: '2px',
                  textTransform: 'uppercase',
                  textAlign: 'center',
                  width: '100%'
                }}
              >
                Loewe
              </h2>
            ) : (
              <div style={{ width: '42px', height: '42px', borderRadius: '50%', border: '1px solid #000', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden', backgroundColor: '#fff' }}>
                <img src="/assets/images/loewe_logo.png" alt="Loewe" style={{ width: '100%', height: '100%', objectFit: 'contain', padding: '3px' }} />
              </div>
            )
          ) : (
            <h2 style={{ margin: 0, fontSize: sidebarExpanded ? '24px' : '0px', color: '#000', display: 'flex', alignItems: 'center', gap: sidebarExpanded ? '12px' : '0px' }}>
              <span style={{ backgroundColor: '#000', color: '#fff', padding: '4px 10px', borderRadius: '6px', fontWeight: 900 }}>LVMH</span>
              {sidebarExpanded && <span style={{ fontSize: '16px', fontWeight: 500, color: '#666' }}>Analytics</span>}
            </h2>
          )}
        </div>

        <nav
          style={{
            flex: 1,
            padding: sidebarExpanded ? '0 15px' : '0 8px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: sidebarExpanded ? 'stretch' : 'center',
            transform: sidebarExpanded ? 'none' : 'translateX(-4px)'
          }}
        >
          {auth.user.role === 'analyste' && (
            <>
              <SidebarItem icon={<Upload size={18} />} label="Ingestion & Tags" active={activeTab === 'data'} isExpanded={sidebarExpanded} onClick={() => setActiveTab('data')} />
              <SidebarItem icon={<Layout size={18} />} label="Vue Globale" active={activeTab === 'global'} isExpanded={sidebarExpanded} onClick={() => setActiveTab('global')} />
              <SidebarItem icon={<BrainCircuit size={18} />} label="Analyse IA" active={activeTab === 'ai'} isExpanded={sidebarExpanded} onClick={() => setActiveTab('ai')} />
              <SidebarItem icon={<Palette size={18} />} label="Studio Builder" active={activeTab === 'builder'} isExpanded={sidebarExpanded} onClick={() => setActiveTab('builder')} />
            </>
          )}

          {auth.user.role === 'vendeur' && (
            <>
              <SidebarItem icon={<Mic size={18} />} label="Enregistrement" active={activeTab === 'voice'} isExpanded={sidebarExpanded} onClick={() => setActiveTab('voice')} />
              <SidebarItem icon={<History size={18} />} label="Historique" active={activeTab === 'history'} isExpanded={sidebarExpanded} onClick={() => setActiveTab('history')} />
            </>
          )}

          <div style={{ height: '1px', backgroundColor: '#f0f0f0', margin: sidebarExpanded ? '20px 15px' : '20px 0', width: sidebarExpanded ? 'auto' : '42px', alignSelf: 'center' }} />
          <SidebarItem icon={<Database size={18} />} label="Base de données" active={activeTab === 'database'} isExpanded={sidebarExpanded} onClick={() => setActiveTab('database')} />
        </nav>

        <div style={{ padding: sidebarExpanded ? '20px' : '14px 10px', borderTop: '1px solid #f0f0f0', transform: sidebarExpanded ? 'none' : 'translateX(-4px)', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          {sidebarExpanded ? (
            <>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-start', gap: '12px', marginBottom: '14px', width: '100%' }}>
                <div style={{ width: '34px', height: '34px', borderRadius: '50%', overflow: 'hidden', border: '1px solid #000' }}>
                  <img src={auth.user.role === 'vendeur' ? '/assets/images/loewe_logo.png' : 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'} alt="Profile" style={{ width: '100%', height: '100%', objectFit: auth.user.role === 'vendeur' ? 'contain' : 'cover', backgroundColor: auth.user.role === 'vendeur' ? '#fff' : 'transparent' }} />
                </div>
                <div>
                  <div style={{ fontSize: '13px', fontWeight: 700, color: '#1a1a1a' }}>{auth.user.role === 'vendeur' ? 'VENDEUR' : auth.user.name}</div>
                  {auth.user.role !== 'vendeur' && <div style={{ fontSize: '10px', color: '#999', textTransform: 'uppercase', fontWeight: 600 }}>{auth.user.role}</div>}
                </div>
              </div>
              <button
                onClick={() => setAuth({ isAuthenticated: false, user: null })}
                style={{ width: '100%', minWidth: '100%', padding: '12px', backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '12px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px', fontSize: '13px', color: '#ef4444', fontWeight: 600 }}
              >
                <LogOut size={16} /> Déconnexion
              </button>
            </>
          ) : (
            <button style={{ width: '52px', height: '52px', borderRadius: '16px', border: '1px solid #e5e7eb', backgroundColor: '#fff', color: '#6b7280', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'default', transform: 'translateY(-6px)' }} aria-label="Paramètres" title="Paramètres">
              <Settings size={20} />
            </button>
          )}
        </div>
      </div>

      <div
        style={{
          flex: 1,
          overflowY: 'auto',
          padding: '50px',
          backgroundColor: '#f4f7f6',
          backgroundImage: 'none'
        }}
      >
        <AnimatePresence mode="wait">
          <motion.div key={activeTab} initial={{ opacity: 0, x: 10 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -10 }} transition={{ duration: 0.2 }}>
            {activeTab === 'data' && <DataTab />}
            {activeTab === 'global' && <PlaceholderTab title="Vue Globale" />}
            {activeTab === 'ai' && <PlaceholderTab title="Analyse IA" />}
            {activeTab === 'builder' && <PlaceholderTab title="Studio Builder" />}
            {activeTab === 'voice' && <VoiceTab />}
            {activeTab === 'history' && <HistoryTab />}
            {activeTab === 'database' && <DatabaseTab />}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}

function SidebarItem({ icon, label, active, isExpanded, onClick }) {
  return (
    <div
      onClick={onClick}
      style={{
        width: isExpanded ? '100%' : '52px',
        height: isExpanded ? 'auto' : '52px',
        padding: isExpanded ? '14px 18px' : '0',
        boxSizing: 'border-box',
        borderRadius: isExpanded ? '14px' : '16px',
        cursor: 'pointer',
        backgroundColor: active ? '#000' : 'transparent',
        color: active ? '#fff' : '#666',
        display: 'flex',
        alignItems: 'center',
        justifyContent: isExpanded ? 'flex-start' : 'center',
        gap: isExpanded ? '14px' : '0px',
        marginBottom: isExpanded ? '10px' : '12px',
        fontSize: '14px',
        fontWeight: active ? 600 : 500,
        whiteSpace: 'nowrap',
        transition: 'all 0.2s'
      }}
      title={!isExpanded ? label : undefined}
    >
      {icon}
      {isExpanded && label}
    </div>
  );
}

function DataTab() {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileSelect = () => {
    if (fileInputRef.current) fileInputRef.current.click();
  };

  const handleFileChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setIsUploading(true);
    setUploadStatus(null);
    const formData = new FormData();
    formData.append('file', file);
    try {
      await axios.post('http://localhost:5001/api/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setUploadStatus('success');
    } catch (err) {
      console.error(err);
      setUploadStatus('error');
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  return (
    <div>
      <h1 style={{ fontSize: '32px', margin: '0 0 8px 0' }}>Ingestion & Tags</h1>
      <p style={{ color: '#555', marginTop: 0 }}>Importez un fichier pour lancer le nettoyage et l'analyse.</p>
      <div style={{ ...styles.card, maxWidth: '760px', marginTop: '24px' }}>
        <input ref={fileInputRef} type="file" accept=".csv,.xlsx,.xls,.json,.txt" onChange={handleFileChange} style={{ display: 'none' }} />
        <button onClick={handleFileSelect} style={{ padding: '12px 16px', borderRadius: '12px', border: 'none', background: '#000', color: '#fff', fontWeight: 700, cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: '8px' }} disabled={isUploading}>
          {isUploading ? <Loader2 size={16} className="animate-spin" /> : <Upload size={16} />}
          {isUploading ? 'Traitement...' : 'Sélectionner un fichier'}
        </button>
        {uploadStatus === 'success' && <p style={{ color: '#15803d', marginTop: '14px' }}>Import terminé.</p>}
        {uploadStatus === 'error' && <p style={{ color: '#b91c1c', marginTop: '14px' }}>Erreur pendant l'import.</p>}
      </div>
    </div>
  );
}

function VoiceTab() {
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [transcription, setTranscription] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      const chunks = [];
      recorder.ondataavailable = (e) => chunks.push(e.data);
      recorder.onstop = async () => {
        const audioBlob = new Blob(chunks, { type: 'audio/webm' });
        await sendAudioToBackend(audioBlob);
      };
      recorder.start();
      setMediaRecorder(recorder);
      setIsRecording(true);
    } catch (err) {
      console.error(err);
      alert("Impossible d'accéder au micro.");
    }
  };

  const stopRecording = () => {
    if (!mediaRecorder) return;
    mediaRecorder.stop();
    setIsRecording(false);
    mediaRecorder.stream.getTracks().forEach((track) => track.stop());
  };

  const sendAudioToBackend = async (blob) => {
    setIsProcessing(true);
    const audioFile = new File([blob], 'recording.webm', { type: 'audio/webm' });
    const data = new FormData();
    data.append('audio', audioFile);
    try {
      const response = await axios.post('http://localhost:5001/api/transcribe', data);
      setTranscription(response.data);
    } catch (err) {
      console.error(err);
      alert('Erreur lors de la transcription.');
    } finally {
      setIsProcessing(false);
    }
  };

  const tagLabels = {
    genre: 'Genre',
    langue: 'Langue',
    statut_client: 'Statut client',
    age: 'Age',
    profession: 'Profession',
    ville: 'Ville',
    pays: 'Pays',
    famille: 'Famille',
    sport: 'Sport',
    musique: 'Musique',
    animaux: 'Animaux',
    voyage: 'Voyage',
    art_culture: 'Art et culture',
    gastronomie: 'Gastronomie',
    pieces_favorites: 'Pièces favorites',
    pieces_recherchees: 'Pièces recherchées',
    couleurs: 'Couleurs',
    matieres: 'Matières',
    sensibilite_mode: 'Sensibilité mode',
    tailles: 'Tailles',
    style: 'Style',
    budget: 'Budget',
    urgence_score: 'Urgence',
    motif_achat: "Motif d'achat",
    marques_preferees: 'Marques préférées',
    frequence_achat: "Fréquence d'achat",
    regime: 'Régime',
    allergies: 'Allergies',
    valeurs: 'Valeurs',
    actions_crm: 'Actions CRM',
    echeances: 'Échéances',
    canaux_contact: 'Canaux contact'
  };

  const taxonomySections = [
    { title: 'Identité', keys: ['genre', 'langue', 'statut_client'] },
    { title: 'Démographique', keys: ['age', 'profession', 'ville', 'pays', 'famille'] },
    { title: 'Lifestyle', keys: ['sport', 'musique', 'animaux', 'voyage', 'art_culture', 'gastronomie'] },
    { title: 'Style', keys: ['pieces_favorites', 'pieces_recherchees', 'couleurs', 'matieres', 'sensibilite_mode', 'tailles', 'style'] },
    { title: 'Achat', keys: ['budget', 'urgence_score', 'motif_achat', 'marques_preferees', 'frequence_achat'] },
    { title: 'Préférences', keys: ['regime', 'allergies', 'valeurs'] },
    { title: 'CRM', keys: ['actions_crm', 'echeances', 'canaux_contact'] }
  ];

  const getExtractedTagGroups = () => {
    const tags = transcription?.tags_extracted || {};
    const groups = [];
    const hiddenKeys = new Set(['cleaned_text', 'centres_interet', 'timing']);
    taxonomySections.forEach((section) => {
      const sectionItems = [];
      section.keys.forEach((key) => {
        const label = tagLabels[key] || key;
        if (hiddenKeys.has(key)) return;

        let value = tags[key];
        // Fallback d'affichage pour ne jamais "manger" l'âge
        if ((value === null || value === undefined || value === '') && key === 'age') {
          const textForAge =
            (typeof transcription?.cleaned_text === 'string' && transcription.cleaned_text) ||
            (typeof transcription?.transcription === 'string' && transcription.transcription) ||
            (typeof tags.cleaned_text === 'string' && tags.cleaned_text) ||
            '';

          const agePatterns = [
            /\b(\d{1,2})\s*ans?\b/i,
            /\bj[' ]?ai\s*(\d{1,2})\b/i,
            /\bage\s*[:=]?\s*(\d{1,2})\b/i
          ];

          for (const pattern of agePatterns) {
            const ageMatch = textForAge.match(pattern);
            if (ageMatch) {
              value = ageMatch[1];
              break;
            }
          }
        }

        if (Array.isArray(value)) {
          if (value.length > 0) {
            sectionItems.push(`${label}: ${value.join(', ')}`);
          }
          return;
        }

        if (typeof value === 'string') {
          if (value.trim() !== '') {
            sectionItems.push(`${label}: ${value.trim()}`);
          }
          return;
        }

        if (value !== null && value !== undefined) {
          sectionItems.push(`${label}: ${String(value)}`);
        }
      });
      if (sectionItems.length > 0) {
        groups.push({ title: section.title, items: sectionItems });
      }
    });
    return groups;
  };

  return (
    <div>
      <div style={{ marginBottom: '40px' }}>
        <h1 style={{ fontSize: '32px', fontWeight: 800, margin: '0 0 8px 0', letterSpacing: '-1px' }}>Enregistrement Client</h1>
        <p style={{ color: '#666', fontSize: '16px' }}>Capturez les interactions clients et laissez l'IA extraire les données.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: '30px' }}>
        <div style={{ ...styles.card, display: 'flex' }}>
          <div style={{ padding: '30px', backgroundColor: '#f8f9fa', borderRadius: '15px', textAlign: 'center', border: '2px solid #eee', width: '100%', minHeight: '240px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
            <motion.div
              animate={isRecording ? { scale: [1, 1.15, 1] } : {}}
              transition={{ repeat: Infinity, duration: 1.5 }}
              style={{
                width: '80px',
                height: '80px',
                borderRadius: '50%',
                backgroundColor: isRecording ? '#ef4444' : '#000',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                margin: '0 auto 20px',
                cursor: 'pointer'
              }}
              onClick={() => (isRecording ? stopRecording() : startRecording())}
            >
              {isProcessing ? <Loader2 size={30} color="white" className="animate-spin" /> : <Mic size={30} color="white" />}
            </motion.div>
            <h4 style={{ margin: '0 0 8px 0', fontSize: '18px', fontWeight: 700 }}>
              {isProcessing ? 'Traitement IA...' : isRecording ? 'Enregistrement en cours...' : 'Prêt à enregistrer'}
            </h4>
            <p style={{ color: '#666', fontSize: '14px' }}>
              {isProcessing
                ? "L'IA analyse votre voix..."
                : isRecording
                ? "Cliquez pour arrêter l'enregistrement."
                : "Cliquez sur le micro pour démarrer l'interaction."}
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div style={styles.card}>
            <h3 style={{ margin: '0 0 15px 0', fontSize: '18px', fontWeight: 700 }}>Dernière Transcription</h3>
            <div style={{ padding: '15px', backgroundColor: '#f9f9f9', borderRadius: '12px', minHeight: '150px', fontSize: '14px', color: '#666', fontStyle: transcription ? 'normal' : 'italic', lineHeight: '1.6' }}>
              {transcription ? transcription.cleaned_text : "Les résultats apparaîtront ici après l'enregistrement..."}
            </div>
          </div>

          <div style={styles.card}>
            <h3 style={{ margin: '0 0 15px 0', fontSize: '18px', fontWeight: 700 }}>Tags Extraits (IA)</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {transcription ? (
                getExtractedTagGroups().length > 0 ? (
                  <>
                    <TagBadge label={`Confiance: ${Number.isFinite(Number(transcription?.confidence)) ? Math.round(Number(transcription.confidence) * 100) : 0}%`} color="#e0f2fe" textColor="#0369a1" />
                    {getExtractedTagGroups().map((group) => (
                      <div key={group.title} style={{ backgroundColor: '#f9fafb', border: '1px solid #eceff3', borderRadius: '12px', padding: '10px' }}>
                        <div style={{ fontSize: '12px', fontWeight: 700, color: '#4b5563', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.4px' }}>{group.title}</div>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                          {group.items.map((item, idx) => (
                            <TagBadge key={`${group.title}-${item}-${idx}`} label={item} color="#f3f4f6" textColor="#111827" />
                          ))}
                        </div>
                      </div>
                    ))}
                  </>
                ) : (
                  <span style={{ color: '#999', fontSize: '13px' }}>Aucun tag détecté pour cette transcription.</span>
                )
              ) : (
                <span style={{ color: '#999', fontSize: '13px' }}>En attente de données...</span>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function TagBadge({ label, color, textColor }) {
  return <span style={{ padding: '6px 12px', borderRadius: '8px', fontSize: '12px', fontWeight: 600, backgroundColor: color, color: textColor }}>{label}</span>;
}

function HistoryTab() {
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [timeFilter, setTimeFilter] = useState('all');
  const [customFrom, setCustomFrom] = useState('');
  const [customTo, setCustomTo] = useState('');

  const now = new Date();
  const dateToInputValue = (d) => d.toISOString().slice(0, 10);
  const toStartOfDay = (d) => {
    const x = new Date(d);
    x.setHours(0, 0, 0, 0);
    return x;
  };
  const toEndOfDay = (d) => {
    const x = new Date(d);
    x.setHours(23, 59, 59, 999);
    return x;
  };
  const subDays = (baseDate, days) => {
    const x = new Date(baseDate);
    x.setDate(x.getDate() - days);
    return x;
  };

  const history = [
    {
      id: 'H-240212-01',
      client: 'Client anonyme',
      timeBucket: 'today',
      recordedAt: subDays(now, 0),
      status: 'Traité',
      duration: '01:46',
      confidence: 94,
      tags: 12,
      summary: 'Préférence forte pour les pièces en cuir, budget clarifié et besoin identifié pour un achat rapide.'
    },
    {
      id: 'H-240211-03',
      client: 'Client anonyme',
      timeBucket: '7d',
      recordedAt: subDays(now, 1),
      status: 'En cours',
      duration: '00:58',
      confidence: 0,
      tags: 0,
      summary: 'Enregistrement effectué, traitement IA en attente.'
    },
    {
      id: 'H-240210-07',
      client: 'Client anonyme',
      timeBucket: '30d',
      recordedAt: subDays(now, 10),
      status: 'Traité',
      duration: '02:34',
      confidence: 91,
      tags: 15,
      summary: 'Tags lifestyle et style détectés avec précision, informations RGPD correctement masquées.'
    }
  ];

  const filteredHistory = history.filter((item) => {
    const matchesSearch =
      item.client.toLowerCase().includes(search.toLowerCase()) ||
      item.id.toLowerCase().includes(search.toLowerCase()) ||
      item.summary.toLowerCase().includes(search.toLowerCase());
    const matchesStatus = statusFilter === 'all' ? true : item.status === statusFilter;

    const sevenDaysAgo = toStartOfDay(subDays(now, 7));
    const thirtyDaysAgo = toStartOfDay(subDays(now, 30));
    const startToday = toStartOfDay(now);
    const endToday = toEndOfDay(now);

    let matchesTime = true;
    if (timeFilter === 'today') {
      matchesTime = item.recordedAt >= startToday && item.recordedAt <= endToday;
    } else if (timeFilter === '7d') {
      matchesTime = item.recordedAt >= sevenDaysAgo && item.recordedAt <= endToday;
    } else if (timeFilter === '30d') {
      matchesTime = item.recordedAt >= thirtyDaysAgo && item.recordedAt <= endToday;
    } else if (timeFilter === 'custom') {
      const hasFrom = !!customFrom;
      const hasTo = !!customTo;
      if (hasFrom || hasTo) {
        const fromDate = hasFrom ? toStartOfDay(new Date(customFrom)) : null;
        const toDate = hasTo ? toEndOfDay(new Date(customTo)) : null;
        if (fromDate && toDate) {
          // Tolérant: si l'utilisateur inverse les dates, on corrige automatiquement.
          const start = fromDate <= toDate ? fromDate : toStartOfDay(new Date(customTo));
          const end = fromDate <= toDate ? toDate : toEndOfDay(new Date(customFrom));
          matchesTime = item.recordedAt >= start && item.recordedAt <= end;
        } else if (fromDate) {
          matchesTime = item.recordedAt >= fromDate;
        } else if (toDate) {
          matchesTime = item.recordedAt <= toDate;
        }
      }
    }

    return matchesSearch && matchesStatus && matchesTime;
  });

  const getStatusStyle = (status) => {
    if (status === 'Traité') {
      return { color: '#166534', backgroundColor: '#dcfce7', border: '1px solid #86efac' };
    }
    return { color: '#92400e', backgroundColor: '#fef3c7', border: '1px solid #fcd34d' };
  };

  const filterControlStyle = {
    ...styles.input,
    marginBottom: 0,
    height: '52px',
    padding: '0 14px',
    lineHeight: '52px'
  };

  const selectControlStyle = {
    ...filterControlStyle,
    appearance: 'none',
    WebkitAppearance: 'none',
    MozAppearance: 'none',
    paddingRight: '42px',
    backgroundImage:
      "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23111827' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E\")",
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'right 16px center',
    backgroundSize: '14px'
  };

  const formatHistoryDate = (dateValue) => {
    if (!(dateValue instanceof Date) || Number.isNaN(dateValue.getTime())) return '';
    return dateValue.toLocaleString('fr-FR', {
      day: '2-digit',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '32px', margin: '0 0 8px 0', fontWeight: 800, letterSpacing: '-1px' }}>Historique</h1>
        <p style={{ margin: 0, color: '#666' }}>Suivez toutes les interactions audio et leur état de traitement.</p>
      </div>

      <div style={{ ...styles.card, marginBottom: '16px', display: 'flex', gap: '12px', alignItems: 'center', flexWrap: 'wrap' }}>
        <div style={{ position: 'relative', flex: 1, minWidth: '280px' }}>
          <Search size={16} style={{ position: 'absolute', right: '12px', top: '50%', transform: 'translateY(-50%)', color: '#9ca3af' }} />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Rechercher un ID, un client ou un résumé..."
            style={{ ...styles.input, paddingLeft: '22px', paddingRight: '38px', marginBottom: 0 }}
          />
        </div>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          style={{ ...selectControlStyle, width: 'fit-content', minWidth: 'unset', flexShrink: 0 }}
        >
          <option value="all">Tous les statuts</option>
          <option value="Traité">Traité</option>
          <option value="En cours">En cours</option>
        </select>
        <select
          value={timeFilter}
          onChange={(e) => setTimeFilter(e.target.value)}
          style={{ ...selectControlStyle, width: 'fit-content', minWidth: 'unset', flexShrink: 0 }}
        >
          <option value="all">Tout le temps</option>
          <option value="today">Aujourd'hui</option>
          <option value="7d">7 derniers jours</option>
          <option value="30d">30 derniers jours</option>
          <option value="custom">Personnalisé</option>
        </select>
      </div>

      {timeFilter === 'custom' && (
        <div style={{ ...styles.card, marginBottom: '16px', display: 'grid', gridTemplateColumns: '1fr 1fr auto', gap: '12px', alignItems: 'end' }}>
          <div>
            <label style={{ ...styles.label, marginBottom: '6px' }}>Du</label>
            <input
              type="date"
              value={customFrom}
              onChange={(e) => setCustomFrom(e.target.value)}
              max={dateToInputValue(now)}
              style={filterControlStyle}
            />
          </div>
          <div>
            <label style={{ ...styles.label, marginBottom: '6px' }}>Au</label>
            <input
              type="date"
              value={customTo}
              onChange={(e) => setCustomTo(e.target.value)}
              max={dateToInputValue(now)}
              style={filterControlStyle}
            />
          </div>
          <button
            type="button"
            onClick={() => {
              setCustomFrom('');
              setCustomTo('');
            }}
            style={{ height: '52px', padding: '0 14px', borderRadius: '12px', border: '1px solid #d1d5db', background: '#fff', cursor: 'pointer', fontWeight: 600 }}
          >
            Réinitialiser
          </button>
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {filteredHistory.map((item) => (
          <div key={item.id} style={{ ...styles.card, padding: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '14px' }}>
              <div>
                <div style={{ fontWeight: 800, fontSize: '16px', marginBottom: '2px' }}>{item.client}</div>
                <div style={{ fontSize: '12px', color: '#6b7280', fontWeight: 600 }}>ID: {item.id}</div>
              </div>
              <div style={{ ...getStatusStyle(item.status), borderRadius: '999px', padding: '5px 10px', fontSize: '12px', fontWeight: 700, display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                {item.status === 'Traité' ? <CheckCircle2 size={14} /> : <AlertCircle size={14} />}
                {item.status}
              </div>
            </div>

            <div style={{ display: 'flex', gap: '16px', marginTop: '10px', fontSize: '13px', color: '#4b5563', flexWrap: 'wrap' }}>
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                <Calendar size={14} /> {formatHistoryDate(item.recordedAt)}
              </span>
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                <Clock3 size={14} /> {item.duration}
              </span>
              <span>Tags: <strong>{item.tags}</strong></span>
              <span>Confiance: <strong>{item.confidence}%</strong></span>
            </div>

            <div style={{ marginTop: '10px', padding: '10px 12px', borderRadius: '10px', backgroundColor: '#f9fafb', border: '1px solid #eef2f7', color: '#374151', fontSize: '13px', lineHeight: '1.5' }}>
              {item.summary}
            </div>
          </div>
        ))}

        {filteredHistory.length === 0 && <div style={{ ...styles.card, textAlign: 'center', color: '#6b7280' }}>Aucun résultat pour ce filtre.</div>}
      </div>
    </div>
  );
}

function DatabaseTab() {
  return (
    <div>
      <h1 style={{ fontSize: '32px', margin: '0 0 8px 0' }}>Base de données</h1>
      <div style={{ ...styles.card, marginTop: '24px' }}>
        <p style={{ margin: 0, color: '#555' }}>Section base de données prête.</p>
      </div>
    </div>
  );
}

function PlaceholderTab({ title }) {
  return (
    <div>
      <h1 style={{ fontSize: '32px', margin: '0 0 8px 0' }}>{title}</h1>
      <div style={{ ...styles.card, marginTop: '24px' }}>
        <p style={{ margin: 0, color: '#555' }}>Cette section est restaurée et peut être affinée.</p>
      </div>
    </div>
  );
}

export default App;
