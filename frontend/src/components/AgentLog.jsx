import React, { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Terminal, Cpu } from 'lucide-react';

export function AgentLog({ thoughts, isStreaming }) {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [thoughts]);

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      className="w-full max-w-4xl mx-auto bg-black/80 border border-neon-green/30 rounded-xl p-6 font-mono text-xs sm:text-sm h-[420px] flex flex-col mt-8 shadow-[0_0_30px_rgba(0,255,136,0.05)] relative overflow-hidden backdrop-blur-md"
    >
      {/* Scanline overlay for that retro-futuristic CRT feel */}
      <div className="absolute inset-0 pointer-events-none scanline opacity-30"></div>
      
      {/* Glow effect at the top */}
      <div className="absolute -top-10 left-1/2 -translate-x-1/2 w-2/3 h-20 bg-neon-green/5 blur-2xl rounded-full pointer-events-none"></div>

      {/* Terminal Header */}
      <div className="flex items-center justify-between border-b border-white/10 pb-4 mb-4 relative z-10">
        <div className="flex items-center space-x-3">
          <div className="flex space-x-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-red-500/80 shadow-[0_0_6px_rgba(239,68,68,0.5)]"></span>
            <span className="w-2.5 h-2.5 rounded-full bg-yellow-500/80 shadow-[0_0_6px_rgba(234,179,8,0.5)]"></span>
            <span className="w-2.5 h-2.5 rounded-full bg-neon-green/80 shadow-[0_0_6px_rgba(0,255,136,0.5)]"></span>
          </div>
          <div className="h-4 w-[1px] bg-white/10 mx-2"></div>
          <div className="flex items-center space-x-2 text-neon-green font-display text-[10px] tracking-[0.2em] uppercase">
            <Cpu className="w-3.5 h-3.5 animate-pulse" />
            <span>Core Logic Monitor</span>
          </div>
        </div>
        <div className="text-[10px] text-gray-500 tracking-wider uppercase font-mono">
          SECURE_STREAM // ACTIVE
        </div>
      </div>
      
      {/* Terminal Output */}
      <div 
        ref={scrollRef} 
        className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar relative z-10 scroll-smooth"
      >
        <AnimatePresence initial={false}>
          {thoughts.map((thought, idx) => {
            let tagColor = 'text-gray-400';
            let tagBg = 'bg-white/5 border-white/10';
            
            if (thought.type === 'ACT') {
              tagColor = 'text-neon-green';
              tagBg = 'bg-neon-green/5 border-neon-green/20';
            } else if (thought.type === 'THINK') {
              tagColor = 'text-amber-400';
              tagBg = 'bg-amber-400/5 border-amber-400/20';
            } else if (thought.type === 'OBS') {
              tagColor = 'text-cyan-400';
              tagBg = 'bg-cyan-400/5 border-cyan-400/20';
            }

            return (
              <motion.div 
                key={idx} 
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3 }}
                className="flex items-start space-x-3 text-left border-l-2 border-white/5 pl-3 hover:border-neon-green/30 transition-colors py-0.5"
              >
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold tracking-wider uppercase border ${tagBg} ${tagColor} min-w-[54px] text-center flex-shrink-0`}>
                  {thought.type}
                </span>
                <span className="text-gray-200 break-words whitespace-pre-wrap flex-1 leading-relaxed text-xs sm:text-sm font-mono selection:bg-neon-green/20">
                  {thought.text}
                </span>
              </motion.div>
            );
          })}
        </AnimatePresence>
        
        {isStreaming && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center pl-3 border-l-2 border-neon-green/30 py-1"
          >
            <div className="flex items-center space-x-2">
              <span className="text-neon-green text-xs font-bold uppercase tracking-wider animate-pulse">Analyzing System Outputs</span>
              <span className="w-1.5 h-3.5 bg-neon-green shadow-[0_0_8px_#00ff88] animate-[pulse_0.8s_infinite] inline-block"></span>
            </div>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}

