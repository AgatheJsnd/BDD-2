import React from 'react';
import { ArrowLeft } from 'lucide-react';

export default function StatsPage({ onBack }) {
    return (
        <div className="min-h-screen bg-[#F3F5F7] p-8 font-sans flex flex-col">
            <div className="max-w-6xl mx-auto w-full">
                {/* Header */}
                <div className="flex items-center gap-4 mb-8">
                    <button onClick={onBack} className="p-2 bg-white rounded-full hover:bg-gray-50 transition border border-gray-200">
                        <ArrowLeft size={20} className="text-gray-600" />
                    </button>
                    <div>
                        <h1 className="text-2xl font-bold text-[#111]">Statistiques</h1>
                        <p className="text-sm text-gray-500">Page en construction</p>
                    </div>
                </div>

                {/* Blank Content */}
                <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-10 h-[60vh] flex items-center justify-center">
                    <p className="text-gray-400 italic">Contenu à venir...</p>
                </div>
            </div>
        </div>
    );
}
