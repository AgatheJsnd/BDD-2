
import React, { useState, useEffect, useCallback } from 'react';
import {
    Search, Filter, ChevronLeft, ChevronRight, ArrowUpDown,
    Download, RefreshCw, X, CheckCircle2, AlertCircle, Database, Layout
} from 'lucide-react';
import { supabase } from '../supabaseClient';

export default function DatabaseFilterPage({ onBack }) {
    const [transcriptions, setTranscriptions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [totalCount, setTotalCount] = useState(0);
    const [fetchError, setFetchError] = useState(null);

    // ── Filters ──
    const [search, setSearch] = useState('');
    const [sentimentFilter, setSentimentFilter] = useState('all'); // all, positif, neutre, négatif
    const [dateSort, setDateSort] = useState('desc'); // desc, asc

    // ── Pagination ──
    const [page, setPage] = useState(1);
    const PAGE_SIZE = 10; // Number of items per page

    // ── Fetch Data ──
    const fetchData = useCallback(async () => {
        setLoading(true);
        setFetchError(null);
        try {
            // Base Query
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
        `, { count: 'exact' });

            // Apply Filters
            if (search) {
                query = query.or(`client_name.ilike.%${search}%,content_summary.ilike.%${search}%`);
            }
            if (sentimentFilter !== 'all') {
                query = query.eq('sentiment', sentimentFilter);
            }

            // Apply Sorting
            query = query.order('created_at', { ascending: dateSort === 'asc' });

            // Apply Pagination
            const from = (page - 1) * PAGE_SIZE;
            const to = from + PAGE_SIZE - 1;
            query = query.range(from, to);

            // Execute
            const { data, error, count } = await query;

            if (error) throw error;

            setTranscriptions(data || []);
            setTotalCount(count || 0);

        } catch (e) {
            console.error("Error fetching database:", e);
            setFetchError(e.message || "Erreur inconnue lors du chargement des données.");
        } finally {
            setLoading(false);
        }
    }, [search, sentimentFilter, dateSort, page]);

    // Debounce search refresh
    useEffect(() => {
        const timer = setTimeout(() => {
            fetchData();
        }, 300);
        return () => clearTimeout(timer);
    }, [fetchData]);

    const totalPages = Math.ceil(totalCount / PAGE_SIZE) || 1;

    return (
        <div className="min-h-screen bg-[#F3F5F7] p-4 md:p-8 font-sans text-[#111]">
            <div className="max-w-[1440px] mx-auto h-full flex flex-col">

                {/* HEADER */}
                <div className="flex flex-col md:flex-row items-start md:items-center justify-between mb-6 gap-4">
                    <div className="flex items-center gap-4">
                        <button
                            onClick={onBack}
                            className="h-10 w-10 rounded-full bg-white border border-gray-200 flex items-center justify-center hover:bg-gray-50 transition shadow-sm"
                        >
                            <ChevronLeft size={20} className="text-gray-600" />
                        </button>
                        <div>
                            <h1 className="text-2xl font-bold tracking-tight text-[#111] flex items-center gap-2">
                                <Layout className="text-[#C87961]" size={24} />
                                Base de Données
                            </h1>
                            <p className="text-sm text-gray-500">Vue complète des transcriptions & analyses</p>
                        </div>
                    </div>

                    <div className="flex gap-3">
                        <button
                            onClick={fetchData}
                            className="h-10 px-4 rounded-full bg-white border border-gray-200 flex items-center gap-2 text-sm font-medium hover:bg-gray-50 transition"
                        >
                            <RefreshCw size={14} className={loading ? "animate-spin" : ""} /> Actualiser
                        </button>
                        <button className="h-10 px-4 rounded-full bg-[#1A1A1A] text-white flex items-center gap-2 text-sm font-medium hover:bg-[#333] transition shadow-md">
                            <Download size={14} /> Exporter CSV
                        </button>
                    </div>
                </div>

                {/* FILTERS BAR */}
                <div className="bg-white rounded-2xl p-4 shadow-sm border border-gray-100 flex flex-wrap items-center gap-4 mb-6">
                    {/* Global Search */}
                    <div className="relative flex-1 min-w-[200px]">
                        <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Rechercher client, résumé..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                            className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-200 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-[#C87961]/20 focus:border-[#C87961] outline-none transition text-sm"
                        />
                    </div>

                    {/* Filters Group */}
                    <div className="flex items-center gap-2">
                        <Filter size={16} className="text-gray-400" />

                        {/* Sentiment */}
                        <select
                            value={sentimentFilter}
                            onChange={(e) => { setSentimentFilter(e.target.value); setPage(1); }}
                            className="px-3 py-2.5 rounded-xl border border-gray-200 bg-white text-sm focus:border-[#C87961] outline-none cursor-pointer hover:bg-gray-50 transition"
                        >
                            <option value="all">Tous Sentiments</option>
                            <option value="positif">Positif 🟢</option>
                            <option value="neutre">Neutre ⚪</option>
                            <option value="négatif">Négatif 🔴</option>
                        </select>
                    </div>

                    {/* Sorting */}
                    <button
                        onClick={() => { setDateSort(prev => prev === 'desc' ? 'asc' : 'desc'); }}
                        className="flex items-center gap-2 px-3 py-2.5 rounded-xl border border-gray-200 bg-white text-sm hover:bg-gray-50 transition"
                    >
                        <ArrowUpDown size={14} />
                        {dateSort === 'desc' ? 'Plus Récents' : 'Plus Anciens'}
                    </button>
                </div>

                {/* DATA TABLE */}
                <div className="bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden flex-1 flex flex-col">
                    <div className="overflow-x-auto flex-1">
                        <table className="w-full text-left border-collapse min-w-[900px]">
                            <thead className="bg-gray-50/50 border-b border-gray-100 sticky top-0 z-10 backdrop-blur-sm">
                                <tr className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                                    <th className="p-4 w-16 text-center">Badge</th>
                                    <th className="p-4">Client</th>
                                    <th className="p-4 w-[35%]">Analyse</th>
                                    <th className="p-4">Tags</th>
                                    <th className="p-4">Sentiment</th>
                                    <th className="p-4 text-right">Date</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-50">
                                {loading && transcriptions.length === 0 ? (
                                    <tr>
                                        <td colSpan="6" className="p-20 text-center text-gray-400">
                                            <div className="flex flex-col items-center">
                                                <RefreshCw size={32} className="animate-spin mb-4 opacity-20" />
                                                <p>Chargement des données...</p>
                                            </div>
                                        </td>
                                    </tr>
                                ) : fetchError ? (
                                    <tr>
                                        <td colSpan="6" className="p-20 text-center text-red-500">
                                            <div className="flex flex-col items-center">
                                                <AlertCircle size={32} className="mb-4" />
                                                <p className="font-bold">Erreur de chargement</p>
                                                <p className="text-sm mt-2">{fetchError}</p>
                                            </div>
                                        </td>
                                    </tr>
                                ) : transcriptions.length === 0 ? (
                                    <tr>
                                        <td colSpan="6" className="p-20 text-center flex flex-col items-center justify-center text-gray-400">
                                            <Database size={48} className="mb-4 opacity-10" />
                                            <p className="text-lg font-medium text-gray-500">Aucune donnée trouvée</p>
                                            <p className="text-sm mt-1">Essayez d'ajuster vos filtres.</p>
                                        </td>
                                    </tr>
                                ) : (
                                    transcriptions.map((t) => (
                                        <tr key={t.id} className="hover:bg-amber-50/20 transition-colors group cursor-pointer">
                                            <td className="p-4 text-center">
                                                <div className={`h-9 w-9 mx-auto rounded-full flex items-center justify-center text-white text-[12px] font-bold shadow-sm ring-2 ring-white ${t.sentiment === 'positif' ? 'bg-emerald-500' :
                                                    t.sentiment === 'négatif' ? 'bg-rose-500' : 'bg-slate-400'
                                                    }`}>
                                                    {t.client_name?.charAt(0).toUpperCase() || '?'}
                                                </div>
                                            </td>
                                            <td className="p-4">
                                                <p className="font-semibold text-gray-900">{t.client_name}</p>
                                                <p className="text-[10px] text-gray-400 font-mono mt-0.5" title={t.id}>ID: ...{t.id.slice(-6)}</p>
                                            </td>
                                            <td className="p-4">
                                                <div className="text-sm font-medium text-gray-800 line-clamp-1">{t.content_summary}</div>
                                                <div className="text-xs text-gray-500 line-clamp-2 mt-1 font-light italic">
                                                    "{t.raw_text || '...'}"
                                                </div>
                                            </td>
                                            <td className="p-4">
                                                <div className="flex flex-wrap gap-1">
                                                    {t.tags && t.tags.length > 0 ? (
                                                        t.tags.slice(0, 3).map((tag, i) => (
                                                            <span key={i} className="px-2 py-0.5 bg-gray-100 text-gray-600 text-[10px] font-medium rounded-md border border-gray-200">
                                                                {tag.tag_name}
                                                            </span>
                                                        ))
                                                    ) : <span className="text-xs text-gray-300 italic">Aucun tag</span>}
                                                    {t.tags && t.tags.length > 3 && (
                                                        <span className="px-1.5 py-0.5 text-[10px] text-gray-400 bg-gray-50 rounded-md border border-gray-100">+{t.tags.length - 3}</span>
                                                    )}
                                                </div>
                                            </td>
                                            <td className="p-4">
                                                <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border ${t.sentiment === 'positif' ? 'bg-emerald-50 text-emerald-700 border-emerald-100' :
                                                    t.sentiment === 'négatif' ? 'bg-rose-50 text-rose-700 border-rose-100' : 'bg-slate-50 text-slate-600 border-slate-100'
                                                    }`}>
                                                    {t.sentiment === 'positif' && <CheckCircle2 size={12} />}
                                                    {t.sentiment === 'négatif' && <AlertCircle size={12} />}
                                                    {t.sentiment || 'Neutre'}
                                                </span>
                                            </td>
                                            <td className="p-4 text-right text-sm text-gray-500 tabular-nums">
                                                <div className="font-medium">{new Date(t.created_at).toLocaleDateString('fr-FR')}</div>
                                                <div className="text-[10px] text-gray-400">
                                                    {new Date(t.created_at).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
                                                </div>
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    </div>

                    {/* PAGINATION */}
                    <div className="bg-white border-t border-gray-100 p-4 flex flex-col md:flex-row items-center justify-between gap-4 shrink-0">
                        <div className="text-sm text-gray-500">
                            Affichage de <span className="font-bold text-gray-900">{transcriptions.length}</span> résultats sur <span className="font-bold text-gray-900">{totalCount}</span>
                        </div>

                        <div className="flex items-center gap-2 bg-gray-50 p-1 rounded-xl border border-gray-100">
                            <button
                                disabled={page === 1}
                                onClick={() => setPage(p => Math.max(1, p - 1))}
                                className="h-8 px-3 rounded-lg bg-white text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center gap-1 text-sm font-medium shadow-sm border border-gray-100"
                            >
                                <ChevronLeft size={14} /> Précédent
                            </button>

                            <span className="px-4 text-sm font-semibold text-gray-700 min-w-[80px] text-center">
                                Page {page} <span className="text-gray-400 font-normal">/ {totalPages}</span>
                            </span>

                            <button
                                disabled={page >= totalPages}
                                onClick={() => setPage(p => p + 1)}
                                className="h-8 px-3 rounded-lg bg-white text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center gap-1 text-sm font-medium shadow-sm border border-gray-100"
                            >
                                Suivant <ChevronRight size={14} />
                            </button>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
}
