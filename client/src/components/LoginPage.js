import React, { useState } from 'react';
import { User, Lock, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';

export default function LoginPage({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [showHelp, setShowHelp] = useState(false);
  const analystUsername = (process.env.REACT_APP_ANALYSTE_USERNAME || 'analyste').trim().toLowerCase();
  const analystPassword = (process.env.REACT_APP_ANALYSTE_PASSWORD || 'analyste123').trim();
  const vendeurUsername = (process.env.REACT_APP_VENDEUR_USERNAME || 'vendeur').trim().toLowerCase();
  const vendeurPassword = (process.env.REACT_APP_VENDEUR_PASSWORD || 'vendeur123').trim();

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    const inputUsername = username.trim().toLowerCase();
    const inputPassword = password.trim();

    if (inputUsername === analystUsername && inputPassword === analystPassword) {
      onLogin('analyste');
    } else if (inputUsername === vendeurUsername && inputPassword === vendeurPassword) {
      onLogin('vendeur');
    } else {
      setError('Identifiants incorrects.');
    }
  };

  return (
    <div className="min-h-screen w-full bg-[#E8D5CF] flex items-center justify-center p-4" style={{ fontFamily: "'Plus Jakarta Sans', sans-serif" }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative bg-[#f8f8f8] rounded-[22px] shadow-2xl p-7 md:p-8 w-full max-w-[410px] flex flex-col items-center border border-[#ececec]"
      >
        {/* Background Decoration */}
        <div className="absolute top-0 left-0 w-full h-2 bg-[#C87961]" />

        {/* Logo / Branding */}
        <div className="mb-10 text-center">
          <p className="font-bold text-[14px] tracking-[0.2em] text-[#C87961] mb-2 uppercase">MAISON LVMH</p>
          <h1 className="font-serif text-[32px] md:text-[40px] leading-tight text-[#1A1A1A]">
            Connexion
          </h1>
          <p className="text-gray-400 mt-2 font-light italic">Accès sécurisé à la plateforme d'analyse</p>
        </div>

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="w-full flex flex-col gap-4">

          {/* Username */}
          <div className="relative">
            <User className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              placeholder="Nom d'utilisateur"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full pl-11 pr-4 py-3 rounded-[12px] bg-white border border-[#e1e1e1] focus:outline-none focus:ring-2 focus:ring-[#C87961]/20 focus:border-[#C87961] transition text-[#1A1A1A] text-sm placeholder:text-[#a1a1aa]"
            />
          </div>

          <div className="relative">
            <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="password"
              placeholder="Mot de passe"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full pl-11 pr-4 py-3 rounded-[12px] bg-white border border-[#e1e1e1] focus:outline-none focus:ring-2 focus:ring-[#C87961]/20 focus:border-[#C87961] transition text-[#1A1A1A] text-sm placeholder:text-[#a1a1aa]"
            />
          </div>

          {error && (
            <div className="flex items-center gap-2 text-red-500 text-xs bg-red-50 p-2.5 rounded-lg border border-red-100">
              <AlertCircle size={16} />
              {error}
            </div>
          )}

          <button
            type="submit"
            className="mt-3 w-full bg-[#1A1A1A] text-white font-semibold py-3.5 rounded-[12px] hover:bg-black transition-all shadow-lg shadow-black/5 active:scale-[0.98]"
          >
            Se connecter
          </button>
        </form>

        <button
          type="button"
          onClick={() => setShowHelp((v) => !v)}
          className="mt-6 w-full flex items-center justify-center gap-4 text-[10px] tracking-[0.2em] text-gray-400 hover:text-gray-600 transition-colors"
        >
          <span className="h-px flex-1 bg-gray-200" />
          <span>BESOIN D'AIDE ?</span>
          <span className="h-px flex-1 bg-gray-200" />
        </button>
        {showHelp && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            className="mt-4 w-full rounded-xl bg-gray-50 border border-gray-100 p-4 text-[11px] text-gray-600 space-y-1"
          >
            <div className="flex justify-between">
              <span className="font-bold">ANALYSTE:</span>
              <span className="font-mono">{analystUsername} / {analystPassword}</span>
            </div>
            <div className="flex justify-between">
              <span className="font-bold">VENDEUR:</span>
              <span className="font-mono">{vendeurUsername} / {vendeurPassword}</span>
            </div>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
}
