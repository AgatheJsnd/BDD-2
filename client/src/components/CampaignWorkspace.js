import React, { useState, useEffect } from 'react';
import {
    X, Filter, Search, Users, Calendar, Send, CheckCircle2,
    AlertTriangle, Clock, ChevronDown, Sparkles, ShieldCheck, Ban
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { supabase } from '../supabaseClient';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

// ── LUXURY UI CONSTANTS ──
const SUBSCRIPTION_FILTERS = [
    { id: 'all', label: 'Tout' },
    { id: 'email', label: 'Email' },
    { id: 'whatsapp', label: 'WhatsApp' }
];

export default function CampaignWorkspace({ isOpen, onClose, initialStrategy }) {
    const [loading, setLoading] = useState(true);
    const [audience, setAudience] = useState([]);
    const [filteredAudience, setFilteredAudience] = useState([]);
    const [selectedClients, setSelectedClients] = useState([]);

    // ── FILTERS V3 ──
    const [searchQuery, setSearchQuery] = useState(''); // Global Search
    const [dateRange, setDateRange] = useState('all'); // 'all', 'last_month', 'last_year', 'older'
    const [isAnalystMode, setIsAnalystMode] = useState(false); // PRIVACY TOGGLE

    // Pre-fill search based on Strategy
    useEffect(() => {
        if (initialStrategy?.query) {
            setSearchQuery(initialStrategy.query);
            return;
        }

        // Fallbacks for older config (if any)
        if (initialStrategy?.id === 'PROFIL_VALEURS') setSearchQuery('Vegan');
        else if (initialStrategy?.id === 'INTERET_NICHE') setSearchQuery('Opéra');
        else if (initialStrategy?.id === 'PREDICTION_ACHAT') setSearchQuery('Investissement');
        else if (initialStrategy?.trigger) {
            const match = initialStrategy.trigger.match(/'([^']+)'/);
            if (match) setSearchQuery(match[1]);
            else setSearchQuery('');
        }
    }, [initialStrategy]);

    // ── DATA FETCHING ──
    const fetchAudience = async () => {
        setLoading(true);
        console.log("Fetching Audience V3...");

        try {
            // CALL RPC with QUERY (or empty for Global Search)
            const { data, error } = await supabase.rpc('deep_memory_search', {
                filter_value: searchQuery,
                filter_location: '',
                current_campaign_tag: initialStrategy?.id || 'GLOBAL_SEARCH'
            });

            if (error) throw error;

            const rawData = data || [];
            setAudience(rawData);

            // Auto-select Eligible by default
            const eligibleIds = rawData
                .filter(c => c.eligibility_status === 'Eligible')
                .map(c => c.client_id);

            setSelectedClients(eligibleIds);

        } catch (err) {
            console.error("Error fetching audience:", err);
            setAudience([]);
        } finally {
            setLoading(false);
        }
    };

    // Re-fetch when Search Query changes (Debounced ideally, but direct for MVP)
    useEffect(() => {
        if (isOpen) {
            const timer = setTimeout(fetchAudience, 500); // 500ms debounce
            return () => clearTimeout(timer);
        }
    }, [isOpen, searchQuery]);

    // ── CLIENT-SIDE FILTERING (Date, etc.) ──
    useEffect(() => {
        let result = audience;

        // Date Range Filter (on Original Event Date)
        if (dateRange !== 'all') {
            const now = new Date();
            result = result.filter(c => {
                if (!c.source_date) return false;
                const date = new Date(c.source_date);
                if (dateRange === 'last_month') return (now - date) < 30 * 24 * 60 * 60 * 1000;
                if (dateRange === 'last_year') return (now - date) < 365 * 24 * 60 * 60 * 1000;
                return true;
            });
        }

        setFilteredAudience(result);
    }, [audience, dateRange]);


    // ── LAUNCH LOGIC ──
    const handleLaunch = async () => {
        if (selectedClients.length === 0) return;

        const confirm = window.confirm(
            `CONFIRMATION D'ENVOI \n\n` +
            `Campagne : ${initialStrategy?.title || 'Campagne Manuelle'}\n` +
            `Cible : ${selectedClients.length} clients\n` +
            `Canal : Email (Défaut)\n\n` +
            `Confirmer l'envoi ?`
        );
        if (!confirm) return;

        try {
            // 1. Log in Campaign History
            const historyInserts = selectedClients.map(clientId => ({
                client_id: clientId,
                campaign_name: initialStrategy?.title || 'Campagne Manuelle',
                campaign_tag: initialStrategy?.id || 'MANUAL',
                channel: 'Email',
                status: 'Sent',
                metadata: {
                    query: searchQuery,
                    strategy_id: initialStrategy?.id
                }
            }));

            const { error: historyError } = await supabase.from('campaign_history').insert(historyInserts);
            if (historyError) throw historyError;

            // 2. Create Operational Tasks (Activations) for Sellers
            const deadlineDays = initialStrategy?.id === 'relance_client' ? 2 : 7;
            const deadlineDate = new Date();
            deadlineDate.setDate(deadlineDate.getDate() + deadlineDays);

            const activationInserts = selectedClients.map(clientId => ({
                client_id: clientId,
                action_type: initialStrategy?.title || 'Relance Générale',
                deadline: deadlineDate.toISOString(),
                channel: initialStrategy?.id === 'relance_client' ? 'Appel' : 'Email',
                status: 'Pending'
            }));

            const { error: activationError } = await supabase.from('activations').insert(activationInserts);
            if (activationError) console.error("Warning: Task creation failed", activationError);

            alert("✅ Campagne envoyée & Tâches créées pour les vendeurs.");
            onClose();

        } catch (err) {
            console.error("Error launching campaign:", err);
            alert("Erreur critique lors de l'envoi.");
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-[9999] bg-[#F7F7F5] text-[#1A1A1A] flex flex-col font-sans">

            {/* ── HEADER "LUXURY TECH" ── */}
            <header className="h-20 border-b border-gray-200 flex items-center justify-between px-8 bg-white shrink-0 shadow-sm z-10">
                <div className="flex items-center gap-6">
                    <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-full transition duration-300">
                        <X size={24} className="text-gray-400" />
                    </button>
                    <div>
                        <div className="flex items-center gap-3">
                            <h1 className="text-xl font-serif font-bold text-[#1A1A1A]">
                                {initialStrategy?.title || 'Campagne Manuelle'}
                            </h1>
                            <span className="px-3 py-1 rounded-full bg-[#FAFAFA] text-gray-500 text-[10px] font-bold border border-gray-200 tracking-widest uppercase">
                                DRAFT
                            </span>
                        </div>
                        <p className="text-xs text-gray-400 mt-1 font-medium tracking-wide">
                            CAMPAIGN MANAGER V3 • {filteredAudience.length} PROFILS IDENTIFIÉS
                        </p>
                    </div>
                </div>

                <div className="flex items-center gap-6">
                    <div className="text-right">
                        <div className="text-xs text-gray-400 font-medium">Audience Sélectionnée</div>
                        <div className="text-xl font-bold font-serif text-[#C87961]">{selectedClients.length}</div>
                    </div>
                    <button
                        onClick={handleLaunch}
                        disabled={selectedClients.length === 0}
                        className="px-8 py-3 bg-[#1A1A1A] text-white text-xs font-bold tracking-widest uppercase rounded-sm hover:bg-[#333] transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
                    >
                        Lancer l'Activation
                    </button>
                </div>
            </header>

            {/* ── SPLIT LAYOUT ── */}
            <div className="flex-1 flex overflow-hidden">

                {/* SIDEBAR: CONTROLS */}
                <aside className="w-[320px] border-r border-gray-200 bg-white p-8 flex flex-col gap-8 overflow-y-auto z-0">

                    {/* SEARCH */}
                    <div>
                        <h3 className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-4 flex items-center gap-2">
                            <Search size={12} /> Global Search
                        </h3>
                        <div className="relative group">
                            <input
                                type="text"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="w-full text-sm p-4 bg-[#FAFAFA] border border-gray-200 rounded-sm focus:border-[#C87961] focus:ring-0 outline-none transition-all placeholder-gray-400 font-medium"
                                placeholder="Rechercher un tag (ex: Vegan)..."
                            />
                            <div className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-300 group-focus-within:text-[#C87961] transition-colors">
                                <Sparkles size={16} />
                            </div>
                        </div>
                        <p className="text-[10px] text-gray-400 mt-2 leading-relaxed">
                            Scan de l'historique complet (Deep Memory). Tapez un mot-clé pour filtrer 100% de la base.
                        </p>
                    </div>

                    <div className="h-px bg-gray-100" />

                    {/* DATE RANGE */}
                    <div>
                        <h3 className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-4 flex items-center gap-2">
                            <Calendar size={12} /> Période d'Origine
                        </h3>
                        <div className="flex flex-col gap-2">
                            {[
                                { id: 'all', label: 'Tout l\'historique' },
                                { id: 'last_month', label: 'Dernier mois' },
                                { id: 'last_year', label: 'Cette année' }
                            ].map(opt => (
                                <button
                                    key={opt.id}
                                    onClick={() => setDateRange(opt.id)}
                                    className={`text-left px-4 py-3 rounded-sm text-xs font-medium transition-all border ${dateRange === opt.id
                                        ? 'bg-[#1A1A1A] text-white border-[#1A1A1A]'
                                        : 'bg-white text-gray-500 border-gray-200 hover:border-gray-300'
                                        }`}
                                >
                                    {opt.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    <div className="h-px bg-gray-100" />

                    {/* RGPD & ANTI-SPAM INFO */}
                    <div className="bg-[#F8F1EF] p-4 rounded-sm border border-[#E8D5CF]">
                        <h3 className="text-[10px] font-bold text-[#C87961] uppercase tracking-widest mb-2 flex items-center gap-2">
                            <ShieldCheck size={12} /> Privacy & Compliance
                        </h3>
                        <ul className="space-y-2">
                            <li className="flex items-center gap-2 text-[10px] text-[#A6644D] font-medium">
                                <CheckCircle2 size={12} /> Check "Opt-in Marketing"
                            </li>
                            <li className="flex items-center gap-2 text-[10px] text-[#A6644D] font-medium">
                                <CheckCircle2 size={12} /> Anti-Spam (60 jours)
                            </li>
                        </ul>

                        {/* ANALYST MODE TOGGLE */}
                        <div className="mt-4 pt-4 border-t border-[#E8D5CF]/50">
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-[10px] font-bold text-[#C87961] uppercase tracking-widest flex items-center gap-2">
                                    <Ban size={12} /> Analyst Mode
                                </span>
                                <button
                                    onClick={() => setIsAnalystMode(!isAnalystMode)}
                                    className={`w-8 h-4 rounded-full relative transition-colors ${isAnalystMode ? 'bg-[#C87961]' : 'bg-gray-300'
                                        }`}
                                >
                                    <div className={`absolute top-0.5 left-0.5 w-3 h-3 bg-white rounded-full transition-transform ${isAnalystMode ? 'translate-x-4' : 'translate-x-0'
                                        }`} />
                                </button>
                            </div>
                            <p className="text-[9px] text-gray-500 leading-tight">
                                Masquer les identités pour l'analyse (RGPD Compliant).
                            </p>
                        </div>
                    </div>

                </aside>

                {/* MAIN: DATA GRID */}
                <main className="flex-1 bg-[#FAFAFA] flex flex-col p-8 overflow-hidden">

                    <div className="bg-white border border-gray-200 rounded-sm shadow-sm flex-1 flex flex-col overflow-hidden">
                        {/* Table Header */}
                        <div className="h-12 border-b border-gray-100 bg-white flex items-center px-6">
                            <div className="w-10"></div>
                            <div className="flex-1 text-[10px] font-bold text-gray-400 uppercase tracking-widest">Client Identity</div>
                            <div className="w-48 text-[10px] font-bold text-gray-400 uppercase tracking-widest">Profiling Source</div>
                            <div className="w-32 text-[10px] font-bold text-gray-400 uppercase tracking-widest">Original Date</div>
                            <div className="w-32 text-[10px] font-bold text-gray-400 uppercase tracking-widest text-center">Status</div>
                        </div>

                        {/* Scrolling List */}
                        <div className="flex-1 overflow-y-auto">
                            {loading ? (
                                <div className="flex flex-col items-center justify-center h-full gap-4 opacity-50">
                                    <div className="animate-spin text-gray-300"><Sparkles size={32} /></div>
                                    <p className="text-xs text-gray-400 tracking-widest uppercase">Deep Memory Search...</p>
                                </div>
                            ) : (
                                <table className="w-full text-left border-collapse">
                                    <tbody className="divide-y divide-gray-50">
                                        {filteredAudience.map(client => {
                                            const isEligible = client.eligibility_status === 'Eligible';
                                            const isOptIn = client.opt_in !== false; // assume true if null
                                            const date = client.source_date ? new Date(client.source_date) : null;

                                            const toggleSelection = () => {
                                                if (!isEligible) return;
                                                setSelectedClients(prev =>
                                                    prev.includes(client.client_id)
                                                        ? prev.filter(id => id !== client.client_id)
                                                        : [...prev, client.client_id]
                                                );
                                            };

                                            return (
                                                <tr
                                                    key={client.client_id}
                                                    onClick={toggleSelection}
                                                    className={`group transition-all cursor-pointer ${!isEligible ? 'bg-gray-50/50 opacity-60 grayscale' : 'hover:bg-[#FDFBF9]'
                                                        }`}
                                                >
                                                    <td className="px-6 py-4 w-10">
                                                        <div className={`
                                      h-4 w-4 rounded border transition-colors flex items-center justify-center
                                      ${selectedClients.includes(client.client_id) ? 'bg-[#1A1A1A] border-[#1A1A1A]' : 'border-gray-300 group-hover:border-gray-400'}
                                    `}>
                                                            {selectedClients.includes(client.client_id) && <CheckCircle2 size={10} className="text-white" />}
                                                        </div>
                                                    </td>

                                                    <td className="px-6 py-4 flex-1">
                                                        <div>
                                                            <p className="text-sm font-serif font-bold text-[#1A1A1A] flex items-center gap-2">
                                                                {isAnalystMode
                                                                    ? `Client ${client.client_id.substring(0, 8)}...`
                                                                    : (client.full_name || 'Client Inconnu')
                                                                }
                                                                {!isOptIn && <span className="text-[9px] px-1.5 py-0.5 bg-red-50 text-red-600 rounded border border-red-100">OPT-OUT</span>}
                                                            </p>
                                                            <p className="text-[11px] text-gray-400 font-mono mt-0.5">
                                                                {isAnalystMode ? '***@***.com' : (client.email || 'No Email')}
                                                            </p>
                                                        </div>
                                                    </td>

                                                    <td className="px-6 py-4 w-48">
                                                        <div className="flex flex-col gap-1">
                                                            <span className="text-[10px] font-bold text-gray-700 bg-gray-100 px-2 py-1 rounded w-fit">
                                                                {client.matched_criteria || 'Match Global'}
                                                            </span>
                                                        </div>
                                                    </td>

                                                    <td className="px-6 py-4 w-32">
                                                        <p className="text-[11px] text-gray-500 font-medium">
                                                            {date ? format(date, 'dd MMM yyyy', { locale: fr }) : '-'}
                                                        </p>
                                                    </td>

                                                    <td className="px-6 py-4 w-32 text-center">
                                                        {(() => {
                                                            // RECURRENCE LOGIC
                                                            if (initialStrategy?.id === 'birthday' && date) {
                                                                const today = new Date();
                                                                const nextAnniv = new Date(today.getFullYear(), date.getMonth(), date.getDate());
                                                                if (nextAnniv < today) nextAnniv.setFullYear(today.getFullYear() + 1);

                                                                const diffDays = Math.ceil((nextAnniv - today) / (1000 * 60 * 60 * 24));

                                                                if (diffDays <= 45) {
                                                                    return (
                                                                        <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-rose-50 text-rose-600 text-[10px] font-bold border border-rose-100 tracking-wide uppercase animate-pulse">
                                                                            🎂 J-{diffDays}
                                                                        </span>
                                                                    );
                                                                }
                                                            }

                                                            // Fallback to Standard Status
                                                            if (isEligible) {
                                                                return (
                                                                    <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-green-50 text-green-700 text-[10px] font-bold border border-green-100 tracking-wide uppercase">
                                                                        Eligible
                                                                    </span>
                                                                );
                                                            }

                                                            return (
                                                                <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-gray-100 text-gray-500 text-[10px] font-bold border border-gray-200 tracking-wide uppercase">
                                                                    {client.eligibility_status === 'Cooldown (60d)' ? 'Cooldown' : 'Exclu'}
                                                                </span>
                                                            );
                                                        })()}
                                                    </td>
                                                </tr>
                                            );
                                        })}
                                    </tbody>
                                </table>
                            )}
                        </div>

                        <div className="h-10 border-t border-gray-100 bg-[#FAFAFA] flex items-center px-6 text-[10px] text-gray-400 font-medium uppercase tracking-widest justify-between">
                            <span>{filteredAudience.length} résultats</span>
                            <span>LVMH CLIENTELING V3.0</span>
                        </div>

                    </div>
                </main>
            </div>
        </div>
    );
}
