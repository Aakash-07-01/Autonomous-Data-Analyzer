import { useState, useCallback } from 'react';

export function useAgentStream() {
  const [thoughts, setThoughts] = useState([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [isDone, setIsDone] = useState(false);
  const [reportData, setReportData] = useState(null);
  const [error, setError] = useState(null);

  const startStream = useCallback((jobId) => {
    setIsStreaming(true);
    setIsDone(false);
    setThoughts([]);
    setReportData(null);
    setError(null);

    const baseUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8080';
    const eventSource = new EventSource(`${baseUrl}/analyse/${jobId}`);

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        if (data.type === 'thought') {
          setThoughts((prev) => [...prev, data.thought]);
        } else if (data.type === 'done') {
          setReportData({
            findings: data.findings,
            charts: data.charts,
            report_markdown: data.report_markdown,
          });
          setIsDone(true);
          setIsStreaming(false);
          eventSource.close();
        } else if (data.type === 'error') {
          setError(data.message);
          setIsStreaming(false);
          eventSource.close();
        }
      } catch (err) {
        console.error('Failed to parse SSE event', err);
      }
    };

    eventSource.onerror = (err) => {
      console.error('EventSource failed', err);
      setError('Connection to server lost or failed.');
      setIsStreaming(false);
      eventSource.close();
    };
    
    return () => {
      eventSource.close();
    };
  }, []);

  return { thoughts, isStreaming, isDone, reportData, error, startStream };
}
