import React, { useState, useEffect } from 'react';
import { ArrowLeft, Sparkles, TrendingUp, AlertCircle, BarChart3, Download, RefreshCw } from 'lucide-react';
import { supabase } from '../supabaseClient';
import { motion } from 'framer-motion';

export default function StatsPage({ onBack, selectedDate }) {
    const [loading, setLoading] = useState(false);
    const [analyzing, setAnalyzing] = useState(false);
    const [insights, setInsights] = useState(null);
    const [error, setError] = useState(null);
    const [transcripts, setTranscripts] = useState([]);
    const [taxonomy, setTaxonomy] = useState([]);

    // Approval State
    const [tagToApprove, setTagToApprove] = useState(null);

    const months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc'];

    // --- 1. Fetch Data ---
    const fetchData = async () => {
        setLoading(true);
        try {
            let records = [];

            if (selectedDate && selectedDate.days && selectedDate.days.length > 0) {
                // Filter by selected Date
                const monthIndex = months.indexOf(selectedDate.month);
                if (monthIndex !== -1) {
                    const year = selectedDate.year;
                    const startOfMonth = new Date(year, monthIndex, 1).toISOString();
                    const startOfNextMonth = new Date(year, monthIndex + 1, 1).toISOString();

                    const { data: monthData, error: monthError } = await supabase
                        .from('transcriptions')
                        .select('id, created_at, client_name, raw_text, tags(tag_name)')
                        .gte('created_at', startOfMonth)
                        .lt('created_at', startOfNextMonth)
                        .order('created_at', { ascending: false });

                    if (monthError) throw monthError;

                    // Filter by specific days
                    records = (monthData || []).filter(t => {
                        const d = new Date(t.created_at);
                        return selectedDate.days.includes(d.getDate());
                    });
                }
            } else {
                // Fallback: Last 100
                const { data: fallbackData, error: fallbackError } = await supabase
                    .from('transcriptions')
                    .select('id, created_at, client_name, raw_text, tags(tag_name)')
                    .order('created_at', { ascending: false })
                    .limit(100);

                if (fallbackError) throw fallbackError;
                records = fallbackData || [];
            }

            setTranscripts(records);

            // Get Taxonomy (unique tags)
            const { data: tagData, error: tagError } = await supabase
                .from('tags')
                .select('tag_name');

            if (tagError) throw tagError;
            const uniqueTags = [...new Set(tagData.map(t => t.tag_name))];
            setTaxonomy(uniqueTags);

        } catch (err) {
            console.error(err);
            setError("Impossible de charger les données.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    // --- 2. Run AI Analysis ---
    const runAnalysis = async () => {
        setAnalyzing(true);
        setError(null);
        try {
            let dateRangeLabel = "Dernières 100 transcriptions";
            if (selectedDate && selectedDate.days && selectedDate.days.length > 0) {
                dateRangeLabel = `${selectedDate.days.join(', ')} ${selectedDate.month} ${selectedDate.year}`;
            }

            const payload = {
                date_range: dateRangeLabel,
                current_taxonomy: taxonomy,
                transcripts: transcripts.map(t => ({
                    id: t.id,
                    date: t.created_at,
                    text: t.raw_text || "Texte non disponible",
                    client: t.client_name
                }))
            };

            const response = await fetch('/api/insights', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const textResult = await response.text();
            let result;

            try {
                result = JSON.parse(textResult);
            } catch (e) {
                console.error("Non-JSON response:", textResult.slice(0, 500));
                throw new Error("Le serveur backend doit être redémarré (Reçu: HTML au lieu de JSON).");
            }

            if (!response.ok) {
                throw new Error(result.error || `Erreur serveur (${response.status})`);
            }

            if (typeof result === 'string') {
                setInsights(JSON.parse(result));
            } else {
                setInsights(result);
            }

        } catch (err) {
            console.error(err);
            setError(err.message || "Erreur lors de l'analyse IA");
        } finally {
            setAnalyzing(false);
        }
    };

    // --- 3. Tag Approval Logic ---
    const handleTagClick = (tagItem) => {
        setTagToApprove(tagItem);
    };

    const confirmAddTag = async () => {
        if (!tagToApprove) return;

        try {
            // Simulate adding to taxonomy by updating local state
            setTaxonomy(prev => [...prev, tagToApprove.term]);

            // Remove from suggestions locally
            setInsights(prev => ({
                ...prev,
                taxonomy_suggestions: prev.taxonomy_suggestions.filter(t => t.term !== tagToApprove.term)
            }));

            setTagToApprove(null);
        } catch (e) {
            console.error(e);
        }
    };

    return (
        <div className="min-h-screen bg-[#F3F5F7] p-4 md:p-8 font-sans flex flex-col">
            <div className="max-w-7xl mx-auto w-full">
                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <div className="flex items-center gap-4">
                        <button onClick={onBack} className="p-2 bg-white rounded-full hover:bg-gray-50 transition border border-gray-200">
                            <ArrowLeft size={20} className="text-gray-600" />
                        </button>
                        <div>
                            <h1 className="text-2xl font-bold text-[#111]">Intelligence Client & Tendances</h1>
                            <p className="text-sm text-gray-500">
                                {transcripts.length > 0 ?
                                    `Analyse de ${transcripts.length} transcriptions (${selectedDate && selectedDate.days.length > 0 ? `${selectedDate.days.join(', ')} ${selectedDate.month}` : 'Récents'})`
                                    : 'Aucune donnée sélectionnée'}
                            </p>
                        </div>
                    </div>
                    <div>
                        {!insights && (
                            <button
                                onClick={runAnalysis}
                                disabled={analyzing || loading || transcripts.length === 0}
                                className="flex items-center gap-2 px-6 py-3 bg-[#1A1A1A] text-white rounded-full font-semibold hover:bg-[#333] disabled:opacity-50 transition shadow-lg"
                            >
                                {analyzing ? <RefreshCw className="animate-spin" size={20} /> : <Sparkles size={20} />}
                                {analyzing ? 'Analyse en cours...' : 'Lancer l\'Analyse IA'}
                            </button>
                        )}
                    </div>
                </div>

                {/* Error Banner */}
                {error && (
                    <div className="mb-6 p-4 bg-red-50 text-red-600 rounded-xl flex items-center gap-2 border border-red-100">
                        <AlertCircle size={20} />
                        {error}
                    </div>
                )}

                {/* Content */}
                {insights ? (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 animate-in fade-in slide-in-from-bottom-5 duration-700">
                        {/* 1. Taxonomy Suggestions */}
                        <div className="bg-white rounded-[32px] p-8 shadow-sm border border-gray-100/50">
                            <div className="flex items-center justify-between mb-6">
                                <h3 className="text-xl font-bold text-[#111] flex items-center gap-2">
                                    <span className="p-2 bg-orange-50 rounded-lg text-[#C87961]">🏷️</span>
                                    Nouvelles Opportunités
                                </h3>
                                <span className="text-xs font-medium bg-gray-100 px-3 py-1 rounded-full text-gray-600">Taxonomie</span>
                            </div>
                            <div className="space-y-4">
                                {insights.taxonomy_suggestions?.length > 0 ? (
                                    insights.taxonomy_suggestions.map((item, idx) => (
                                        <button
                                            key={idx}
                                            onClick={() => handleTagClick(item)}
                                            className="w-full text-left p-4 rounded-xl bg-gray-50 hover:bg-orange-50 transition border border-transparent hover:border-orange-200 group relative"
                                        >
                                            <div className="flex justify-between items-start">
                                                <p className="font-bold text-[#111] text-lg flex items-center gap-2">
                                                    {item.term}
                                                    <span className="opacity-0 group-hover:opacity-100 text-xs bg-orange-100 text-orange-600 px-2 py-0.5 rounded-full transition-opacity">
                                                        + Ajouter
                                                    </span>
                                                </p>
                                                <span className="text-[10px] uppercase font-bold text-gray-400 bg-white px-2 py-1 rounded border border-gray-100">{item.category}</span>
                                            </div>
                                            <p className="text-sm text-gray-600 mt-1">{item.reason}</p>
                                        </button>
                                    ))
                                ) : (
                                    <div className="p-6 text-center text-gray-400 italic bg-gray-50 rounded-xl border border-dashed border-gray-200">
                                        Aucune suggestion détectée pour ce lot (textes trop courts ou génériques).
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* 2. Marketing Actions */}
                        <div className="bg-white rounded-[32px] p-8 shadow-sm border border-gray-100/50">
                            <div className="flex items-center justify-between mb-6">
                                <h3 className="text-xl font-bold text-[#111] flex items-center gap-2">
                                    <span className="p-2 bg-emerald-50 rounded-lg text-emerald-600">🚀</span>
                                    Actions Recommandées
                                </h3>
                                <span className="text-xs font-medium bg-gray-100 px-3 py-1 rounded-full text-gray-600">Marketing</span>
                            </div>
                            <div className="space-y-4">
                                {insights.marketing_actions?.length > 0 ? (
                                    insights.marketing_actions.map((action, idx) => (
                                        <div key={idx} className="relative p-5 rounded-2xl border border-gray-100 bg-gradient-to-br from-white to-gray-50 overflow-hidden">
                                            <div className={`absolute left-0 top-0 bottom-0 w-1 ${action.priority === 'High' ? 'bg-red-500' : action.priority === 'Medium' ? 'bg-orange-400' : 'bg-green-400'}`} />
                                            <div className="pl-3">
                                                <div className="flex justify-between mb-2">
                                                    <h4 className="font-semibold text-gray-900 text-sm">{action.insight}</h4>
                                                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${action.priority === 'High' ? 'bg-red-100 text-red-600' : 'bg-orange-100 text-orange-600'}`}>{action.priority} Priority</span>
                                                </div>
                                                <p className="text-[#1A1A1A] font-medium text-base leading-snug">"{action.suggested_action}"</p>
                                            </div>
                                        </div>
                                    ))
                                ) : (
                                    <div className="p-6 text-center text-gray-400 italic bg-gray-50 rounded-xl border border-dashed border-gray-200">
                                        Pas d'actions marketing identifiées.
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* 3. Global Stats */}
                        <div className="lg:col-span-2 bg-[#1A1A1A] rounded-[32px] p-8 text-white shadow-xl relative overflow-hidden">
                            <div className="relative z-10 flex flex-col md:flex-row gap-10">
                                <div className="flex-1">
                                    <h3 className="text-2xl font-bold mb-2">Top Tendances Globales</h3>
                                    <p className="text-gray-400 mb-8 text-sm">Tags les plus fréquents détectés dans le lot.</p>

                                    <div className="space-y-5 pr-2">
                                        {(() => {
                                            const maxCount = Math.max(...(insights.graph_data?.top_tags_global?.map(t => t.count) || [10]));
                                            return insights.graph_data?.top_tags_global?.map((tag, i) => (
                                                <div key={i} className="group">
                                                    <div className="flex items-center justify-between mb-1.5">
                                                        <span className="text-sm font-medium text-gray-200 tracking-wide group-hover:text-white transition-colors">
                                                            {tag.tag.replace(/_/g, ' ')}
                                                        </span>
                                                        <span className="text-xs font-bold text-[#C87961] bg-[#C87961]/10 px-2 py-0.5 rounded-full border border-[#C87961]/20">
                                                            {tag.count} occurrences
                                                        </span>
                                                    </div>
                                                    <div className="h-2.5 w-full bg-gray-800/50 rounded-full overflow-hidden backdrop-blur-sm border border-white/5">
                                                        <motion.div
                                                            initial={{ width: 0 }}
                                                            animate={{ width: `${(tag.count / maxCount) * 100}%` }}
                                                            transition={{ duration: 1, ease: "easeOut", delay: i * 0.1 }}
                                                            className="h-full bg-gradient-to-r from-[#C87961] via-[#D68B75] to-[#E8A68D] rounded-full relative"
                                                        >
                                                            <div className="absolute right-0 top-0 bottom-0 w-1 bg-white/30 skew-x-12 blur-[1px]" />
                                                        </motion.div>
                                                    </div>
                                                </div>
                                            ));
                                        })()}
                                    </div>
                                </div>

                                <div className="flex-1 border-l border-gray-800 pl-0 md:pl-10 pt-10 md:pt-0">
                                    <h3 className="text-xl font-bold mb-6">Par Langue</h3>
                                    <div className="grid grid-cols-2 gap-6">
                                        {Object.entries(insights.graph_data?.top_tags_by_language || {}).map(([lang, tags]) => (
                                            <div key={lang}>
                                                <h4 className="text-sm font-bold text-[#C87961] uppercase mb-2">{lang === 'fr' ? 'Français' : lang === 'en' ? 'English' : lang}</h4>
                                                <ul className="text-sm text-gray-400 space-y-1">
                                                    {tags.map((t, k) => <li key={k}>• {t}</li>)}
                                                </ul>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                ) : (
                    /* Empty State / Intro */
                    <div className="bg-white rounded-3xl p-10 text-center border border-gray-100 shadow-sm min-h-[50vh] flex flex-col items-center justify-center">
                        <div className="h-20 w-20 bg-orange-50 rounded-full flex items-center justify-center mb-6">
                            <Sparkles size={40} className="text-[#C87961]" />
                        </div>
                        <h2 className="text-2xl font-bold text-[#111] mb-2">Prêt à analyser vos données ?</h2>
                        <p className="text-gray-500 max-w-md mx-auto mb-8">
                            {transcripts.length > 0 ? (
                                <>
                                    L'IA va analyser <strong className="text-gray-900">{transcripts.length} transcriptions</strong> du
                                    <br /><span className="text-[#C87961] font-semibold">{selectedDate && selectedDate.days ? `${selectedDate.days.join(', ')} ${selectedDate.month} ${selectedDate.year}` : 'sélectionnées'}</span>.
                                </>
                            ) : (
                                "Sélectionnez des dates dans le calendrier pour commencer."
                            )}
                        </p>

                        {transcripts.length > 0 && (
                            <div className="mb-8 px-5 py-2.5 bg-gray-50 rounded-full border border-gray-200 inline-flex items-center gap-2.5">
                                <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
                                <span className="text-xs font-medium text-gray-600">
                                    Temps estimé : <span className="text-[#111] font-bold">~{Math.max(10, Math.ceil(transcripts.length / 25) * 35)} secondes</span>
                                </span>
                            </div>
                        )}
                        {transcripts.length === 0 && (
                            <div className="text-red-500 text-sm font-medium bg-red-50 px-4 py-2 rounded-lg">
                                Aucune transcription trouvée pour ces dates. Essayez une autre période.
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* CONFIRMATION MODAL */}
            {tagToApprove && (
                <div className="fixed inset-0 bg-black/50 z-[100] flex items-center justify-center p-4 backdrop-blur-sm">
                    <motion.div
                        initial={{ scale: 0.9, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        className="bg-white rounded-2xl p-6 md:p-8 max-w-sm w-full shadow-2xl"
                    >
                        <h3 className="text-xl font-bold text-[#111] mb-2">Ajouter ce tag ?</h3>
                        <div className="bg-orange-50 p-3 rounded-lg border border-orange-100 mb-4">
                            <p className="text-lg font-bold text-[#C87961]">{tagToApprove.term}</p>
                            <p className="text-xs text-gray-500 uppercase mt-1">{tagToApprove.category}</p>
                        </div>
                        <p className="text-gray-600 text-sm mb-6">
                            Voulez-vous officiellement ajouter ce terme à la taxonomie globale de LVMH ?
                        </p>
                        <div className="flex gap-3">
                            <button
                                onClick={() => setTagToApprove(null)}
                                className="flex-1 py-3 rounded-full border border-gray-200 font-semibold text-gray-600 hover:bg-gray-50 transition"
                            >
                                Non, annuler
                            </button>
                            <button
                                onClick={confirmAddTag}
                                className="flex-1 py-3 rounded-full bg-[#1A1A1A] font-semibold text-white hover:bg-black transition shadow-lg"
                            >
                                Oui, ajouter
                            </button>
                        </div>
                    </motion.div>
                </div>
            )}
        </div>
    );
}
