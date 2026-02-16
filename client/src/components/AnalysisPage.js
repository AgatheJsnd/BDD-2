import React, { useState, useEffect } from 'react';
import { ArrowLeft, Save, Tag, Check, AlertCircle, Edit3, Trash2 } from 'lucide-react';
import { supabase } from '../supabaseClient';

export default function AnalysisPage({ onBack }) {
    const [transcriptions, setTranscriptions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedId, setSelectedId] = useState(null);
    const [editedTags, setEditedTags] = useState([]);
    const [newTag, setNewTag] = useState('');

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        setLoading(true);
        const { data, error } = await supabase
            .from('transcriptions')
            .select(`
                id, 
                client_name, 
                content_summary, 
                raw_text, 
                tags ( id, tag_name )
            `)
            .order('created_at', { ascending: false })
            .limit(50);

        if (data) setTranscriptions(data);
        setLoading(false);
    };

    const handleSelect = (item) => {
        setSelectedId(item.id);
        setEditedTags(item.tags.map(t => t.tag_name));
    };

    const handleAddTag = () => {
        if (newTag && !editedTags.includes(newTag)) {
            setEditedTags([...editedTags, newTag]);
            setNewTag('');
        }
    };

    const handleRemoveTag = (tagToRemove) => {
        setEditedTags(editedTags.filter(t => t !== tagToRemove));
    };

    const handleSave = async () => {
        if (!selectedId) return;

        // 1. Delete old tags
        await supabase.from('tags').delete().eq('transcription_id', selectedId);

        // 2. Insert new tags
        const tagsToInsert = editedTags.map(t => ({
            transcription_id: selectedId,
            tag_name: t
        }));

        if (tagsToInsert.length > 0) {
            await supabase.from('tags').insert(tagsToInsert);
        }

        alert('Tags mis à jour !');
        fetchData(); // Refresh
        setSelectedId(null);
    };

    return (
        <div className="min-h-screen bg-[#F3F5F7] p-8 font-sans">
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <div className="flex items-center gap-4 mb-8">
                    <button onClick={onBack} className="p-2 bg-white rounded-full hover:bg-gray-50 transition border border-gray-200">
                        <ArrowLeft size={20} className="text-gray-600" />
                    </button>
                    <div>
                        <h1 className="text-2xl font-bold text-[#111]">Analyse & Amélioration</h1>
                        <p className="text-sm text-gray-500">Nettoyage des transcripts • Gestion des Tags IA</p>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* LIST */}
                    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col h-[70vh]">
                        <div className="p-4 border-b border-gray-100 bg-gray-50/50">
                            <h3 className="font-semibold text-gray-700">Transcriptions Récentes</h3>
                        </div>
                        <div className="overflow-y-auto flex-1 p-2 space-y-2">
                            {loading ? <p className="p-4 text-center text-gray-400">Chargement...</p> :
                                transcriptions.map(t => (
                                    <div
                                        key={t.id}
                                        onClick={() => handleSelect(t)}
                                        className={`p-3 rounded-xl cursor-pointer transition border ${selectedId === t.id ? 'bg-orange-50 border-[#C87961]' : 'bg-white border-gray-100 hover:border-gray-200 hover:bg-gray-50'}`}
                                    >
                                        <div className="flex justify-between items-start mb-1">
                                            <span className="font-bold text-sm text-[#111]">{t.client_name}</span>
                                            <span className="text-[10px] bg-gray-100 px-1.5 py-0.5 rounded text-gray-500">{t.tags.length} tags</span>
                                        </div>
                                        <p className="text-xs text-gray-500 line-clamp-2">{t.content_summary}</p>
                                    </div>
                                ))}
                        </div>
                    </div>

                    {/* EDITOR */}
                    <div className="lg:col-span-2 flex flex-col gap-6">
                        {selectedId ? (
                            <>
                                <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
                                    <div className="flex items-center gap-2 mb-4">
                                        <Edit3 size={18} className="text-[#C87961]" />
                                        <h3 className="font-bold text-lg">Édition des Tags</h3>
                                    </div>

                                    {/* Existing Tags */}
                                    <div className="flex flex-wrap gap-2 mb-6">
                                        {editedTags.map(tag => (
                                            <span key={tag} className="px-3 py-1.5 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium flex items-center gap-2 group">
                                                {tag}
                                                <button onClick={() => handleRemoveTag(tag)} className="text-gray-400 hover:text-red-500"><X size={14} /></button>
                                            </span>
                                        ))}
                                    </div>

                                    {/* Add Tag */}
                                    <div className="flex gap-2">
                                        <input
                                            type="text"
                                            value={newTag}
                                            onChange={(e) => setNewTag(e.target.value)}
                                            onKeyDown={(e) => e.key === 'Enter' && handleAddTag()}
                                            placeholder="Nouveau tag..."
                                            className="flex-1 px-4 py-2 rounded-xl border border-gray-200 focus:outline-none focus:border-[#C87961] focus:ring-1 focus:ring-[#C87961]"
                                        />
                                        <button onClick={handleAddTag} className="px-4 py-2 bg-gray-900 text-white rounded-xl font-medium hover:bg-gray-800">Ajouter</button>
                                    </div>
                                </div>

                                <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex-1">
                                    <h3 className="font-bold text-lg mb-4">Transcription Nettoyée (Preview)</h3>
                                    <div className="bg-gray-50 p-4 rounded-xl text-sm leading-relaxed text-gray-700 h-64 overflow-y-auto border border-gray-100">
                                        {transcriptions.find(t => t.id === selectedId)?.raw_text || "Aucun contenu brut disponible."}
                                    </div>
                                    <div className="mt-6 flex justify-end">
                                        <button onClick={handleSave} className="px-6 py-3 bg-[#C87961] text-white rounded-xl font-bold hover:bg-[#B06851] transition flex items-center gap-2">
                                            <Save size={18} /> Sauvegarder les modifications
                                        </button>
                                    </div>
                                </div>
                            </>
                        ) : (
                            <div className="h-full bg-white rounded-2xl border border-gray-100 border-dashed flex flex-col items-center justify-center text-gray-400 p-10">
                                <Tag size={48} className="mb-4 opacity-20" />
                                <p>Sélectionnez une transcription pour l'analyser</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
