import React, { useState, useRef, useEffect } from 'react';
import { Uploader } from './components/Uploader';
import { AgentLog } from './components/AgentLog';
import { ReportView } from './components/ReportView';
import { useAgentStream } from './hooks/useAgentStream';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Activity, Terminal, Cpu, Database, 
  MessageSquare, ChevronDown, Check, AlertCircle, 
  RefreshCw, X, Play, Shield, Globe, Award, Settings
} from 'lucide-react';

function App() {
  const [appState, setAppState] = useState('idle'); // 'idle', 'running', 'done'
  const [jobId, setJobId] = useState(null);
  const [filename, setFilename] = useState('');
  const [scrolled, setScrolled] = useState(false);

  const uploadSectionRef = useRef(null);
  
  const { thoughts, isStreaming, isDone, reportData, error, startStream } = useAgentStream();

  // Handle header glassmorphism on scroll
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleUploadSuccess = (id, name) => {
    setJobId(id);
    setFilename(name);
    // Smoothly scroll down to the matrix analysis actions
    setTimeout(() => {
      scrollToMatrix();
    }, 400);
  };

  const handleRunAnalysis = () => {
    if (!jobId) return;
    setAppState('running');
    startStream(jobId);
  };

  // When agent finishes successfully, redirect to the HTML report directly
  useEffect(() => {
    if (isDone && !isStreaming && jobId) {
      setAppState('done');
      const baseUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8080';
      window.location.href = `${baseUrl}/report/${jobId}/html`;
    }
  }, [isDone, isStreaming, jobId]);

  // If there's an error and we are not streaming, revert or show error
  useEffect(() => {
    if (error) {
      setAppState('done');
    }
  }, [error]);

  const scrollToMatrix = () => {
    uploadSectionRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleStartOver = () => {
    setAppState('idle');
    setJobId(null);
    setFilename('');
  };

  // Animation variants
  const fadeInUp = {
    hidden: { opacity: 0, y: 30 },
    visible: { 
      opacity: 1, 
      y: 0, 
      transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] } 
    }
  };

  const staggerContainer = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.1
      }
    }
  };

  return (
    <div className="min-h-screen bg-black text-white font-sans selection:bg-neon-green selection:text-black relative overflow-x-hidden">
      
      {/* Background visual components */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.012)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.012)_1px,transparent_1px)] bg-[size:40px_40px] pointer-events-none z-0"></div>
      
      {/* Breathing neon radial glow behind content */}
      <div className="absolute top-[20%] left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full pointer-events-none radial-glow opacity-75 z-0 animate-pulse-slow"></div>
      <div className="absolute bottom-[10%] right-[-10%] w-[400px] h-[400px] rounded-full pointer-events-none radial-glow opacity-30 z-0"></div>

      {/* Margins - Telemetry Data (Visible on Lg viewports) */}
      <div className="hidden lg:flex fixed left-6 bottom-10 z-20 flex-col items-center space-y-6 pointer-events-auto">
        <div className="flex flex-col space-y-4">
          <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="text-gray-500 hover:text-neon-green transition-colors duration-200" aria-label="GitHub">
            <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.385.6.11.82-.26.82-.577v-2.234c-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.43.372.82 1.102.82 2.222v3.293c0 .319.22.694.825.576C20.565 21.795 24 17.3 24 12c0-6.63-5.37-12-12-12z" />
            </svg>
          </a>
          <a href="#" className="text-gray-500 hover:text-neon-green transition-colors duration-200">
            <MessageSquare className="w-4 h-4" />
          </a>
        </div>
        <div className="h-20 w-[1px] bg-white/10"></div>
        <span className="text-[9px] font-mono text-gray-500 tracking-[0.3em] uppercase [writing-mode:vertical-lr] select-none">
          SYS.NODE.CONNECT // SECURE
        </span>
      </div>

      <div className="hidden lg:flex fixed right-6 bottom-10 z-20 flex-col items-center space-y-6 select-none pointer-events-none">
        <span className="text-[9px] font-mono text-neon-green tracking-[0.3em] uppercase [writing-mode:vertical-lr]">
          MATRIX_V1.0 // STABLE
        </span>
        <div className="h-20 w-[1px] bg-neon-green/20"></div>
        <div className="flex flex-col items-center space-y-2">
          <span className="w-1.5 h-1.5 rounded-full bg-neon-green animate-ping"></span>
          <span className="text-[8px] font-mono text-gray-500">SYS_OK</span>
        </div>
      </div>

      {/* Transparent Sticky Navbar */}
      <header className={`fixed top-0 left-0 right-0 z-30 transition-all duration-300 ${
        scrolled ? 'bg-black/60 border-b border-white/10 backdrop-blur-md py-4' : 'bg-transparent py-6'
      }`}>
        <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center space-x-3 cursor-pointer"
            onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          >
            <div className="p-2 border border-neon-green/30 rounded-lg bg-black relative overflow-hidden group">
              <Cpu className="text-neon-green w-5 h-5 relative z-10 transition-transform group-hover:rotate-90 duration-500" />
              <div className="absolute inset-0 bg-neon-green/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
            </div>
            <span className="font-display font-black text-sm tracking-[0.25em] uppercase text-white">
              Neural<span className="text-neon-green">Analyst</span>
            </span>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, x: 25 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center space-x-4"
          >
            {appState === 'running' && (
              <div className="flex items-center space-x-2 text-neon-green border border-neon-green/20 bg-neon-green/5 rounded-full px-3 py-1 text-[10px] font-mono tracking-widest uppercase">
                <Activity className="w-3.5 h-3.5 animate-spin" />
                <span>Processing Matrix</span>
              </div>
            )}
          </motion.div>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10">
        
        {/* IDLE STATE (Hero & Upload Sections) */}
        {appState === 'idle' && (
          <div>
            {/* Hero Section */}
            <section className="h-screen w-full flex flex-col justify-center items-center px-6 relative">
              <motion.div 
                variants={staggerContainer}
                initial="hidden"
                animate="visible"
                className="max-w-4xl text-center flex flex-col items-center"
              >
                {/* Glowing Top Pill */}
                <motion.div 
                  variants={fadeInUp}
                  className="mb-6 flex items-center space-x-2 px-4 py-1.5 border border-neon-green/30 bg-neon-green/5 rounded-full"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-neon-green animate-ping"></span>
                  <span className="text-[10px] font-mono text-neon-green tracking-[0.2em] uppercase">Autonomous AI Analytics Agent</span>
                </motion.div>

                {/* Big Display Title */}
                <motion.h1 
                  variants={fadeInUp}
                  className="text-4xl sm:text-6xl md:text-7xl font-display font-extrabold tracking-[0.25em] uppercase text-white leading-[1.15]"
                >
                  Neural <span className="text-transparent bg-clip-text bg-gradient-to-r from-neon-green via-emerald-400 to-teal-400 font-black">Matrix</span>
                </motion.h1>
                
                {/* Subtitle */}
                <motion.p 
                  variants={fadeInUp}
                  className="text-gray-400 text-sm sm:text-base md:text-lg max-w-2xl mt-8 font-light leading-relaxed tracking-wide"
                >
                  Upload dataset matrix. Our custom autonomous neural pipeline runs pattern recognition code, designs live charts, and generates executive summaries in milliseconds.
                </motion.p>
                
                {/* Double CTA Buttons */}
                <motion.div 
                  variants={fadeInUp}
                  className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-5 mt-10"
                >
                  <button
                    onClick={scrollToMatrix}
                    className="group bg-neon-green hover:bg-[#39ff14] text-black font-semibold tracking-wider font-mono text-xs uppercase px-8 py-3.5 rounded-full shadow-[0_0_20px_rgba(0,255,136,0.25)] hover:shadow-[0_0_30px_rgba(0,255,136,0.45)] transition-all duration-300 flex items-center space-x-2"
                  >
                    <span>Upload Dataset</span>
                    <Play className="w-3.5 h-3.5 fill-black transition-transform group-hover:translate-x-1" />
                  </button>
                </motion.div>
              </motion.div>
            </section>

            {/* Matrix Upload Section */}
            <section 
              ref={uploadSectionRef} 
              className="min-h-[80vh] w-full flex flex-col items-center justify-center py-20 px-6 bg-black relative"
            >
              <div className="absolute inset-0 bg-gradient-to-b from-transparent via-neutral-950/40 to-transparent pointer-events-none"></div>
              
              <div className="max-w-4xl w-full text-center relative z-10">
                <div className="flex flex-col items-center mb-8">
                  <Database className="w-10 h-10 text-neon-green mb-4 p-2 border border-neon-green/30 rounded-xl bg-neon-green/5 shadow-[0_0_15px_rgba(0,255,136,0.1)]" />
                  <h2 className="text-xl sm:text-2xl font-display font-bold tracking-[0.2em] uppercase text-white">Initialize Analysis Matrix</h2>
                  <div className="w-12 h-[1px] bg-neon-green/40 mt-3"></div>
                </div>

                {!jobId ? (
                  <Uploader onUploadSuccess={handleUploadSuccess} />
                ) : (
                  <motion.div 
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="w-full max-w-md mx-auto mt-6 p-8 border border-neon-green bg-black/60 rounded-2xl shadow-[0_0_30px_rgba(0,255,136,0.1)] backdrop-blur-md relative overflow-hidden"
                  >
                    {/* Corner border highlights */}
                    <div className="absolute top-0 left-0 w-4 h-4 border-t-2 border-l-2 border-neon-green"></div>
                    <div className="absolute top-0 right-0 w-4 h-4 border-t-2 border-r-2 border-neon-green"></div>
                    <div className="absolute bottom-0 left-0 w-4 h-4 border-b-2 border-l-2 border-neon-green"></div>
                    <div className="absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 border-neon-green"></div>
                    
                    <div className="flex flex-col items-center">
                      <div className="flex items-center space-x-3 mb-6">
                        <Check className="w-5 h-5 text-neon-green border border-neon-green/20 rounded-full p-0.5 bg-neon-green/5" />
                        <span className="font-mono text-sm tracking-wider text-gray-200 truncate max-w-[240px]">{filename} loaded</span>
                      </div>
                      
                      <div className="w-full h-[1px] bg-white/10 my-4"></div>

                      <button
                        onClick={handleRunAnalysis}
                        className="w-full group bg-neon-green hover:bg-[#39ff14] text-black font-mono font-bold tracking-widest text-xs uppercase py-4 rounded-xl shadow-[0_0_20px_rgba(0,255,136,0.15)] hover:shadow-[0_0_30px_rgba(0,255,136,0.35)] transition-all duration-300 flex items-center justify-center space-x-3"
                      >
                        <Terminal className="w-4 h-4 fill-black" />
                        <span>Run Data Analysis Pipeline</span>
                      </button>
                      
                      <button 
                        onClick={handleStartOver}
                        className="text-gray-500 hover:text-white font-mono text-[10px] tracking-wider uppercase mt-4 transition-colors"
                      >
                        Reset Matrix Upload
                      </button>
                    </div>
                  </motion.div>
                )}
              </div>
            </section>
          </div>
        )}

        {/* RUNNING STATE */}
        {appState === 'running' && (
          <section className="min-h-screen w-full flex flex-col items-center justify-center pt-28 pb-16 px-6 relative">
            <div className="max-w-4xl w-full text-center relative z-10 flex flex-col items-center">
              <div className="flex items-center space-x-3 mb-3">
                <span className="w-2 h-2 bg-neon-green rounded-full animate-ping"></span>
                <h2 className="text-xl sm:text-2xl font-display font-bold tracking-[0.2em] text-neon-green uppercase">
                  Neural Pipeline Active
                </h2>
              </div>
              <p className="text-gray-400 font-mono text-xs tracking-wider mb-8">
                COMPILING CORE METRICS // PARSING {filename.toUpperCase()}
              </p>
              
              <div className="w-full relative">
                {/* Horizontal futuristic line scan indicator */}
                <div className="absolute left-0 right-0 h-[1px] bg-neon-green/20 top-0 overflow-hidden">
                  <div className="w-1/3 h-full bg-gradient-to-r from-transparent via-neon-green to-transparent animate-[pan_2s_linear_infinite]"></div>
                </div>
                
                <AgentLog thoughts={thoughts} isStreaming={isStreaming} />
              </div>
            </div>
          </section>
        )}

        {/* DONE STATE (Direct fallback if redirection fails or delays) */}
        {appState === 'done' && (
          <section className="min-h-screen w-full pt-28 pb-20 px-6">
            <div className="max-w-5xl mx-auto flex flex-col items-center">
              {error ? (
                <motion.div 
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="p-8 border border-red-500/30 bg-red-950/20 rounded-2xl max-w-xl text-center backdrop-blur-md relative"
                >
                  <AlertCircle className="w-12 h-12 text-red-400 mx-auto mb-4" />
                  <h2 className="text-xl font-display font-bold text-red-400 mb-3 tracking-widest uppercase">Pipeline Interrupted</h2>
                  <p className="text-gray-400 font-mono text-xs leading-relaxed mb-6">{error}</p>
                  <button 
                    onClick={handleStartOver}
                    className="border border-white/20 hover:border-neon-green hover:text-neon-green font-mono text-xs px-6 py-2.5 rounded-full transition-all"
                  >
                    Start New Session
                  </button>
                </motion.div>
              ) : (
                <>
                  <div className="flex flex-col items-center space-y-2 mb-8 text-center">
                    <div className="flex items-center space-x-3">
                      <div className="w-3 h-3 bg-neon-green rounded-full shadow-[0_0_8px_rgba(0,255,136,1)]"></div>
                      <h2 className="text-2xl font-display font-extrabold tracking-[0.2em] uppercase">Pipeline Finalized</h2>
                    </div>
                    <p className="text-gray-400 text-xs font-mono">HTML REPORT REDIRECTION ENGAGED</p>
                  </div>
                  <ReportView reportData={reportData} jobId={jobId} />
                </>
              )}
              
              {/* Show log below report for reference */}
              {!error && thoughts.length > 0 && (
                <div className="mt-12 w-full max-w-4xl border-t border-white/10 pt-10">
                  <h3 className="text-gray-500 font-mono text-xs uppercase tracking-[0.25em] mb-4 text-center">Neural Trace Archive</h3>
                  <AgentLog thoughts={thoughts} isStreaming={false} />
                </div>
              )}
            </div>
          </section>
        )}

      </main>
      
      {/* Scroll animation styles injected for specific keyframes */}
      <style>{`
        @keyframes pan {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(300%); }
        }
      `}</style>
    </div>
  );
}

export default App;
