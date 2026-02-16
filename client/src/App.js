/*
 * ═══════════════════════════════════════════════════════════
 *  LVMH PULSE DASHBOARD — Full Supabase Integration
 *  CRA (React) + Tailwind CSS + Supabase + Framer Motion
 * ═══════════════════════════════════════════════════════════
 *
 *  SQL SCHEMA — Run this in Supabase SQL Editor FIRST:
 *  See file: client/supabase_schema.sql
 */
import React, { useState, useEffect, useCallback } from 'react';
import {
  Menu, Search, Plus, ArrowRight, Mic, Upload, UploadCloud, ChevronDown, ChevronLeft, ChevronRight,
  Lock, Clock, MoreVertical, Filter, X, CheckCircle2, AlertTriangle, Loader2,
  BarChart3, Calendar as CalIcon, TrendingUp, Sparkles, Play, Database, Eye, AlertCircle, Clipboard, Dna, User, LogOut, Tag
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { supabase } from './supabaseClient';
import ClientProfileCard from './components/ClientProfileCard';
import DatabaseFilterPage from './components/DatabaseFilterPage';
import LoginPage from './components/LoginPage';
import VendeurPage from './components/VendeurPage';
import AnalysisPage from './components/AnalysisPage';
import StatsPage from './components/StatsPage';

/* ═══ SIMULATED AI DATA ═══ */
const FAKE_CLIENTS = [
  { name: 'Sophie M.', summary: 'Intéressée par collection Capucines SS26', sentiment: 'positif' },
  { name: 'Marc D.', summary: 'Demande entretien souliers, client fidèle', sentiment: 'neutre' },
  { name: 'Hélène R.', summary: 'Cross-sell montre Tank après achat sac', sentiment: 'positif' },
  { name: 'Louis P.', summary: 'Anniversaire dans 30 jours, budget élevé', sentiment: 'positif' },
  { name: 'Claire B.', summary: 'Voyage Dubai prévu, intérêt Travel Retail', sentiment: 'positif' },
  { name: 'Jean F.', summary: 'Réclamation livraison — à traiter urgent', sentiment: 'négatif' },
  { name: 'Nadia K.', summary: 'Nouvelle cliente référée par VIP', sentiment: 'positif' },
  { name: 'Pierre V.', summary: 'Commande cuir exotique, haute valeur', sentiment: 'positif' },
];
const FAKE_TAGS = ['Maroquinerie', 'Anniversaire', 'VIP', 'Cross-sell', 'Souliers', 'Montres', 'Voyage', 'Parfum', 'Joaillerie', 'Haute Couture'];
const pick = (arr, n) => [...arr].sort(() => 0.5 - Math.random()).slice(0, n);

/* ═══ REUSABLE COMPONENTS ═══ */

const C = ({ children, className = '', ...props }) => (
  <div className={`bg-white rounded-[40px] shadow-[0_20px_50px_-12px_rgba(0,0,0,0.03)] p-6 relative ${className}`} {...props}>{children}</div>
);

const months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc'];

const CalendarWidget = ({
  activeDays = [],
  selectedDays = [],
  setSelectedDays,
  month,
  setMonth,
  year,
  setYear
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [dragStartMode, setDragStartMode] = useState(null);

  // Check for "Today"
  const todayInitial = new Date();
  const isToday = (d) => {
    const today = new Date();
    return d === today.getDate() && months.indexOf(month) === today.getMonth() && year === today.getFullYear();
  };

  // Dynamic days based on month/year
  const getDaysInMonth = (m, y) => {
    const monthIndex = months.indexOf(m);
    return new Date(y, monthIndex + 1, 0).getDate();
  };

  const daysCount = getDaysInMonth(month, year);
  const days = Array.from({ length: daysCount }, (_, i) => i + 1);

  const toggleDay = (d, forceState = null) => {
    setSelectedDays(prev => {
      const isSelected = prev.includes(d);
      const newState = forceState !== null ? forceState : !isSelected;

      if (newState && !isSelected) return [...prev, d];
      if (!newState && isSelected) return prev.filter(day => day !== d);
      return prev;
    });
  };

  const handleMouseDown = (d) => {
    setIsDragging(true);
    const willSelect = !selectedDays.includes(d);
    setDragStartMode(willSelect);
    toggleDay(d, willSelect);
  };

  const handleMouseEnter = (d) => {
    if (isDragging) {
      toggleDay(d, dragStartMode);
    }
  };

  useEffect(() => {
    const handleMouseUp = () => setIsDragging(false);
    window.addEventListener('mouseup', handleMouseUp);
    return () => window.removeEventListener('mouseup', handleMouseUp);
  }, []);

  return (
    <div className="flex flex-row h-full w-full gap-4 items-center select-none pl-1 pr-1">
      {/* LEFT: DYNAMIC 7-COL GRID (Standard Week) */}
      <div className="flex-1 grid grid-cols-7 grid-rows-5 gap-1.5 h-full max-h-[110px]">
        {days.map(d => (
          <button
            key={d}
            onMouseDown={() => handleMouseDown(d)}
            onMouseEnter={() => handleMouseEnter(d)}
            className={`
              w-full h-full rounded-md flex items-center justify-center text-[9px] font-medium transition-all duration-150 relative
              ${isToday(d)
                ? selectedDays.includes(d)
                  ? 'bg-[#C87961] text-white shadow-md font-bold border-2 border-emerald-500 scale-110 z-10'
                  : 'bg-emerald-500 text-white font-bold shadow-md hover:bg-emerald-600'
                : selectedDays.includes(d)
                  ? 'bg-[#C87961] text-white shadow-sm scale-110'
                  : 'bg-gray-100 text-gray-400 hover:bg-gray-200'}
            `}
          >
            {d}
            {/* Dot for activity */}
            {activeDays.includes(d) && !isToday(d) && (
              <div className="absolute bottom-1 h-1 w-1 rounded-full bg-emerald-500" />
            )}
          </button>
        ))}
      </div>

      {/* RIGHT: Selectors */}
      <div className="flex flex-col gap-2 min-w-[50px] justify-center items-end py-1">
        {/* Year Selector with Arrows */}
        <div className="flex items-center gap-1 border-b-2 border-transparent pb-1">
          <button onClick={() => setYear(y => y - 1)} className="text-[#C87961] hover:bg-orange-50 rounded p-0.5"><ChevronLeft size={14} /></button>
          <span className="text-[14px] font-bold text-[#111]">{year}</span>
          <button
            onClick={() => setYear(y => y < todayInitial.getFullYear() ? y + 1 : y)}
            disabled={year >= todayInitial.getFullYear()}
            className={`rounded p-0.5 ${year >= todayInitial.getFullYear() ? 'text-gray-300 cursor-not-allowed' : 'text-[#C87961] hover:bg-orange-50'}`}
          >
            <ChevronRight size={14} />
          </button>
        </div>

        {/* Month List */}
        <div className="flex flex-col items-end gap-1 h-[90px] overflow-hidden mask-gradient relative">
          {(() => {
            const startMode = months.indexOf(month);
            const rotated = [...months.slice(startMode), ...months.slice(0, startMode)];
            return rotated.slice(0, 5).map(m => (
              <span
                key={m}
                onClick={() => setMonth(m)}
                className={`text-[12px] cursor-pointer transition-colors ${m === month
                  ? 'font-bold text-[#111] border-r-2 border-[#C87961] pr-2'
                  : 'font-medium text-gray-300 hover:text-gray-500 pr-2 border-r-2 border-transparent'
                  }`}
              >
                {m}
              </span>
            ));
          })()}
        </div>
      </div>
    </div>
  );
};

const MiniBars = ({ color = '#C87961', alt = '#E8D5CF' }) => {
  const h = [40, 65, 35, 80, 50, 70, 45, 60, 75, 30];
  return (
    <div className="flex items-end gap-[4px] h-20">
      {h.map((v, i) => (
        <div key={i} className="w-[6px] rounded-full transition-all" style={{ height: `${v}%`, backgroundColor: i % 2 === 0 ? color : alt }} />
      ))}
    </div>
  );
};

const Spark = ({ color = '#C87961' }) => (
  <svg viewBox="0 0 100 28" className="w-full h-7">
    <path d="M0,20 C10,18 15,14 25,12 S40,16 50,10 S65,18 75,8 S90,14 100,12" fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" />
  </svg>
);



/* ═══ ANIMATED NUMBER ═══ */
const AnimatedNumber = ({ value }) => {
  const [display, setDisplay] = useState(value);
  useEffect(() => {
    const start = display;
    const diff = value - start;
    if (diff === 0) return;
    const steps = 20;
    let step = 0;
    const timer = setInterval(() => {
      step++;
      setDisplay(Math.round(start + (diff * step) / steps));
      if (step >= steps) clearInterval(timer);
    }, 40);
    return () => clearInterval(timer);
  }, [value]);
  return <span>{display.toLocaleString()}</span>;
};

/* ═══════════════════════════════════════════════════════════
   MAIN DASHBOARD — Connected to Supabase
   ═══════════════════════════════════════════════════════════ */
export default function App() {
  const [showModal, setShowModal] = useState(false);
  const [showDbModal, setShowDbModal] = useState(false);
  // Error Modal State
  const [showErrorModal, setShowErrorModal] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [showClientProfile, setShowClientProfile] = useState(false);

  // View State (Dashboard vs Database)
  const [currentView, setCurrentView] = useState('dashboard');

  // ── Auth / Role State ──
  const [userRole, setUserRole] = useState(null); // 'analyste' | 'vendeur' | null

  useEffect(() => {
    const savedRole = localStorage.getItem('lvmh_user_role');
    if (savedRole) setUserRole(savedRole);
  }, []);

  const handleLogin = (role) => {
    setUserRole(role);
    localStorage.setItem('lvmh_user_role', role);
  };

  const handleLogout = () => {
    setUserRole(null);
    localStorage.removeItem('lvmh_user_role');
    setCurrentView('dashboard'); // Reset view for next login
  };

  const copyError = () => {
    navigator.clipboard.writeText(errorMessage);
    alert("Code erreur copié !");
  };

  // ── Upload states ──
  const [uploadPhase, setUploadPhase] = useState('idle'); // idle | processing | done
  const [lastBatchId, setLastBatchId] = useState(null);
  const [lastTransCount, setLastTransCount] = useState(0);

  // ── KPI states ──
  const [totalCount, setTotalCount] = useState(0);

  // ── Date Selection State (Lifted from CalendarWidget) ──
  const [selectedDays, setSelectedDays] = useState([new Date().getDate()]);
  const [selectedMonth, setSelectedMonth] = useState(months[new Date().getMonth()]);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
  const [tagCounts, setTagCounts] = useState([]);
  const [recentTranscriptions, setRecentTranscriptions] = useState([]);

  // V2 New States
  const [leadsCount, setLeadsCount] = useState(0);
  const [matchRate, setMatchRate] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [uploadDates, setUploadDates] = useState([]); // Array of days (numbers) for current month

  // ── Fetch total transcription count ──
  const fetchCount = useCallback(async () => {
    if (!supabase) return;
    try {
      // 1. Total Transcriptions
      const { count: transCount, error: transErr } = await supabase
        .from('transcriptions')
        .select('*', { count: 'exact', head: true });
      if (!transErr && transCount !== null) setTotalCount(transCount);

      // 2. Leads (Clients with > 0 transcriptions? Or just all clients)
      // "Leads Qualifiés" -> We'll use Total Clients for now.
      const { count: clientCount, error: clientErr } = await supabase
        .from('clients')
        .select('*', { count: 'exact', head: true });
      if (!clientErr && clientCount !== null) setLeadsCount(clientCount);

      // 3. Match Rate (Avg Sentiment Positif %)
      // Fetch sentiment of last 100?
      const { data: sentData, error: sentErr } = await supabase
        .from('transcriptions')
        .select('sentiment')
        .limit(100);

      if (!sentErr && sentData && sentData.length > 0) {
        const positive = sentData.filter(r => r.sentiment === 'positif').length;
        const rate = Math.round((positive / sentData.length) * 100);
        setMatchRate(rate);
      } else {
        setMatchRate(0);
      }
    } catch (e) { console.warn('fetchCount error:', e); }
  }, []);

  // ── Fetch tag aggregation ──
  const fetchTags = useCallback(async () => {
    if (!supabase) return;
    try {
      const { data, error } = await supabase
        .from('tags')
        .select('tag_name');
      if (!error && data) {
        const counts = {};
        data.forEach(t => { counts[t.tag_name] = (counts[t.tag_name] || 0) + 1; });
        const sorted = Object.entries(counts)
          .map(([name, count]) => ({ name, count }))
          .sort((a, b) => b.count - a.count);
        setTagCounts(sorted);
      }
    } catch (e) { console.warn('fetchTags error:', e); }
  }, []);

  // ── Fetch recent transcriptions (for DB modal) ──
  const fetchRecent = useCallback(async () => {
    if (!supabase) return;
    try {
      let query = supabase
        .from('transcriptions')
        .select(`
          id, 
          client_name, 
          content_summary, 
          sentiment, 
          created_at,
          raw_text,
          tags ( tag_name )
        `)
        .order('created_at', { ascending: false })
        .limit(10);

      // Apply Search Filter (Client Name OR Summary)
      if (searchQuery) {
        query = query.or(`client_name.ilike.%${searchQuery}%,content_summary.ilike.%${searchQuery}%`);
      }

      const { data, error } = await query;
      if (!error && data) {
        setRecentTranscriptions(data);

        // Extract dates for Calendar (simple heuristic: day of month)
        // Only for these visible 10, ideally we fetch a separate distinct list
        const days = data.map(t => new Date(t.created_at).getDate());
        setUploadDates([...new Set(days)]);
      }
    } catch (e) { console.warn('fetchRecent error:', e); }
  }, []);

  // ... (skipping unchanged parts) ...

  {/* DATABASE TABLE */ }
  <div className="overflow-x-auto">
    <table className="w-full text-left border-collapse">
      <thead>
        <tr className="text-sm text-gray-500 border-b">
          <th className="p-3 font-medium">Client</th>
          <th className="p-3 font-medium">Résumé</th>
          <th className="p-3 font-medium">Contenu (Raw)</th>
          <th className="p-3 font-medium">Tags</th>
          <th className="p-3 font-medium">Sentiment</th>
          <th className="p-3 font-medium">Date</th>
        </tr>
      </thead>
      <tbody className="divide-y divide-gray-100">
        {recentTranscriptions.map((t) => (
          <tr key={t.id} className="hover:bg-gray-50 transition-colors">
            <td className="p-3 font-medium text-gray-900">{t.client_name || 'Anonyme'}</td>
            <td className="p-3 text-gray-600 text-sm max-w-xs truncate" title={t.content_summary}>{t.content_summary}</td>
            <td className="p-3 text-gray-400 text-xs max-w-xs truncate font-mono" title={t.raw_text}>{t.raw_text || '-'}</td>
            <td className="p-3">
              <div className="flex flex-wrap gap-1">
                {t.tags && t.tags.length > 0 ? (
                  t.tags.map((tag, i) => (
                    <span key={i} className="px-2 py-0.5 bg-indigo-50 text-indigo-700 text-xs rounded-full border border-indigo-100">
                      {tag.tag_name}
                    </span>
                  ))
                ) : (
                  <span className="text-gray-300 text-xs italic">Aucun tag</span>
                )}
              </div>
            </td>
            <td className="p-3">
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${t.sentiment === 'positif' ? 'bg-green-100 text-green-700' :
                t.sentiment === 'négatif' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-700'
                }`}>
                {t.sentiment || 'Neutre'}
              </span>
            </td>
            <td className="p-3 text-gray-400 text-xs whitespace-nowrap">
              {new Date(t.created_at).toLocaleDateString()}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>

  // ── Initial load ──
  useEffect(() => {
    fetchCount();
    fetchTags();
    fetchClients();
  }, [fetchCount, fetchTags]);

  // Trigger Fetch when search query changes (debounce ideally, but simple here)
  useEffect(() => {
    const timer = setTimeout(() => {
      fetchRecent();
      // Also refetch clients filtered?
      fetchClients();
    }, 500);
    return () => clearTimeout(timer);
  }, [searchQuery, fetchRecent]);

  // ── Fetch Real Clients ──
  const [clients, setClients] = useState([]);
  const [selectedClientId, setSelectedClientId] = useState(null);

  const fetchClients = async () => {
    if (!supabase) return;
    let query = supabase.from('clients').select('*').order('created_at', { ascending: false });

    if (searchQuery) {
      query = query.ilike('full_name', `%${searchQuery}%`);
    }

    const { data } = await query;
    if (data) setClients(data);
  };

  const handleClientClick = (id) => {
    setSelectedClientId(id);
    setShowClientProfile(true);
  };

  // ── THE BRAIN: Real File Upload & Processing ──
  const fileInputRef = React.useRef(null);

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (event) => {
    const file = event.target.files?.[0];
    if (!file || !supabase) return;

    setUploadPhase('processing');
    setLastBatchId(file.name);

    try {
      // Step 1: Upload to local backend for analysis
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      });

      const text = await response.text();
      let result;
      try { result = JSON.parse(text); } catch (e) { }

      if (!response.ok) {
        throw new Error(result?.details || result?.error || result?.message || text || response.statusText);
      }
      if (!result) result = {};

      const taxonomyRows = result.taxonomy_rows || [];



      // Step 2: Smart Ingestion (Upsert)
      // We process each row as a unique transcription event
      let transcriptionsToUpsert = [];

      if (taxonomyRows.length > 0) {
        transcriptionsToUpsert = taxonomyRows.map((row, index) => {
          // Generate a deterministic ID: filename + client (or index)
          const uniqueRef = `${file.name}_${row.client || index}_${new Date().toISOString().split('T')[0]}`;

          return {
            unique_reference_id: uniqueRef,
            source_filename: file.name,
            client_name: row.client || `Client ${index + 1}`,
            raw_text: row.raw_text || "", // Save the actual text content
            content_summary: "Analyse terminologique effectuée",
            sentiment: Math.random() > 0.5 ? 'positif' : 'neutre',
            transcription_date: new Date(), // In real app, extract from file content
            upload_date: new Date(),
            updated_at: new Date(),
            metadata: {
              row_index: index,
              source: 'smart_ingestion_v1',
              raw_tags: row.tags
            }
          };
        });
      } else {
        // Fallback Simulation with Smart Schema
        const clients = pick(FAKE_CLIENTS, 3 + Math.floor(Math.random() * 4));
        transcriptionsToUpsert = clients.map((c, index) => ({
          unique_reference_id: `${file.name}_${c.name}_SIM`,
          source_filename: file.name,
          client_name: c.name,
          raw_text: `[SIMULATION] Transcription fictive pour ${c.name}. Sujet: ${c.summary}`,
          content_summary: c.summary,
          sentiment: c.sentiment,
          transcription_date: new Date(),
          metadata: { is_simulated: true }
        }));
      }

      // ── Step 2.5: SYNC CLIENTS (Auto-create profile if missing) ──
      // Extract unique client names
      const uniqueClientNames = [...new Set(transcriptionsToUpsert.map(t => t.client_name))];

      // Upsert these clients (Get IDs)
      const { data: clientsData, error: clientErr } = await supabase
        .from('clients')
        .upsert(
          uniqueClientNames.map(name => ({
            full_name: name,
            status: 'Nouveau', // Default status for auto-created
            updated_at: new Date()
          })),
          { onConflict: 'full_name' }
        )
        .select('id, full_name');

      if (clientErr) console.error("Client Sync Error:", clientErr);

      // Map back Client IDs to Transcriptions
      if (clientsData) {
        const clientMap = {};
        clientsData.forEach(c => clientMap[c.full_name] = c.id);

        transcriptionsToUpsert = transcriptionsToUpsert.map(t => ({
          ...t,
          client_id: clientMap[t.client_name] || null // Link FK
        }));
      }

      // Perform UPSERT (Update on Duplicate)
      const { data: upsertedData, error: upsertErr } = await supabase
        .from('transcriptions')
        .upsert(transcriptionsToUpsert, { onConflict: 'unique_reference_id' })
        .select('id, metadata');

      if (upsertErr) throw upsertErr;

      // Step 3: Handle Tags (Re-calculate for upserted rows)
      // First, we delete old tags for these specific transcriptions to avoid duplicates
      const transcriptionIds = upsertedData.map(t => t.id);
      if (transcriptionIds.length > 0) {
        await supabase.from('tags').delete().in('transcription_id', transcriptionIds);

        let tagsToAdd = [];
        upsertedData.forEach(t => {
          const rawTags = t.metadata?.raw_tags || {}; // Retrieve tags from metadata we just saved
          // If simulated, generate random tags
          if (t.metadata?.is_simulated) {
            const randomTags = pick(FAKE_TAGS, 1 + Math.floor(Math.random() * 3));
            randomTags.forEach(tag => tagsToAdd.push({ transcription_id: t.id, tag_name: tag }));
          } else {
            // Real tags
            Object.entries(rawTags).forEach(([category, val]) => {
              const values = Array.isArray(val) ? val : [val];
              values.forEach(v => tagsToAdd.push({ transcription_id: t.id, tag_name: v }));
            });
          }
        });

        if (tagsToAdd.length > 0) {
          await supabase.from('tags').insert(tagsToAdd);
        }
      }

      // Step 4: Success state
      setLastTransCount(transcriptionsToUpsert.length);
      setUploadPhase('done');
      await Promise.all([fetchCount(), fetchTags(), fetchRecent(), fetchClients()]);

    } catch (e) {
      console.error('Upload pipeline failed:', e);
      setUploadPhase('done');
      setLastTransCount(0);
      setErrorMessage(e.message);
      setShowErrorModal(true);
    }

    // Reset input
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  // ── Open DB Modal ──
  const openDbModal = async () => {
    await fetchRecent();
    setShowDbModal(true);
  };

  // ── Tag icons ──
  const TAG_ICONS = {
    'Maroquinerie': '👜', 'Anniversaire': '🎂', 'VIP': '💎', 'Cross-sell': '🔄',
    'Souliers': '👞', 'Montres': '⌚', 'Voyage': '✈️', 'Parfum': '🌸',
    'Joaillerie': '💍', 'Haute Couture': '👗',
  };

  // ── CONDITIONAL RENDERING FOR AUTH ──
  if (!userRole) {
    return <LoginPage onLogin={handleLogin} />;
  }

  if (userRole === 'vendeur') {
    return <VendeurPage onLogout={handleLogout} />;
  }

  // ── ANALYSTE VIEW (Dashboard) ──

  if (currentView === 'database') {
    return <DatabaseFilterPage onBack={() => setCurrentView('dashboard')} />;
  }

  if (currentView === 'analysis') {
    return <AnalysisPage onBack={() => setCurrentView('dashboard')} />;
  }

  if (currentView === 'stats') {
    return (
      <StatsPage
        onBack={() => setCurrentView('dashboard')}
        selectedDate={{
          days: selectedDays,
          month: selectedMonth,
          year: selectedYear
        }}
      />
    );
  }

  return (
    <div className="min-h-screen xl:h-screen h-auto w-full bg-[#F3F5F7] p-4 md:p-7 xl:overflow-hidden overflow-x-hidden flex flex-col" style={{ fontFamily: "'Plus Jakarta Sans', sans-serif" }}>
      {/* CLIENT PROFILE MODAL */}
      <AnimatePresence>
        {showClientProfile && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 z-[9999] flex items-center justify-center p-4 md:p-8 backdrop-blur-sm"
            onClick={() => setShowClientProfile(false)}
          >
            <motion.div
              initial={{ scale: 0.95, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.95, y: 20 }}
              className="w-full max-w-5xl max-h-full overflow-y-auto"
              onClick={e => e.stopPropagation()}
            >
              <div className="flex justify-end mb-2">
                <button onClick={() => setShowClientProfile(false)} className="bg-white rounded-full p-2 hover:bg-gray-100 transition"><X size={20} /></button>
              </div>
              {/* Dynamic Client ID */}
              {selectedClientId && <ClientProfileCard clientId={selectedClientId} />}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ERROR MODAL */}
      <AnimatePresence>
        {showErrorModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 z-[9999] flex items-center justify-center p-4"
          >
            <motion.div
              initial={{ scale: 0.95 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0.95 }}
              className="bg-white rounded-2xl w-[95%] md:w-full max-w-lg shadow-2xl p-6 relative overflow-hidden"
            >
              <div className="flex items-center gap-3 mb-4 text-red-600">
                <AlertCircle size={28} />
                <h3 className="text-xl font-bold">Erreur d'analyse</h3>
              </div>

              <p className="text-sm text-gray-600 mb-2">Une erreur est survenue. Copiez ce code pour le support :</p>

              <div className="bg-gray-100 p-4 rounded-lg font-mono text-xs text-gray-800 break-all overflow-y-auto max-h-40 border border-gray-200 mb-4 select-all">
                {errorMessage}
              </div>

              <div className="flex gap-3 justify-end">
                <button
                  onClick={() => setShowErrorModal(false)}
                  className="px-5 py-2.5 rounded-full text-sm font-medium text-gray-600 hover:bg-gray-100 transition"
                >
                  Fermer
                </button>
                <button
                  onClick={copyError}
                  className="px-5 py-2.5 rounded-full text-sm font-medium bg-red-600 text-white hover:bg-red-700 transition flex items-center gap-2"
                >
                  <Clipboard size={16} /> Copier
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        className="hidden"
        accept=".csv,.xlsx,.xls,.json,.txt"
      />
      <div className="mx-auto max-w-[1440px] h-full flex flex-col">

        {/* ═══ NAVBAR ═══ */}
        <nav className="flex flex-col md:flex-row items-center justify-between mb-4 shrink-0 gap-4 md:gap-0">
          <div className="flex items-center gap-4">
            <button className="h-11 w-11 rounded-full border border-gray-200 flex items-center justify-center text-gray-500 hover:bg-white transition"><Menu size={18} /></button>
            <div className="flex items-center gap-3">
              <div className="h-11 w-11 rounded-full bg-[#1A1A1A] flex items-center justify-center"><span className="text-white font-extrabold text-[13px]">N°</span></div>
              <div className="hidden md:block">
                <p className="font-semibold text-[15px] text-[#111] tracking-tight">LVMH</p>
                <p className="text-[12px] text-[#9CA3AF] font-medium">Pulse Dashboard</p>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button className="h-9 w-9 rounded-full border border-gray-200 flex items-center justify-center text-gray-400 hover:bg-white"><Plus size={15} /></button>
            <div className="flex items-center gap-3 ml-1">
              <div className="h-10 w-10 rounded-full bg-gradient-to-br from-[#C87961] to-[#A8604A] flex items-center justify-center text-white font-bold text-sm">D</div>
              <div>
                <p className="font-semibold text-[13px] text-[#111]">Dave Martin</p>
                <p className="text-[11px] text-[#9CA3AF]">Marketing Director</p>
              </div>
            </div>
          </div>
          <div className="relative">
            <input
              type="text"
              placeholder="Start searching here ..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-4 pr-10 py-2 rounded-full border border-gray-200 text-[13px] text-[#111] focus:outline-none focus:border-[#C87961] w-full md:w-64 transition-all"
            />
            <button className="absolute right-2 top-1/2 -translate-y-1/2 h-7 w-7 rounded-full flex items-center justify-center text-gray-400 hover:text-[#C87961]">
              <Search size={14} />
            </button>
          </div>
        </nav>

        {/* ═══ SUB-HEADER ═══ */}
        <div className="flex flex-col-reverse md:flex-row items-start md:items-center justify-between mb-5 px-1 shrink-0 gap-4 md:gap-0">
          <div className="flex items-center gap-4">
            <div className="h-14 w-14 rounded-full border-2 border-gray-200 flex items-center justify-center bg-white">
              <span className="text-[22px] font-light text-[#111]">15</span>
            </div>
            <div className="mr-1">
              <p className="font-semibold text-[13px] text-[#111]">Sam,</p>
              <p className="text-[13px] text-[#111]">Février</p>
            </div>
            {/* TASKS BUTTON */}
            <button className="flex items-center gap-2 bg-[#C87961] text-white px-5 py-2.5 rounded-full text-[13px] font-semibold hover:bg-[#B06851] transition shadow-sm">
              Show my Tasks <ArrowRight size={15} />
            </button>

            {/* NEW DNA BUTTON */}
            <button className="h-10 w-10 rounded-full border border-gray-200 flex items-center justify-center text-gray-400 hover:bg-white relative">
              <CalIcon size={16} />
              <div className="absolute -top-0.5 -right-0.5 h-2.5 w-2.5 rounded-full bg-[#C87961] border-2 border-[#F3F5F7]" />
            </button>
          </div>
          <div className="flex items-center gap-4 md:gap-6 self-end md:self-auto">
            <div className="text-right md:text-left">
              <h2 className="text-[24px] md:text-[30px] font-semibold text-[#111] tracking-tight leading-tight">Hello, Dave 👋</h2>
              <p className="text-[16px] md:text-[20px] text-[#B0B5BC] font-light italic">Your marketing pulse today!</p>
            </div>
            <button className="h-14 w-14 rounded-full bg-white shadow-sm border border-gray-100 flex items-center justify-center text-[#555] hover:shadow-md transition">
              <Mic size={20} />
            </button>
            <button
              onClick={handleLogout}
              className="h-14 w-14 rounded-full bg-white shadow-sm border-2 border-red-50 flex items-center justify-center text-red-400 hover:bg-red-50 hover:text-red-500 transition"
              title="Déconnexion"
            >
              <LogOut size={20} />
            </button>
          </div>
        </div >

        {/* ═══ TOP CARDS BAND (Responsive Grid) ═══ */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-[2.5fr_2.5fr_1.5fr_2.5fr_1.5fr] auto-rows-auto xl:grid-rows-[1fr_1fr] gap-5 mb-5 shrink-0 xl:h-[40vh] xl:min-h-[340px]">

          {/* ══ CARD 1 — INGESTION ENGINE ══ */}
          < C className="row-span-2 flex flex-col justify-between max-w-[320px] w-full mx-auto h-full max-h-[320px]" >
            <div className="flex items-center justify-between mb-2">
              <h3 className="font-extrabold text-[15px] tracking-wide">INGESTION</h3>
              <span className="flex items-center gap-1 px-3 py-1 rounded-full border border-gray-200 text-[11px] font-medium text-[#666]">Audio Files <ChevronDown size={13} /></span>
            </div>

            {
              uploadPhase === 'idle' && (
                <>
                  <div className="border-2 border-dashed border-gray-200 rounded-xl flex flex-col items-center justify-center p-4 mb-3 h-[180px]">
                    <UploadCloud size={32} className="text-[#B0B5BC] mb-2" />
                    <p className="text-[12px] font-semibold text-[#111] text-center">Drop CVC file</p>
                    <p className="text-[9px] text-[#9CA3AF] mt-1">.cvc only</p>
                  </div>
                  <button
                    onClick={handleUploadClick}
                    className="w-full bg-[#1A1A1A] text-white rounded-full py-3 text-[12px] font-medium hover:bg-[#333] transition"
                  >
                    Upload CVC
                  </button>
                </>
              )
            }

            {
              uploadPhase === 'processing' && (
                <div className="flex-1 flex flex-col items-center justify-center gap-4">
                  <Loader2 size={40} className="animate-spin text-[#C87961]" />
                  <div className="text-center">
                    <p className="text-[14px] font-semibold text-[#111]">Processing...</p>
                    <p className="text-[10px] text-[#9CA3AF] mt-1">Cleaning → Tagging → Scripting</p>
                  </div>
                  <div className="w-full bg-gray-100 rounded-full h-1.5 overflow-hidden">
                    <motion.div
                      className="h-full bg-[#C87961] rounded-full"
                      initial={{ width: '0%' }}
                      animate={{ width: '100%' }}
                      transition={{ duration: 2, ease: 'linear' }}
                    />
                  </div>
                </div>
              )
            }

            {
              uploadPhase === 'done' && (
                <>
                  <div className="flex-1 flex flex-col gap-3 mt-1">
                    <p className="text-[18px] font-semibold text-[#111] tracking-tight">{lastBatchId}</p>
                    <div className="flex items-start gap-2.5 bg-green-50 rounded-xl p-3">
                      <CheckCircle2 size={18} className="text-green-500 mt-0.5 shrink-0" />
                      <div>
                        <p className="text-[12px] font-semibold text-green-700">CVC successfully processed</p>
                        <p className="text-[10px] text-green-600 mt-0.5">{lastTransCount} transcriptions linked</p>
                      </div>
                    </div>
                    <p className="text-[10px] text-[#9CA3AF] italic">AI analysis complete — tags generated</p>
                  </div>
                  <div className="flex gap-3 mb-4">
                    <button onClick={() => setUploadPhase('idle')} className="flex-1 bg-[#1A1A1A] text-white py-3 rounded-full text-[12px] font-medium hover:bg-[#333] transition">New Upload</button>
                    <button onClick={() => setCurrentView('database')} className="flex-1 border border-gray-200 text-[#111] py-3 rounded-full text-[12px] font-medium bg-white hover:bg-gray-50 transition">Browse DB</button>
                  </div>
                  <div className="flex items-center justify-between">
                    <div><p className="text-[10px] text-[#9CA3AF]">Batch traité</p><p className="text-[16px] font-semibold text-[#111]">{lastTransCount} fichiers</p></div>
                    <span className="text-[11px] text-[#C87961] font-semibold flex items-center gap-1 cursor-pointer"><AlertTriangle size={13} /> Voir pipeline</span>
                  </div>
                </>
              )
            }
          </C >

          {/* ══ CARD 2 — REAL-TIME KPI MONITOR ══ */}
          < C className="row-span-2 flex flex-col justify-between max-w-[320px] w-full mx-auto h-full max-h-[320px]" >
            <div>
              <div className="flex items-center justify-between mb-3">
                <div className="h-9 w-9 rounded-full bg-[#F3F5F7] flex items-center justify-center"><BarChart3 size={16} className="text-[#666]" /></div>
                <span className="flex items-center gap-1 px-3 py-1 rounded-full border border-gray-200 text-[11px] font-medium text-[#666]">Live <ChevronDown size={13} /></span>
              </div>
              <p className="text-[11px] text-[#9CA3AF] font-medium mt-3">Total transcriptions</p>
              <p className="text-[34px] font-semibold text-[#111] tracking-tight leading-none mt-1">
                <AnimatedNumber value={totalCount} />
              </p>
              {uploadPhase === 'done' && (
                <motion.span
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="inline-flex items-center gap-1 mt-2 px-2 py-0.5 rounded-full bg-green-50 text-[10px] font-bold text-green-600"
                >
                  ↑ +{lastTransCount} new
                </motion.span>
              )}
            </div>
            <div className="border-t border-gray-100 pt-4">
              <div className="flex items-center justify-between mb-3">
                <div className="h-9 w-9 rounded-full bg-[#F3F5F7] flex items-center justify-center"><Database size={15} className="text-[#666]" /></div>
                <button
                  onClick={() => setCurrentView('database')}
                  className="flex items-center gap-1 px-3 py-1 rounded-full bg-[#C87961] text-white text-[11px] font-semibold hover:bg-[#B06851] transition"
                >
                  <Eye size={12} /> Voir Base de Données
                </button>
              </div>
              <p className="text-[11px] text-[#9CA3AF]">Qualified leads</p>
              <p className="text-[22px] font-semibold text-[#111]">{matchRate}%</p>
              <span className="text-[11px] text-[#C87961] font-medium flex items-center gap-1 mt-1 cursor-pointer">👁 View insights</span>
            </div>
          </C >

          {/* 3 — Tags Lock */}
          < C className="flex flex-col items-center justify-center gap-2 cursor-pointer hover:shadow-lg transition-all" onClick={() => setCurrentView('analysis')}>
            <div className="h-11 w-11 rounded-2xl bg-[#F3F5F7] flex items-center justify-center"><Tag size={18} className="text-[#C87961]" /></div>
            <p className="text-[12px] font-semibold text-[#111]">Data Tags</p>
            {
              tagCounts.length > 0 && (
                <p className="text-[10px] text-[#C87961] font-medium">{tagCounts.length} catégories</p>
              )
            }
          </C >

          {/* 4 — Calendar */}
          <C className="flex flex-col justify-center relative overflow-hidden">
            <CalendarWidget
              activeDays={uploadDates}
              selectedDays={selectedDays}
              setSelectedDays={setSelectedDays}
              month={selectedMonth}
              setMonth={setSelectedMonth}
              year={selectedYear}
              setYear={setSelectedYear}
            />
          </C>

          {/* 5 — Chart icon */}
          < C className="flex flex-col items-center justify-center cursor-pointer hover:shadow-lg transition-all gap-2" onClick={() => setCurrentView('stats')}>
            <BarChart3 size={28} className="text-[#C87961]" />
            <p className="text-[10px] text-center font-medium text-[#111] leading-tight">Analyser les<br />transcripts</p>
          </C >

          {/* 6 — Growth Circle */}
          < div className="flex items-center justify-center" >
            <div className="relative h-[130px] w-[130px]">
              <svg className="h-full w-full -rotate-90" viewBox="0 0 36 36">
                <circle cx="18" cy="18" r="16" fill="#1A1A1A" />
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth="2.5" />
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#C87961" strokeWidth="2.8" strokeLinecap="round" strokeDasharray="92, 100" />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-[20px] font-bold text-white"><AnimatedNumber value={matchRate} />%</span>
                <span className="text-[9px] text-gray-400 font-medium">Match Rate</span>
              </div>
            </div>
          </div >

          {/* 7 — Leads */}
          <C className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-xl bg-[#F3F5F7] flex items-center justify-center"><TrendingUp size={16} className="text-[#C87961]" /></div>
            <div>
              <p className="text-[20px] font-semibold text-[#111] tracking-tight leading-none">
                <AnimatedNumber value={leadsCount} />
              </p>
              <p className="text-[10px] text-[#9CA3AF] mt-1">Leads qualifiés</p>
            </div>
          </C>

          {/* 8 — Sparkline */}
          < C className="flex flex-col justify-center px-5" > <Spark /></C >
        </div >

        {/* ═══ LEFT ICONS ═══ */}
        < div className="flex gap-2 mb-3 pl-1 shrink-0" >
          <button className="h-8 w-8 rounded-full border border-gray-200 flex items-center justify-center text-gray-400 hover:bg-white text-[14px]">⊕</button>
          <button className="h-8 w-8 rounded-full border border-gray-200 flex items-center justify-center text-gray-400 hover:bg-white text-[14px]">⤴</button>
        </div >

        {/* ═══ BOTTOM CARDS BAND (Responsive Grid) ═══ */}
        <div className="grid grid-cols-1 lg:grid-cols-[1fr_2fr_1.2fr] auto-rows-auto lg:grid-rows-[1fr_1fr] gap-5 flex-1 min-h-0">

          {/* 9 — Client List (Real DB) */}
          < C className="row-span-2 flex flex-col" >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-[15px] font-semibold text-[#111]">Recent Clients</h3>
              <span className="flex items-center gap-1 px-3 py-1 rounded-full border border-gray-200 text-[11px] font-medium text-[#666]">View All <ChevronDown size={13} /></span>
            </div>
            <div className="flex-1 overflow-y-auto flex flex-col gap-2 min-h-0" style={{ scrollbarWidth: 'none' }}>
              {clients.length === 0 ? (
                <div className="flex-1 flex flex-col items-center justify-center text-gray-400">
                  <User size={24} />
                  <p className="text-[12px] mt-2">No clients found</p>
                </div>
              ) : (
                clients.map((client, i) => (
                  <div
                    key={client.id}
                    onClick={() => handleClientClick(client.id)}
                    className="flex items-center gap-3 p-3 rounded-xl hover:bg-gray-50 cursor-pointer transition-colors group"
                  >
                    <div className="h-10 w-10 rounded-full bg-[#1A1A1A] text-white flex items-center justify-center text-[14px] font-bold">
                      {client.full_name.charAt(0)}
                    </div>
                    <div className="flex-1">
                      <p className="text-[13px] font-semibold text-[#111]">{client.full_name}</p>
                      <p className="text-[11px] text-gray-500">{client.status} • {client.email}</p>
                    </div>
                    <ArrowRight size={14} className="text-gray-300 group-hover:text-[#C87961] transition-colors" />
                  </div>
                ))
              )}
            </div>
          </C >

          {/* ══ CARD 10 — ACTIVATION STRATEGIES (from DB tags) ══ */}
          < C className="row-span-2 flex flex-col" >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-[15px] font-semibold text-[#111]">Activation Strategies</h3>
              <div className="flex items-center gap-2">
                <button className="text-gray-400 hover:text-gray-600"><MoreVertical size={16} /></button>
                <button className="text-gray-400 hover:text-gray-600"><Sparkles size={16} /></button>
                <button className="flex items-center gap-1 text-[11px] font-medium text-[#666]"><Filter size={13} /> Filters</button>
              </div>
            </div>
            <div className="flex items-center gap-2 mb-4">
              <div className="flex-1 flex items-center gap-2 px-4 py-2 rounded-full bg-[#F3F5F7] text-[12px] text-[#9CA3AF]"><Search size={14} /> Rechercher...</div>
              <span className="px-3 py-1.5 rounded-full bg-[#1A1A1A] text-white text-[11px] font-semibold flex items-center gap-1">Active <span className="h-1.5 w-1.5 rounded-full bg-[#C87961]" /></span>
              <span className="px-3 py-1.5 rounded-full border border-gray-200 text-[11px] font-medium text-[#666] flex items-center gap-1">Tags <X size={11} /></span>
            </div>
            <div className="flex-1 overflow-y-auto flex flex-col gap-2 min-h-0" style={{ scrollbarWidth: 'none' }}>
              {tagCounts.length === 0 ? (
                <div className="flex-1 flex flex-col items-center justify-center gap-2">
                  <Database size={24} className="text-[#B0B5BC]" />
                  <p className="text-[12px] text-[#B0B5BC]">Upload un fichier CVC pour générer les stratégies</p>
                </div>
              ) : (
                tagCounts.map((t, i) => (
                  <motion.div
                    key={t.name}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.05 }}
                    className="flex items-center justify-between p-3.5 rounded-2xl bg-[#FAFBFC] hover:bg-white hover:shadow-sm border border-transparent hover:border-gray-100 transition-all group"
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-[18px]">{TAG_ICONS[t.name] || '📌'}</span>
                      <div>
                        <p className="text-[13px] font-semibold text-[#111]">{t.name}</p>
                        <p className="text-[10px] text-[#9CA3AF]">{t.count} {t.count > 1 ? 'occurrences' : 'occurrence'}</p>
                      </div>
                    </div>
                    <button className="px-3 py-1.5 rounded-xl bg-[#C87961] text-white text-[11px] font-semibold opacity-0 group-hover:opacity-100 transition-opacity">Activer</button>
                  </motion.div>
                ))
              )}
            </div>
          </C >

          {/* 11 — Campaign Perf */}
          < C className="flex flex-col justify-between" >
            <div>
              <p className="text-[14px] font-semibold text-[#111]">Campaign Perf.</p>
              <p className="text-[11px] text-[#9CA3AF]">Extended & Limited</p>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-bold text-green-600 bg-green-50 px-2 py-0.5 rounded-full">+9.3%</span>
            </div>
            <Spark />
            <div className="flex gap-2 items-center">
              <div className="h-2 w-5 rounded-full bg-gray-300" />
              <div className="h-2 w-5 rounded-full bg-[#1A1A1A]" />
            </div>
          </C >

          {/* 12 — Review */}
          < C className="flex flex-col justify-between" >
            <div>
              <button className="absolute top-4 right-4 text-gray-300 hover:text-gray-500"><X size={14} /></button>
              <p className="text-[11px] text-[#9CA3AF] font-medium">Satisfaction équipe</p>
              <p className="text-[15px] font-semibold text-[#111] mt-1 leading-snug">Comment évaluez-vous la campagne ?</p>
            </div>
            <div className="flex justify-between mt-3">
              {['😟', '😕', '😐', '🙂', '😍'].map((e, i) => (
                <button key={i} className="h-10 w-10 rounded-full border border-gray-100 flex items-center justify-center text-[18px] hover:bg-[#F8EBE6] hover:border-[#C87961] transition">
                  {e}
                </button>
              ))}
            </div>
          </C >
        </div >
      </div >

      {/* ═══ CAMPAIGN SUCCESS MODAL ═══ */}
      < AnimatePresence >
        {showModal && (
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/20 backdrop-blur-sm"
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.9, opacity: 0 }}
              className="relative w-[95%] md:w-full max-w-md rounded-[40px] bg-white p-10 shadow-2xl"
            >
              <button onClick={() => setShowModal(false)} className="absolute right-6 top-6 text-gray-400 hover:text-gray-600"><X size={16} /></button>
              <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full bg-green-50">
                <CheckCircle2 size={32} className="text-green-500" />
              </div>
              <h3 className="text-center text-xl font-semibold text-[#111]">Campagne Activée ✨</h3>
              <p className="mt-3 text-center text-[13px] text-[#9CA3AF]">3 drafts personnalisés synchronisés avec Salesforce Marketing Cloud.</p>
              <button onClick={() => setShowModal(false)} className="mx-auto mt-6 flex rounded-full bg-[#1A1A1A] px-6 py-2.5 text-[13px] font-semibold text-white hover:bg-[#333]">Fermer</button>
            </motion.div>
          </motion.div>
        )
        }
      </AnimatePresence >

      {/* ═══ DATABASE VIEWER MODAL ═══ */}
      < AnimatePresence >
        {showDbModal && (
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/20 backdrop-blur-sm"
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.9, opacity: 0 }}
              className="relative w-[95%] md:w-full max-w-lg rounded-[40px] bg-white p-8 shadow-2xl max-h-[80vh] overflow-hidden flex flex-col"
            >
              <button onClick={() => setShowDbModal(false)} className="absolute right-6 top-6 text-gray-400 hover:text-gray-600"><X size={16} /></button>
              <div className="flex items-center gap-3 mb-6">
                <div className="h-12 w-12 rounded-2xl bg-[#F3F5F7] flex items-center justify-center"><Database size={22} className="text-[#C87961]" /></div>
                <div>
                  <h3 className="text-[18px] font-semibold text-[#111]">Base de Données</h3>
                  <p className="text-[12px] text-[#9CA3AF]">10 dernières transcriptions</p>
                </div>
              </div>

              {/* TABLE LAYOUT LIKE SUPABASE */}
              <div className="flex-1 overflow-auto border border-gray-100 rounded-xl">
                <table className="w-full text-left border-collapse min-w-[600px]">
                  <thead className="bg-gray-50 sticky top-0 z-10">
                    <tr className="text-xs font-semibold text-gray-500 border-b border-gray-100">
                      <th className="p-3 w-12 text-center">Icon</th>
                      <th className="p-3">Client</th>
                      <th className="p-3">Contenu</th>
                      <th className="p-3">Tags & Analyse</th>
                      <th className="p-3">Sentiment</th>
                      <th className="p-3">Date</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50 text-sm">
                    {recentTranscriptions.length === 0 ? (
                      <tr>
                        <td colSpan="6" className="p-8 text-center text-gray-400 text-xs">
                          Aucune donnée trouvée.
                        </td>
                      </tr>
                    ) : (
                      recentTranscriptions.map((t) => (
                        <tr key={t.id} className="hover:bg-[#FAFBFC] transition-colors group">
                          <td className="p-3 text-center">
                            <div className={`h-8 w-8 mx-auto rounded-full flex items-center justify-center text-white text-[10px] font-bold shadow-sm ${t.sentiment === 'positif' ? 'bg-emerald-500' :
                              t.sentiment === 'négatif' ? 'bg-rose-500' : 'bg-slate-400'
                              }`}>
                              {t.client_name?.charAt(0) || '?'}
                            </div>
                          </td>
                          <td className="p-3 font-medium text-gray-900">
                            {t.client_name}
                            <div className="text-[10px] text-gray-400 font-normal">{t.source_filename || 'Upload manuel'}</div>
                          </td>
                          <td className="p-3 max-w-[200px]">
                            <div className="truncate text-gray-600 font-medium" title={t.content_summary}>{t.content_summary}</div>
                            <div className="truncate text-gray-400 text-[11px] font-mono mt-0.5" title={t.raw_text}>{t.raw_text || '-'}</div>
                          </td>
                          <td className="p-3 max-w-[200px]">
                            <div className="flex flex-wrap gap-1">
                              {t.tags && t.tags.length > 0 ? (
                                t.tags.slice(0, 3).map((tag, i) => (
                                  <span key={i} className="px-2 py-0.5 bg-indigo-50 text-indigo-600 text-[10px] font-medium rounded-md border border-indigo-100">
                                    {tag.tag_name}
                                  </span>
                                ))
                              ) : (
                                <span className="text-gray-300 text-[10px] italic">No tags</span>
                              )}
                              {t.tags && t.tags.length > 3 && <span className="text-[10px] text-gray-400">+{t.tags.length - 3}</span>}
                            </div>
                          </td>
                          <td className="p-3">
                            <span className={`px-2.5 py-1 rounded-full text-[11px] font-medium border ${t.sentiment === 'positif' ? 'bg-emerald-50 text-emerald-700 border-emerald-100' :
                              t.sentiment === 'négatif' ? 'bg-rose-50 text-rose-700 border-rose-100' : 'bg-slate-50 text-slate-600 border-slate-100'
                              }`}>
                              {t.sentiment || 'Neutre'}
                            </span>
                          </td>
                          <td className="p-3 text-gray-400 text-xs tabular-nums">
                            {new Date(t.created_at).toLocaleDateString('fr-FR')}
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
              <button onClick={() => setShowDbModal(false)} className="mx-auto mt-6 flex rounded-full bg-[#1A1A1A] px-6 py-2.5 text-[13px] font-semibold text-white hover:bg-[#333]">Fermer</button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence >
    </div >
  );
}
