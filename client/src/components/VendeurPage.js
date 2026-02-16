import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Mic, Square, History, LogOut, Loader2, Search, Clock3, Calendar, Trash2, ChevronDown } from 'lucide-react';
import { supabase } from '../supabaseClient';

const TIME_OPTIONS = [
  { id: 'all', label: 'Tout le temps' },
  { id: 'today', label: "Aujourd'hui" },
  { id: '7d', label: '7 derniers jours' },
  { id: '30d', label: '30 derniers jours' },
  { id: 'custom', label: 'Personnalisé' },
];

const formatDate = (value) =>
  new Date(value).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' });
const formatTime = (value) =>
  new Date(value).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });

const VENDEUR_HISTORY_STORAGE_KEY = 'lvmh_vendeur_history_v2';

const TAG_LABELS = {
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
  actions_crm: 'Actions CRM',
  echeances: 'Echéances',
  canaux_contact: 'Canaux contact',
};

const TAG_SECTIONS = [
  { title: 'IDENTITÉ', keys: ['genre', 'langue', 'statut_client'] },
  { title: 'DÉMOGRAPHIQUE', keys: ['age', 'profession', 'ville', 'pays', 'famille'] },
  { title: 'LIFESTYLE', keys: ['sport', 'musique', 'animaux', 'voyage', 'art_culture', 'gastronomie'] },
  { title: 'STYLE', keys: ['pieces_favorites', 'pieces_recherchees', 'couleurs', 'matieres', 'sensibilite_mode', 'tailles', 'style'] },
  { title: 'ACHAT', keys: ['budget', 'urgence_score', 'motif_achat', 'marques_preferees', 'frequence_achat'] },
  { title: 'CRM', keys: ['actions_crm', 'echeances', 'canaux_contact'] },
];

const loadPersistedVendeurHistory = () => {
  if (typeof window === 'undefined') return [];
  try {
    const raw = window.localStorage.getItem(VENDEUR_HISTORY_STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
};

export default function VendeurPage({ onLogout }) {
  const [activeTab, setActiveTab] = useState('record');
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);
  const [transcriptionResult, setTranscriptionResult] = useState(null);
  const [history, setHistory] = useState(() => loadPersistedVendeurHistory());
  const [search, setSearch] = useState('');
  const [timeFilter, setTimeFilter] = useState('all');
  const [customFrom, setCustomFrom] = useState('');
  const [customTo, setCustomTo] = useState('');
  const audioChunksRef = useRef([]);

  const extractClientName = (text) => {
    if (!text || typeof text !== 'string') return null;
    const patterns = [
      /(?:rendez[- ]vous|rdv)\s+(mme|mr|monsieur|madame)\s+([A-ZÀ-ÖØ-Ý][a-zà-öø-ÿ'-]+)/i,
      /(?:s[' ]appelle|s'appelle)\s+([A-ZÀ-ÖØ-Ý][a-zà-öø-ÿ'-]+(?:\s+[A-ZÀ-ÖØ-Ý][a-zà-öø-ÿ'-]+){0,2})/i,
      /(?:client(?:e)?\s*:\s*)([A-ZÀ-ÖØ-Ý][a-zà-öø-ÿ'-]+(?:\s+[A-ZÀ-ÖØ-Ý][a-zà-öø-ÿ'-]+){0,2})/i,
    ];
    for (const p of patterns) {
      const m = text.match(p);
      if (!m) continue;
      if (m[2]) return m[2].trim();
      if (m[1]) return m[1].trim();
    }
    return null;
  };

  const fetchHistory = async () => {
    const { data } = await supabase
      .from('transcriptions')
      .select('id, client_name, content_summary, created_at, tags, metadata')
      .order('created_at', { ascending: false })
      .limit(50);
    if (!Array.isArray(data)) return;
    setHistory((prev) => {
      const localOnly = (prev || []).filter((row) => typeof row.id === 'string' && row.id.startsWith('local-'));
      const merged = [...localOnly, ...data];
      const uniq = [];
      const seen = new Set();
      for (const row of merged) {
        const key = String(row.id);
        if (seen.has(key)) continue;
        seen.add(key);
        uniq.push(row);
      }
      return uniq.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    });
  };

  const makeLocalHistoryItemFromResult = (result) => {
    const summary = result?.cleaned_text || result?.transcription || '';
    const tags = result?.tags_extracted || result?.tags || {};
    const detectedClient = extractClientName(summary) || extractClientName(result?.transcription) || 'Client anonyme';
    const confidence = Number.isFinite(Number(result?.confidence)) ? Math.round(Number(result.confidence) * 100) : 99;
    return {
      id: `local-${Date.now()}-${Math.random().toString(16).slice(2, 8)}`,
      client_name: detectedClient,
      content_summary: summary || 'Transcription disponible',
      created_at: new Date().toISOString(),
      tags,
      metadata: { confidence, local: true },
      sentiment: 'Traité',
    };
  };

  const persistTranscription = async (result) => {
    const summary = result?.cleaned_text || result?.transcription || '';
    const tags = result?.tags_extracted || result?.tags || {};
    const detectedClient = extractClientName(summary) || extractClientName(result?.transcription) || 'Client anonyme';
    const confidence = Number.isFinite(Number(result?.confidence)) ? Math.round(Number(result.confidence) * 100) : 99;
    return supabase.from('transcriptions').insert([
      {
        client_name: detectedClient,
        content_summary: summary || 'Transcription disponible',
        raw_text: result?.transcription || summary,
        sentiment: 'Traité',
        tags,
        source_filename: 'vocal_recording.webm',
        metadata: { confidence },
      },
    ]);
  };

  const transcribeBlob = async (blob) => {
    if (!blob) return;
    setIsProcessing(true);
    try {
      const formData = new FormData();
      formData.append('audio', blob, 'recording.webm');
      const response = await fetch('/api/transcribe', { method: 'POST', body: formData });
      if (!response.ok) throw new Error('Erreur serveur lors de la transcription');
      const result = await response.json();
      setTranscriptionResult(result);

      // Ajout immédiat dans l'historique (UX instantanée, même si Supabase échoue).
      const localItem = makeLocalHistoryItemFromResult(result);
      setHistory((prev) => [localItem, ...(prev || [])]);

      // Sync backend en parallèle; on garde l'item local en fallback.
      const { error } = await persistTranscription(result);
      if (!error) await fetchHistory();
    } catch (e) {
      console.error(e);
      alert(`Erreur de transcription: ${e.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      audioChunksRef.current = [];

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) audioChunksRef.current.push(event.data);
      };

      recorder.onstop = async () => {
        const blob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        setAudioBlob(blob);
        await transcribeBlob(blob);
      };

      recorder.start();
      setMediaRecorder(recorder);
      setIsRecording(true);
      setAudioBlob(null);
      setTranscriptionResult(null);
    } catch (err) {
      console.error('Error accessing microphone:', err);
      alert("Impossible d'accéder au microphone. Vérifiez les permissions.");
    }
  };

  const stopRecording = () => {
    if (!mediaRecorder || !isRecording) return;
    mediaRecorder.stop();
    setIsRecording(false);
    mediaRecorder.stream.getTracks().forEach((track) => track.stop());
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  useEffect(() => {
    try {
      window.localStorage.setItem(VENDEUR_HISTORY_STORAGE_KEY, JSON.stringify(history || []));
    } catch {
      // ignore storage quota/private mode errors
    }
  }, [history]);

  useEffect(() => {
    if (activeTab === 'history') fetchHistory();
  }, [activeTab]);

  useEffect(() => {
    if (!customFrom || !customTo) return;
    if (customFrom > customTo) {
      setCustomFrom(customTo);
      setCustomTo(customFrom);
    }
  }, [customFrom, customTo]);

  const filteredHistory = useMemo(() => {
    const now = new Date();
    const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    return history.filter((item) => {
      const text = `${item.client_name || ''} ${item.content_summary || ''} ${item.id || ''}`.toLowerCase();
      const matchesSearch = !search.trim() || text.includes(search.trim().toLowerCase());
      const created = new Date(item.created_at);
      let matchesTime = true;
      if (timeFilter === 'today') matchesTime = created >= startOfToday;
      if (timeFilter === '7d') matchesTime = now - created <= 7 * 24 * 60 * 60 * 1000;
      if (timeFilter === '30d') matchesTime = now - created <= 30 * 24 * 60 * 60 * 1000;
      if (timeFilter === 'custom' && customFrom && customTo) {
        const start = new Date(`${customFrom}T00:00:00`);
        const end = new Date(`${customTo}T23:59:59`);
        matchesTime = created >= start && created <= end;
      }
      return matchesSearch && matchesTime;
    });
  }, [history, search, timeFilter, customFrom, customTo]);

  const tagsCount = (tags) => {
    if (!tags || typeof tags !== 'object') return 0;
    return Object.entries(tags).filter(([, value]) => {
      if (Array.isArray(value)) return value.length > 0;
      return value !== null && value !== undefined && String(value).trim() !== '';
    }).length;
  };

  const buildTagSections = (tags) => {
    if (!tags || typeof tags !== 'object') return [];
    const hidden = new Set(['cleaned_text', 'centres_interet', 'timing']);
    const sections = [];
    for (const section of TAG_SECTIONS) {
      const items = [];
      for (const key of section.keys) {
        if (hidden.has(key)) continue;
        const value = tags[key];
        if (Array.isArray(value) && value.length > 0) {
          items.push(`${TAG_LABELS[key] || key}: ${value.join(', ')}`);
        } else if (value !== null && value !== undefined && String(value).trim() !== '') {
          items.push(`${TAG_LABELS[key] || key}: ${String(value)}`);
        }
      }
      if (items.length > 0) sections.push({ title: section.title, items });
    }
    return sections;
  };

  const deleteHistoryItem = async (item) => {
    setHistory((prev) => prev.filter((x) => String(x.id) !== String(item.id)));
    // Si l'item vient de la DB, on tente aussi suppression serveur.
    if (typeof item.id === 'number') {
      try {
        await supabase.from('transcriptions').delete().eq('id', item.id);
      } catch {
        // on ne bloque pas l'UX en cas d'erreur serveur
      }
    }
  };

  return (
    <div className="min-h-screen bg-[#f4f5f7] pb-28">
      <header className="px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="h-[40px] w-[40px] rounded-full border border-black bg-white overflow-hidden flex items-center justify-center">
            <img src="/assets/images/loewe_logo.png" alt="Loewe" className="w-[110%] h-[110%] object-contain" />
          </div>
          <h1 className="text-[17px] max-md:text-[16px] font-extrabold text-[#1a1a1a] tracking-tight">VENDEUR</h1>
        </div>
        <button
          onClick={onLogout}
          className="p-2 bg-white rounded-full border border-gray-200 text-gray-600 hover:bg-red-50 hover:text-red-500 transition"
          title="Déconnexion"
        >
          <LogOut size={18} />
        </button>
      </header>

      <main className="px-6 w-full -mt-3">
        {activeTab === 'record' && (
          <div className="w-full">
            <h2 className="text-[38px] max-md:text-3xl font-extrabold text-[#111827] mb-1 text-center">Enregistrement Client</h2>
            <p className="text-[#6b7280] mb-5 text-base max-md:text-sm text-center">
              Capturez les échanges clients et laissez l’IA en extraire les données.
            </p>

            <div className="grid grid-cols-[1.4fr_1fr] gap-4 max-lg:grid-cols-1 items-stretch mt-3">
              <div className="bg-white rounded-3xl border border-gray-100 p-5 min-h-[380px] flex">
                <div className="bg-[#f7f7f9] border border-gray-200 rounded-2xl w-full min-h-[320px] flex flex-col items-center justify-center px-7 text-center">
                  <button
                    onClick={() => (isRecording ? stopRecording() : startRecording())}
                    className={`h-20 w-20 rounded-full flex items-center justify-center text-white transition ${
                      isRecording ? 'bg-red-500' : 'bg-black'
                    }`}
                    title={isRecording ? "Arrêter l'enregistrement" : "Démarrer l'enregistrement"}
                  >
                    {isProcessing ? <Loader2 size={30} className="animate-spin" /> : isRecording ? <Square size={28} fill="currentColor" /> : <Mic size={30} />}
                  </button>

                  <h3 className="mt-4 text-xl max-md:text-lg font-bold text-[#1f2937]">
                    {isProcessing ? 'Traitement IA...' : isRecording ? 'Enregistrement en cours...' : 'Prêt à enregistrer'}
                  </h3>
                  <p className="text-[#6b7280] mt-2 text-base max-md:text-sm">
                    {isProcessing
                      ? "L'IA analyse votre voix..."
                      : isRecording
                      ? "Cliquez pour arrêter l'enregistrement."
                      : 'Activez le micro pour enregistrer le compte rendu du rendez-vous'}
                  </p>

                  {audioBlob && !isRecording && (
                    <button
                      onClick={() => setAudioBlob(null)}
                      className="mt-4 inline-flex items-center gap-2 px-3 py-1.5 rounded-lg border border-gray-200 text-sm text-gray-600 hover:bg-white"
                    >
                      <Trash2 size={14} />
                      Effacer l’audio
                    </button>
                  )}
                </div>
              </div>

              <div className="flex flex-col gap-4 min-h-[380px]">
                <div className="bg-white rounded-3xl border border-gray-100 p-4 flex-1 flex flex-col">
                  <div className="bg-[#f7f7f9] rounded-xl p-4 w-full flex-1 min-h-[170px] -mt-1 text-[#6b7280] text-sm">
                    <h3 className="text-[24px] max-md:text-xl font-bold text-[#111827] mb-2.5">Transcription de l'audio</h3>
                    <div>
                      {transcriptionResult?.cleaned_text || transcriptionResult?.transcription || "Les résultats apparaîtront ici après l'enregistrement..."}
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-3xl border border-gray-100 p-4 flex-1 flex flex-col">
                  <div className="bg-[#f7f7f9] rounded-xl p-4 w-full flex-1 min-h-[170px] -mt-1">
                    <h3 className="text-[24px] max-md:text-xl font-bold text-[#111827] mb-2.5">Tags détectés</h3>
                    {transcriptionResult?.tags_extracted || transcriptionResult?.tags ? (() => {
                      const tagsPayload = transcriptionResult.tags_extracted || transcriptionResult.tags;
                      const sections = buildTagSections(tagsPayload);
                      const confidence = Number.isFinite(Number(transcriptionResult?.confidence))
                        ? Math.round(Number(transcriptionResult.confidence) * 100)
                        : 99;
                      return (
                        <div className="space-y-2.5">
                          <div className="bg-[#dbeafe] text-[#1d4f91] font-bold px-2.5 py-1.5 rounded-lg text-xs">
                            Confiance: {confidence}%
                          </div>
                          {sections.map((section) => (
                            <div key={section.title} className="bg-[#f3f4f6] border border-[#e5e7eb] rounded-xl p-2.5">
                              <p className="text-[#4b5563] text-sm font-extrabold tracking-wide mb-1.5">{section.title}</p>
                              <div className="flex flex-wrap gap-1.5">
                                {section.items.map((item, idx) => (
                                  <span key={`${section.title}-${idx}`} className="px-2.5 py-1 rounded-lg bg-[#edeff2] text-xs text-[#111827] font-semibold">
                                    {item}
                                  </span>
                                ))}
                              </div>
                            </div>
                          ))}
                        </div>
                      );
                    })() : (
                      <p className="text-[#9ca3af] text-base">En attente de données...</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'history' && (
          <div className="max-w-[1060px] mx-auto">
            <h2 className="text-[42px] max-md:text-3xl font-extrabold text-[#111827] mb-1 text-center">Historique</h2>
            <p className="text-[#6b7280] mb-6 text-lg text-center">Suivez toutes les interactions audio et leur état de traitement.</p>

            <div className="bg-white rounded-2xl border border-gray-100 p-4 mb-4 flex gap-3 max-md:flex-col">
              <div className="relative flex-1">
                <Search size={16} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400" />
                <input
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder="Rechercher un ID, un client ou un résumé..."
                  className="w-full border border-gray-200 rounded-xl py-2.5 pl-4 pr-9 text-sm focus:outline-none focus:ring-2 focus:ring-[#c57b62]/20"
                />
              </div>
              <div className="relative min-w-[138px]">
                <ChevronDown size={16} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
                <select
                  value={timeFilter}
                  onChange={(e) => setTimeFilter(e.target.value)}
                  className="appearance-none border border-gray-200 rounded-xl py-2.5 pl-9 pr-3 text-sm bg-white min-w-[138px] w-full"
                >
                  {TIME_OPTIONS.map((opt) => (
                    <option key={opt.id} value={opt.id}>
                      {opt.label}
                    </option>
                  ))}
                </select>
              </div>
              {timeFilter === 'custom' && (
                <>
                  <input
                    type="date"
                    value={customFrom}
                    onChange={(e) => setCustomFrom(e.target.value)}
                    className="border border-gray-200 rounded-xl py-2.5 px-3 text-sm bg-white min-w-[145px]"
                    title="Date de début"
                  />
                  <input
                    type="date"
                    value={customTo}
                    onChange={(e) => setCustomTo(e.target.value)}
                    className="border border-gray-200 rounded-xl py-2.5 px-3 text-sm bg-white min-w-[145px]"
                    title="Date de fin"
                  />
                </>
              )}
            </div>

            <div className="flex flex-col gap-3">
              {filteredHistory.map((item) => {
                const count = tagsCount(item.tags);
                const confidence = item?.metadata?.confidence || 99;
                return (
                  <div key={item.id} className="bg-white rounded-2xl border border-gray-100 p-4">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <h3 className="font-bold text-2xl text-[#111827]">{item.client_name || 'Client anonyme'}</h3>
                        <p className="text-xs text-[#9ca3af] font-semibold">{`ID: ${item.id}`}</p>
                      </div>
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => deleteHistoryItem(item)}
                          className="p-1.5 rounded-full text-gray-400 hover:text-red-500 hover:bg-red-50 transition"
                          title="Supprimer"
                        >
                          <Trash2 size={15} />
                        </button>
                      </div>
                    </div>

                    <div className="mt-2 text-sm text-[#4b5563] flex gap-4 flex-wrap">
                      <span className="inline-flex items-center gap-1"><Calendar size={14} /> {formatDate(item.created_at)}</span>
                      <span className="inline-flex items-center gap-1"><Clock3 size={14} /> {formatTime(item.created_at)}</span>
                      <span>{`Tags: ${count}`}</span>
                      <span>{`Confiance: ${confidence}%`}</span>
                    </div>

                    <div className="mt-3 bg-[#f7f7f9] rounded-lg p-3 text-sm text-[#4b5563]">
                      {item.content_summary || 'Transcription disponible'}
                    </div>
                  </div>
                );
              })}

              {filteredHistory.length === 0 && (
                <div className="bg-white rounded-2xl border border-gray-100 p-10 text-center text-gray-400">
                  <History size={36} className="mx-auto mb-2 opacity-40" />
                  <p>Aucun historique pour ce filtre.</p>
                </div>
              )}
            </div>
          </div>
        )}
      </main>

      <div className="fixed bottom-4 left-1/2 -translate-x-1/2 z-30 w-[calc(100%-24px)] max-w-[430px]">
        <div className="flex bg-white p-[2px] rounded-[11px] shadow-sm border border-gray-100">
          <button
            onClick={() => setActiveTab('record')}
            className={`flex-1 py-[3px] text-[17px] max-md:text-[14px] font-bold rounded-[7px] transition ${
              activeTab === 'record' ? 'bg-[#c57b62] text-white' : 'text-[#6b7280]'
            }`}
          >
            Micro
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={`flex-1 py-[3px] text-[17px] max-md:text-[14px] font-bold rounded-[7px] transition ${
              activeTab === 'history' ? 'bg-[#c57b62] text-white' : 'text-[#6b7280]'
            }`}
          >
            Historique
          </button>
        </div>
      </div>
    </div>
  );
}
