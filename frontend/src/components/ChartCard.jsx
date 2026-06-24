import React from 'react';

export function ChartCard({ chart }) {
  return (
    <div className="bg-[#111] border border-terminal-green/20 hover:border-terminal-green/50 rounded-xl p-5 flex flex-col items-center shadow-2xl transition-all duration-300 hover:shadow-terminal-green/5 hover:scale-[1.01]">
      <h3 className="text-terminal-green font-semibold mb-4 text-center text-sm tracking-wider uppercase">{chart.title}</h3>
      <div className="w-full h-auto rounded-lg overflow-hidden border border-[#222] bg-[#070707] p-2">
        <img 
          src={`data:image/png;base64,${chart.base64}`} 
          alt={chart.title}
          className="w-full h-auto object-contain bg-transparent"
        />
      </div>
    </div>
  );
}
