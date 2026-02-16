import React, { useState } from 'react';
import { User, Lock, ArrowRight, AlertCircle } from 'lucide-react';
import { motion } from 'framer-motion';

export default function LoginPage({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    // Hardcoded Credentials (matching Python version)
    if (username === 'analyste' && password === 'analyste123') {
      onLogin('analyste');
    } else if (username === 'vendeur' && password === 'vendeur123') {
      onLogin('vendeur');
    } else {
      setError('Identifiants incorrects. Essayez "analyste" / "analyste123"');
    }
  };

  return (
    <div className="min-h-screen w-full bg-[#E8D5CF] flex items-center justify-center p-4" style={{ fontFamily: "'Plus Jakarta Sans', sans-serif" }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-[40px] shadow-2xl p-10 md:p-14 w-full max-w-lg flex flex-col items-center text-center relative overflow-hidden"
      >
        {/* Background Decoration */}
        <div className="absolute top-0 left-0 w-full h-2 bg-[#C87961]" />

        {/* Logo / Branding */}
        <div className="mb-10">
          <p className="font-bold text-[14px] tracking-[0.2em] text-[#C87961] mb-2">MAISON LVMH</p>
          <h1 className="font-serif text-[32px] md:text-[40px] leading-tight text-[#1A1A1A]">
            Connexion
          </h1>
          <p className="text-gray-400 mt-2 font-light italic">Accès sécurisé à la plateforme</p>
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
              className="w-full pl-12 pr-4 py-4 rounded-xl bg-gray-50 border border-gray-100 focus:outline-none focus:ring-2 focus:ring-[#C87961]/20 focus:border-[#C87961] transition text-[#1A1A1A] font-medium placeholder:text-gray-400"
            />
          </div>

          {/* Password */}
          <div className="relative">
            <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="password"
              placeholder="Mot de passe"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full pl-12 pr-4 py-4 rounded-xl bg-gray-50 border border-gray-100 focus:outline-none focus:ring-2 focus:ring-[#C87961]/20 focus:border-[#C87961] transition text-[#1A1A1A] font-medium placeholder:text-gray-400"
            />
          </div>

          {/* Error Message */}
          {error && (
            <div className="flex items-center gap-2 text-red-500 text-sm bg-red-50 p-3 rounded-lg">
              <AlertCircle size={16} />
              {error}
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            className="mt-4 w-full bg-[#1A1A1A] text-white font-bold py-4 rounded-xl hover:bg-[#333] transition-colors flex items-center justify-center gap-2 group"
          >
            Se Connecter
            <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
          </button>
        </form>

        <p className="mt-8 text-xs text-gray-300 font-medium tracking-wide">
          ANALYSTE: analyste123 • VENDEUR: vendeur123
        </p>

      </motion.div>
    </div>
  );
}
