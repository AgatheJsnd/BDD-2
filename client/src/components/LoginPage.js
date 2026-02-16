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
    <div className="min-h-screen w-full relative flex items-center justify-center p-4" style={{ fontFamily: "'Plus Jakarta Sans', sans-serif" }}>
      <div
        className="absolute inset-0"
        style={{
          backgroundImage: 'url("/assets/images/background.png")',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          filter: 'saturate(0.88)',
        }}
      />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative bg-[#f8f8f8] rounded-[22px] shadow-2xl p-7 md:p-8 w-full max-w-[410px] flex flex-col items-center border border-[#ececec]"
      >
        <div className="mb-5 mt-1 text-center">
          <div className="h-[76px] w-[76px] rounded-full border border-black bg-white mx-auto mb-2 overflow-hidden flex items-center justify-center">
            <img src="/assets/images/loewe_logo.png" alt="Loewe logo" className="w-[108%] h-[108%] object-contain" />
          </div>
          <p className="font-serif text-[40px] text-[#111] leading-none tracking-wide">LOEWE</p>
        </div>

        <form onSubmit={handleSubmit} className="w-full flex flex-col gap-3">
          <div className="relative">
            <label
              className="block text-[12px] tracking-[0.08em] text-[#4f4f4f] mb-1.5 uppercase"
              style={{ fontFamily: '"Times New Roman", Times, serif', fontWeight: 700 }}
            >
              UTILISATEUR
            </label>
            <User className="absolute left-3 top-[35px] text-gray-400" size={16} />
            <input
              type="text"
              placeholder="Analyste / Vendeur"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full pl-9 pr-4 py-2.5 rounded-[8px] bg-white border border-[#e1e1e1] focus:outline-none focus:ring-2 focus:ring-black/10 transition text-[#1A1A1A] text-sm placeholder:text-[#a1a1aa]"
            />
          </div>

          <div className="relative">
            <label
              className="block text-[12px] tracking-[0.08em] text-[#4f4f4f] mb-1.5 uppercase"
              style={{ fontFamily: '"Times New Roman", Times, serif', fontWeight: 700 }}
            >
              MOT DE PASSE
            </label>
            <Lock className="absolute left-3 top-[35px] text-gray-400" size={16} />
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full pl-9 pr-4 py-2.5 rounded-[8px] bg-white border border-[#e1e1e1] focus:outline-none focus:ring-2 focus:ring-black/10 transition text-[#1A1A1A] text-sm placeholder:text-[#a1a1aa]"
            />
          </div>

          {error && (
            <div className="flex items-center gap-2 text-red-500 text-xs bg-red-50 p-2.5 rounded-lg">
              <AlertCircle size={16} />
              {error}
            </div>
          )}

          <button
            type="submit"
            className="mt-3 w-full bg-black text-white font-semibold py-2.5 rounded-[9px] hover:bg-[#1f1f1f] transition-colors"
          >
            Se connecter
          </button>
        </form>

        <button
          type="button"
          onClick={() => setShowHelp((v) => !v)}
          className="mt-3 w-full flex items-center justify-center gap-3 text-[11px] tracking-[0.2em] text-[#666]"
        >
          <span className="h-px flex-1 bg-[#d4d4d8]" />
          <span>AIDE</span>
          <span className="h-px flex-1 bg-[#d4d4d8]" />
        </button>
        {showHelp && (
          <div className="mt-2 w-full rounded-[8px] bg-white border border-[#e4e4e7] p-2.5 text-[11px] text-gray-700 text-center">
            {`ANALYSTE: ${analystUsername} / ${analystPassword}`}
            <br />
            {`VENDEUR: ${vendeurUsername} / ${vendeurPassword}`}
          </div>
        )}
      </motion.div>
    </div>
  );
}
