import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, FileType } from 'lucide-react';
import { motion } from 'framer-motion';

export function Uploader({ onUploadSuccess }) {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    if (!file.name.endsWith('.csv')) {
      setError('Only CSV files are supported.');
      return;
    }

    setIsUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    const baseUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8080';

    try {
      const response = await fetch(`${baseUrl}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to upload file');
      }

      const data = await response.json();
      onUploadSuccess(data.job_id, data.filename);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setIsUploading(false);
    }
  }, [onUploadSuccess]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
    },
    maxFiles: 1,
  });

  return (
    <motion.div 
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
      className="w-full max-w-md mx-auto mt-10"
    >
      <div
        {...getRootProps()}
        className={`border border-white/10 rounded-2xl p-10 flex flex-col items-center justify-center cursor-pointer bg-futuristic-card/60 backdrop-blur-md transition-all duration-300 ${
          isDragActive 
            ? 'border-neon-green shadow-[0_0_24px_rgba(0,255,136,0.15)] bg-neon-green/5' 
            : 'hover:border-neon-green/50 hover:shadow-[0_0_20px_rgba(0,255,136,0.08)] hover:scale-[1.02]'
        }`}
      >
        <input {...getInputProps()} />
        {isUploading ? (
          <div className="flex flex-col items-center">
            <UploadCloud className="w-12 h-12 text-neon-green mb-4 animate-bounce" />
            <p className="text-white font-medium font-display tracking-wider uppercase text-sm">Uploading Matrix...</p>
          </div>
        ) : (
          <>
            <motion.div
              animate={{ y: [0, -6, 0] }}
              transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
            >
              <FileType className="w-12 h-12 text-neon-green mb-4" />
            </motion.div>
            <p className="text-center text-white font-medium mb-1 text-sm tracking-wide">
              Drag & drop a CSV file here
            </p>
            <p className="text-center text-gray-400 text-xs">
              or click to upload from local drive
            </p>
          </>
        )}
      </div>
      {error && (
        <motion.p 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-red-400 text-xs mt-3 text-center font-mono border border-red-500/20 bg-red-500/5 py-2 px-3 rounded-lg"
        >
          {error}
        </motion.p>
      )}
    </motion.div>
  );
}
