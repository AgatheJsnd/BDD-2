import React, { useState, useEffect, useRef } from 'react';
import { Mic, Square, Play, Save, History, Settings, LogOut, Loader2, FileAudio, Check, AlertCircle, Trash2 } from 'lucide-react';
import { supabase } from '../supabaseClient';

export default function VendeurPage({ onLogout }) {
    const [activeTab, setActiveTab] = useState('record'); // record | history | config
    const [isRecording, setIsRecording] = useState(false);
    const [audioBlob, setAudioBlob] = useState(null);
    const [transcriptionResult, setTranscriptionResult] = useState(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const [mediaRecorder, setMediaRecorder] = useState(null);
    const audioChunksRef = useRef([]);

    // Form State
    const [clientName, setClientName] = useState('');
    const [clientId, setClientId] = useState('');
    const [saveStatus, setSaveStatus] = useState('idle'); // idle | saving | success | error

    // History State
    const [history, setHistory] = useState([]);

    // ── AUDIO RECORDING ──
    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const recorder = new MediaRecorder(stream);
            audioChunksRef.current = [];

            recorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunksRef.current.push(event.data);
                }
            };

            recorder.onstop = () => {
                const blob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
                setAudioBlob(blob);
            };

            recorder.start();
            setMediaRecorder(recorder);
            setIsRecording(true);
            setAudioBlob(null);
            setTranscriptionResult(null);
        } catch (err) {
            console.error("Error accessing microphone:", err);
            alert("Impossible d'accéder au microphone. Veuillez vérifier vos permissions.");
        }
    };

    const stopRecording = () => {
        if (mediaRecorder && isRecording) {
            mediaRecorder.stop();
            setIsRecording(false);
            // Stop all tracks to release mic
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
        }
    };

    // ── TRANSCRIPTION ──
    const handleTranscribe = async () => {
        if (!audioBlob) return;
        setIsProcessing(true);
        setSaveStatus('idle');

        try {
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.webm');

            // Call backend
            const response = await fetch('/api/transcribe', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) throw new Error("Erreur serveur lors de la transcription");

            const result = await response.json();
            setTranscriptionResult(result);
        } catch (e) {
            console.error(e);
            alert("Erreur de transcription: " + e.message);
        } finally {
            setIsProcessing(false);
        }
    };

    // ── SAVE TO SUPABASE ──
    const handleSave = async () => {
        if (!transcriptionResult || !clientName) return;
        setSaveStatus('saving');

        try {
            // Insert into Supabase
            const { error } = await supabase.from('transcriptions').insert([{
                client_name: clientName,
                content_summary: transcriptionResult.cleaned_text || transcriptionResult.transcription,
                sentiment: 'neutre', // Default, or analyze from tags
                tags: transcriptionResult.tags, // Assuming tags is JSONB compatible
                uploaded_by_user_id: null, // Anonymous for now, or user ID if auth proper
                source_filename: 'vocal_recording.webm',
                raw_text: transcriptionResult.transcription
            }]);

            if (error) throw error;
            setSaveStatus('success');

            // Reset after success
            setTimeout(() => {
                setAudioBlob(null);
                setTranscriptionResult(null);
                setClientName('');
                setClientId('');
                setSaveStatus('idle');
                fetchHistory(); // Refresh history
            }, 2000);

        } catch (e) {
            console.error(e);
            setSaveStatus('error');
        }
    };

    // ── FETCH HISTORY ──
    const fetchHistory = async () => {
        const { data } = await supabase
            .from('transcriptions')
            .select('*')
            .order('created_at', { ascending: false })
            .limit(20);
        if (data) setHistory(data);
    };

    useEffect(() => {
        if (activeTab === 'history') {
            fetchHistory();
        }
    }, [activeTab]);


    return (
        <div className="min-h-screen bg-[#F3F5F7] pb-20 font-sans">

            {/* HEADER */}
            <header className="bg-white px-6 py-4 shadow-sm sticky top-0 z-10 flex justify-between items-center">
                <div>
                    <h1 className="text-xl font-bold text-[#1A1A1A]">Espace Vendeur</h1>
                    <p className="text-xs text-gray-500">Enregistrement & IA</p>
                </div>
                <button onClick={onLogout} className="p-2 bg-gray-100 rounded-full text-gray-600 hover:bg-red-50 hover:text-red-500 transition">
                    <LogOut size={18} />
                </button>
            </header>

            {/* MAIN CONTENT */}
            <main className="p-6 max-w-lg mx-auto">

                {/* TABS */}
                <div className="flex bg-white p-1 rounded-xl shadow-sm mb-6">
                    <button
                        onClick={() => setActiveTab('record')}
                        className={`flex-1 py-2 text-sm font-semibold rounded-lg transition ${activeTab === 'record' ? 'bg-[#C87961] text-white shadow-md' : 'text-gray-500 hover:bg-gray-50'}`}
                    >
                        Micro
                    </button>
                    <button
                        onClick={() => setActiveTab('history')}
                        className={`flex-1 py-2 text-sm font-semibold rounded-lg transition ${activeTab === 'history' ? 'bg-[#C87961] text-white shadow-md' : 'text-gray-500 hover:bg-gray-50'}`}
                    >
                        Historique
                    </button>
                </div>

                {/* TAB 1: RECORD */}
                {activeTab === 'record' && (
                    <div className="flex flex-col gap-6">

                        {/* RECORDER CARD */}
                        <div className="bg-white rounded-3xl shadow-sm p-8 flex flex-col items-center justify-center min-h-[300px] border border-gray-100">

                            {!audioBlob && !isProcessing ? (
                                <>
                                    <div className={`h-32 w-32 rounded-full flex items-center justify-center transition-all duration-500 mb-6 ${isRecording ? 'bg-red-50 shadow-[0_0_0_20px_rgba(254,226,226,0.5)] animate-pulse' : 'bg-gray-50'}`}>
                                        <button
                                            onClick={isRecording ? stopRecording : startRecording}
                                            className={`h-24 w-24 rounded-full flex items-center justify-center shadow-lg transition-transform active:scale-95 ${isRecording ? 'bg-red-500 text-white' : 'bg-[#C87961] text-white'}`}
                                        >
                                            {isRecording ? <Square size={32} fill="currentColor" /> : <Mic size={32} />}
                                        </button>
                                    </div>
                                    <p className="text-gray-400 font-medium text-center">
                                        {isRecording ? "Enregistrement en cours..." : "Appuyez pour enregistrer"}
                                    </p>
                                </>
                            ) : isProcessing ? (
                                <div className="text-center">
                                    <Loader2 size={48} className="animate-spin text-[#C87961] mb-4 mx-auto" />
                                    <p className="text-gray-500 font-medium">Analyse IA en cours...</p>
                                    <p className="text-xs text-gray-400 mt-2">Transcription & Extraction de tags</p>
                                </div>
                            ) : (
                                <div className="w-full">
                                    <div className="bg-gray-50 rounded-2xl p-4 mb-4 flex items-center gap-3">
                                        <div className="h-10 w-10 bg-white rounded-full flex items-center justify-center shadow-sm">
                                            <FileAudio size={20} className="text-[#C87961]" />
                                        </div>
                                        <div className="flex-1">
                                            <p className="text-sm font-bold text-gray-700">Enregistrement terminé</p>
                                            <audio src={URL.createObjectURL(audioBlob)} controls className="h-6 w-full mt-1" />
                                        </div>
                                        <button onClick={() => setAudioBlob(null)} className="p-2 hover:bg-white rounded-full text-gray-400">
                                            <Trash2 size={16} />
                                        </button>
                                    </div>

                                    {!transcriptionResult ? (
                                        <button
                                            onClick={handleTranscribe}
                                            className="w-full py-3 bg-[#1A1A1A] text-white rounded-xl font-bold hover:bg-[#333] transition flex items-center justify-center gap-2"
                                        >
                                            <Loader2 size={18} className="animate-spin" /> Transcrire & Analyser
                                        </button>
                                    ) : (
                                        <div className="animate-in fade-in slide-in-from-bottom duration-500">
                                            <div className="mb-4">
                                                <label className="text-xs font-bold text-gray-400 uppercase tracking-wide">Client</label>
                                                <input
                                                    type="text"
                                                    placeholder="Nom du client (ex: Sophie M.)"
                                                    value={clientName}
                                                    onChange={(e) => setClientName(e.target.value)}
                                                    className="w-full mt-1 p-3 bg-gray-50 rounded-xl border-none focus:ring-2 focus:ring-[#C87961]"
                                                    autoFocus
                                                />
                                            </div>

                                            <div className="bg-orange-50 p-4 rounded-xl border border-orange-100 mb-4">
                                                <h3 className="text-sm font-bold text-orange-800 mb-1">Résumé IA</h3>
                                                <p className="text-sm text-orange-900/80 leading-relaxed">
                                                    {transcriptionResult.cleaned_text || transcriptionResult.transcription}
                                                </p>
                                            </div>

                                            {/* TAGS PREVIEW */}
                                            <div className="flex flex-wrap gap-2 mb-6">
                                                {transcriptionResult.tags && Object.entries(transcriptionResult.tags).map(([key, val]) => (
                                                    val && <span key={key} className="px-2 py-1 bg-white border border-gray-200 rounded-md text-[10px] text-gray-600 font-medium">
                                                        {key}: {Array.isArray(val) ? val.join(', ') : val}
                                                    </span>
                                                ))}
                                            </div>

                                            <button
                                                onClick={handleSave}
                                                disabled={!clientName || saveStatus === 'saving'}
                                                className={`w-full py-3 rounded-xl font-bold transition flex items-center justify-center gap-2 ${saveStatus === 'success' ? 'bg-green-500 text-white' :
                                                    saveStatus === 'error' ? 'bg-red-500 text-white' :
                                                        'bg-[#C87961] text-white hover:bg-[#B06851]'
                                                    }`}
                                            >
                                                {saveStatus === 'saving' ? <Loader2 className="animate-spin" /> :
                                                    saveStatus === 'success' ? <Check /> : <Save size={18} />}
                                                {saveStatus === 'success' ? 'Enregistré !' :
                                                    saveStatus === 'error' ? 'Erreur (Réessayer)' : 'Sauvegarder'}
                                            </button>
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {/* TAB 2: HISTORY */}
                {activeTab === 'history' && (
                    <div className="flex flex-col gap-3">
                        {history.map((item) => (
                            <div key={item.id} className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex items-start justify-between">
                                <div>
                                    <h3 className="font-bold text-[#1A1A1A]">{item.client_name || 'Inconnu'}</h3>
                                    <p className="text-xs text-gray-400 mb-2">{new Date(item.created_at).toLocaleDateString()} à {new Date(item.created_at).toLocaleTimeString()}</p>
                                    <p className="text-sm text-gray-600 line-clamp-2">{item.content_summary}</p>
                                </div>
                                <span className="px-2 py-1 bg-gray-50 rounded-md text-[10px] font-bold text-gray-500">
                                    {item.sentiment || 'N/A'}
                                </span>
                            </div>
                        ))}
                        {history.length === 0 && (
                            <div className="text-center py-10 text-gray-400">
                                <History size={48} className="mx-auto mb-2 opacity-20" />
                                <p>Aucun historique récent</p>
                            </div>
                        )}
                    </div>
                )}

            </main>
        </div>
    );
}
