import React from 'react';
import ReactMarkdown from 'react-markdown';
import { ChartCard } from './ChartCard';

export function ReportView({ reportData, jobId }) {
  if (!reportData) return null;

  return (
    <div className="w-full max-w-5xl mx-auto mt-10 space-y-10 pb-20">
      
      {/* Charts Grid */}
      {reportData.charts && reportData.charts.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-terminal-green border-b border-terminal-border pb-2">Generated Visualizations</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {reportData.charts.map((chart, idx) => (
              <ChartCard key={idx} chart={chart} />
            ))}
          </div>
        </div>
      )}

      {/* Markdown Report */}
      <div className="bg-[#111] border border-[#333] rounded-lg p-8 shadow-xl">
        <div className="markdown-content">
          <ReactMarkdown>
            {reportData.report_markdown}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
}
