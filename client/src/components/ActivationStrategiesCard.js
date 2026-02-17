import React, { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import {
    Gift, ShoppingBag, Wine, Plane, ChevronRight, Sparkles, Filter, Leaf, Music, TrendingUp, Gem, Briefcase, Palmtree
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import CampaignWorkspace from './CampaignWorkspace';
import { supabase } from '../supabaseClient';

// ── STRATEGY CONFIGURATION (V4 - REAL DATA ALIGNED) ──
// Top Tags found: Rappeler, Vegan, Cognac, Chic, Bleu_marine, 5-10k, Cadeau, Anniversaire, Business
const STRATEGIES_CONFIG = [
    {
        id: 'birthday',
        category: 'Court Terme',
        title: 'Anniversaires & Cadeaux',
        subtitle: 'Opportunités du Moment',
        icon: Gift,
        color: 'text-rose-600',
        bgColor: 'bg-rose-50',
        borderColor: 'border-rose-100',
        trigger: 'Tag: Anniversaire, Cadeau',
        query: 'Anniversaire'
    },
    {
        id: 'relance_client',
        category: 'Court Terme',
        title: 'À Rappeler (Urgent)',
        subtitle: 'Suivi Clientèle',
        icon: Sparkles,
        color: 'text-amber-600',
        bgColor: 'bg-amber-50',
        borderColor: 'border-amber-100',
        trigger: 'Tag: Rappeler',
        query: 'Rappeler'
    },
    {
        id: 'upgrade_exotic',
        category: 'High Value',
        title: 'Montée en Gamme',
        subtitle: 'Potentiel Exotique',
        icon: Gem,
        color: 'text-purple-600',
        bgColor: 'bg-purple-50',
        borderColor: 'border-purple-100',
        trigger: 'Tag: Cuir, VIP, 10-15k',
        query: 'Cuir'
    },
    {
        id: 'style_chic',
        category: 'High Value',
        title: 'L\'Élégance Classique',
        subtitle: 'Code: Chic & Business',
        icon: Briefcase,
        color: 'text-slate-700',
        bgColor: 'bg-slate-50',
        borderColor: 'border-slate-100',
        trigger: 'Tag: Chic, Business',
        query: 'Chic'
    },
    {
        id: 'leather_goods',
        category: 'High Value',
        title: 'Maroquinerie d\'Exception',
        subtitle: 'Cuir & Cognac',
        icon: ShoppingBag,
        color: 'text-[#C87961]', // Terracotta
        bgColor: 'bg-[#F8EBE6]',
        borderColor: 'border-[#E8D5CF]',
        trigger: 'Tag: Cuir, Cognac',
        query: 'Cognac'
    },
    {
        id: 'eco_responsible',
        category: 'Lifestyle',
        title: 'Cercle Éco-Responsable',
        subtitle: 'Engagement Durable',
        icon: Leaf,
        color: 'text-green-600',
        bgColor: 'bg-green-50',
        borderColor: 'border-green-100',
        trigger: 'Tag: Vegan, Durabilité',
        query: 'Vegan'
    },
    {
        id: 'nautical',
        category: 'Lifestyle',
        title: 'Esprit Riviera',
        subtitle: 'Bleu Marine & Voyage',
        icon: Palmtree,
        color: 'text-blue-600',
        bgColor: 'bg-blue-50',
        borderColor: 'border-blue-100',
        trigger: 'Tag: Bleu_marine, Voyageur',
        query: 'Bleu_marine'
    }
];

export default function ActivationStrategiesCard({ className }) {
    const [activeFilter, setActiveFilter] = useState('Tout');
    const [showWorkspace, setShowWorkspace] = useState(false);
    const [selectedStrategy, setSelectedStrategy] = useState(null);
    const [counts, setCounts] = useState({});
    const [urgencyData, setUrgencyData] = useState({});
    const [loadingCounts, setLoadingCounts] = useState(true);

    const filters = ['Tout', 'Court Terme', 'Lifestyle', 'High Value'];

    // Filter Logic
    const filteredStrategies = activeFilter === 'Tout'
        ? STRATEGIES_CONFIG
        : STRATEGIES_CONFIG.filter(s => s.category === activeFilter);

    // Fetch Counts & Urgency on Mount
    useEffect(() => {
        const fetchCounts = async () => {
            setLoadingCounts(true);
            const newCounts = {};
            const newUrgency = {};

            // Parallel Fetch
            await Promise.all(STRATEGIES_CONFIG.map(async (strategy) => {
                try {
                    const { data, error } = await supabase.rpc('deep_memory_search', {
                        filter_value: strategy.query,
                        filter_location: '',
                        current_campaign_tag: 'COUNT_CHECK'
                    });

                    if (!error && data) {
                        newCounts[strategy.id] = data.length;

                        // Check for High Urgency (Score 1 or 2)
                        // Score 1 = < 7 days
                        // Score 2 = < 30 days
                        const highPriority = data.filter(c => c.urgency_score === 1 || c.urgency_score === 2);
                        const topUrgency = highPriority.length > 0
                            ? Math.min(...highPriority.map(c => c.days_remaining))
                            : null;

                        newUrgency[strategy.id] = {
                            count: highPriority.length,
                            minDays: topUrgency
                        };

                    } else {
                        newCounts[strategy.id] = 0;
                        newUrgency[strategy.id] = { count: 0, minDays: null };
                    }
                } catch (err) {
                    console.error(`Error counting for ${strategy.id}:`, err);
                    newCounts[strategy.id] = 0;
                    newUrgency[strategy.id] = { count: 0, minDays: null };
                }
            }));

            setCounts(newCounts);
            setUrgencyData(newUrgency);
            setLoadingCounts(false);
        };

        fetchCounts();
    }, []);

    const handleStrategyClick = (strategy) => {
        setSelectedStrategy(strategy);
        setShowWorkspace(true);
    };

    // Sort Strategies: Urgency First, then Default Order
    const sortedStrategies = [...filteredStrategies].sort((a, b) => {
        // Mock urgency for new strategies if not yet loaded
        const urgencyA = urgencyData[a.id]?.count > 0 ? 1 : 0;
        const urgencyB = urgencyData[b.id]?.count > 0 ? 1 : 0;

        if (urgencyA !== urgencyB) {
            return urgencyB - urgencyA; // Urgent strategies first
        }
        // Real Sorting Logic (When V5 RPC is live)
        // return (b.urgencyCount - a.urgencyCount);
        return 0; // Keeping default for now to avoid jumpiness before RPC update
    });

    return (
        <div className={`h-full w-full flex flex-col relative overflow-hidden bg-white rounded-[40px] shadow-[0_20px_50px_-12px_rgba(0,0,0,0.03)] p-6 ${className}`}>

            {/* ── HEADER ── */}
            <div className="flex flex-col gap-4 mb-4 shrink-0">
                <div className="flex items-center justify-between">
                    <h3 className="text-[15px] font-semibold text-[#111]">Stratégies d'Activation</h3>
                    <div className="flex items-center gap-2 text-gray-400">
                        {loadingCounts && <div className="animate-spin h-3 w-3 border-2 border-gray-300 border-t-[#C87961] rounded-full" />}
                        <Sparkles size={16} className="text-[#C87961]" />
                    </div>
                </div>

                {/* Filter Tabs */}
                <div className="flex items-center gap-2 overflow-x-auto no-scrollbar pb-1">
                    {filters.map(filter => (
                        <button
                            key={filter}
                            onClick={() => setActiveFilter(filter)}
                            className={`whitespace-nowrap px-3 py-1.5 rounded-full text-[11px] font-semibold transition-all border ${activeFilter === filter
                                ? 'bg-[#1A1A1A] text-white border-[#1A1A1A]'
                                : 'bg-white text-gray-500 border-gray-100 hover:border-gray-200'
                                }`}
                        >
                            {filter}
                        </button>
                    ))}
                </div>
            </div>

            {/* ── BODY (Scrollable List) ── */}
            <div className="flex-1 overflow-y-auto pr-1 space-y-3" style={{ scrollbarWidth: 'thin', scrollbarColor: '#E5E7EB transparent' }}>
                <AnimatePresence mode='popLayout'>
                    {sortedStrategies.map((strategy, index) => {
                        const count = counts[strategy.id] || 0;
                        const urgencyInfo = urgencyData[strategy.id] || { count: 0, minDays: null };
                        const isUrgent = urgencyInfo.count > 0;

                        return (
                            <motion.div
                                key={strategy.id}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, scale: 0.95 }}
                                transition={{ delay: index * 0.05 }}
                                onClick={() => handleStrategyClick(strategy)}
                                className={`group relative p-4 rounded-2xl border ${strategy.borderColor} ${strategy.bgColor} hover:shadow-md transition-all cursor-pointer`}
                            >

                                {/* Header: Icon + Title */}
                                <div className="flex items-start justify-between mb-2">
                                    <div className="flex items-center gap-3">
                                        <div className={`h-10 w-10 rounded-full bg-white flex items-center justify-center shadow-sm relative ${strategy.color}`}>
                                            <strategy.icon size={18} strokeWidth={2.5} />
                                            {isUrgent && (
                                                <div className="absolute -top-1 -right-1 h-3 w-3 bg-red-500 rounded-full border-2 border-white animate-pulse" />
                                            )}
                                        </div>
                                        <div>
                                            <h4 className="text-[13px] font-bold text-gray-900 flex items-center gap-2">
                                                {strategy.title}
                                                {isUrgent && urgencyInfo.minDays !== null && (
                                                    <span className="text-[9px] px-1.5 py-0.5 bg-red-100 text-red-600 rounded-full animate-pulse">
                                                        J-{urgencyInfo.minDays}
                                                    </span>
                                                )}
                                            </h4>
                                            <p className="text-[11px] text-gray-500 font-medium">{strategy.subtitle}</p>
                                        </div>
                                    </div>
                                    {/* Confidence Score Bar */}
                                    <div className="text-right">
                                        <div className="text-[9px] font-bold text-gray-400 uppercase tracking-wider mb-1">Potentiel</div>
                                        <div className="h-1.5 w-16 bg-white rounded-full overflow-hidden border border-white/50">
                                            <div className="h-full bg-green-500 rounded-full" style={{ width: `${Math.min(100, (count / 5) * 100)}%` }} />
                                        </div>
                                    </div>
                                </div>

                                {/* Action Section */}
                                <div className="flex items-center justify-between mt-3 pl-1">
                                    <p className="text-[10px] text-gray-500 italic max-w-[140px] truncate">
                                        {strategy.trigger}
                                    </p>
                                    <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white shadow-sm text-[10px] font-bold text-[#1A1A1A] group-hover:bg-[#C87961] group-hover:text-white transition-colors">
                                        {loadingCounts ? '...' : `Voir ${count} Clients`}
                                        <ChevronRight size={12} />
                                    </button>
                                </div>

                            </motion.div>
                        );
                    })}
                </AnimatePresence>

                {filteredStrategies.length === 0 && (
                    <div className="flex flex-col items-center justify-center h-40 text-center opacity-50">
                        <Sparkles size={24} className="mb-2 text-gray-400" />
                        <p className="text-xs text-gray-500">Aucune stratégie trouvée.</p>
                    </div>
                )}
            </div>

            {/* ── CAMPAIGN WORKSPACE PORTAL ── */}
            {showWorkspace && createPortal(
                <CampaignWorkspace
                    isOpen={showWorkspace}
                    onClose={() => setShowWorkspace(false)}
                    initialStrategy={selectedStrategy}
                />,
                document.body
            )}
        </div>
    );
}
