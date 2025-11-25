import { useState, useCallback, useEffect, useRef } from 'react';
import { JobStatus } from '../services/api';

export interface UseFileConverterOptions {
  uploadFn: (file: File) => Promise<{ job_id: string; status: string; message: string }>;
  getStatusFn: (jobId: string) => Promise<JobStatus>;
  pollInterval?: number;
}

export interface UseFileConverterResult {
  file: File | null;
  jobId: string | null;
  status: JobStatus | null;
  uploading: boolean;
  error: string | null;
  handleFileChange: (file: File | null) => void;
  handleUpload: () => Promise<void>;
  handleReset: () => void;
}

export const useFileConverter = ({
  uploadFn,
  getStatusFn,
  pollInterval = 2000,
}: UseFileConverterOptions): UseFileConverterResult => {
  const [file, setFile] = useState<File | null>(null);
  const [jobId, setJobId] = useState<string | null>(null);
  const [status, setStatus] = useState<JobStatus | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const pollingRef = useRef<NodeJS.Timeout | null>(null);

  const stopPolling = useCallback(() => {
    if (pollingRef.current) {
      clearTimeout(pollingRef.current);
      pollingRef.current = null;
    }
  }, []);

  const pollJobStatus = useCallback(
    async (id: string) => {
      try {
        const jobStatus = await getStatusFn(id);
        setStatus(jobStatus);

        if (jobStatus.status === 'completed' || jobStatus.status === 'failed') {
          setUploading(false);
          stopPolling();
          
          if (jobStatus.status === 'failed') {
            setError(jobStatus.error || 'Processing failed');
          }
        } else {
          // Continue polling
          pollingRef.current = setTimeout(() => pollJobStatus(id), pollInterval);
        }
      } catch (err: any) {
        setError('Failed to check job status');
        setUploading(false);
        stopPolling();
      }
    },
    [getStatusFn, pollInterval, stopPolling]
  );

  const handleFileChange = useCallback((newFile: File | null) => {
    setFile(newFile);
    setError(null);
    setJobId(null);
    setStatus(null);
  }, []);

  const handleUpload = useCallback(async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const response = await uploadFn(file);
      setJobId(response.job_id);
      pollJobStatus(response.job_id);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload file');
      setUploading(false);
    }
  }, [file, uploadFn, pollJobStatus]);

  const handleReset = useCallback(() => {
    stopPolling();
    setFile(null);
    setJobId(null);
    setStatus(null);
    setError(null);
    setUploading(false);
  }, [stopPolling]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopPolling();
    };
  }, [stopPolling]);

  return {
    file,
    jobId,
    status,
    uploading,
    error,
    handleFileChange,
    handleUpload,
    handleReset,
  };
};
