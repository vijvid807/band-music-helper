import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface JobStatus {
  type: string;
  status: string;
  filename: string;
  upload_path: string;
  output_path: string | null;
  error: string | null;
  step?: string | null;
  progress?: number;
}

export interface UploadResponse {
  job_id: string;
  status: string;
  message: string;
}

export const bandMusicAPI = {
  // OMR Endpoints
  uploadImageForOMR: async (file: File, instrument: string = 'piano'): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post(`/api/omr/upload?instrument=${encodeURIComponent(instrument)}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  getOMRStatus: async (jobId: string): Promise<JobStatus> => {
    const response = await api.get(`/api/omr/status/${jobId}`);
    return response.data;
  },

  downloadOMRResult: (jobId: string): string => {
    return `${API_BASE_URL}/api/omr/download/${jobId}`;
  },

  // AMT Endpoints
  uploadAudioForAMT: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/api/amt/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  getAMTStatus: async (jobId: string): Promise<JobStatus> => {
    const response = await api.get(`/api/amt/status/${jobId}`);
    return response.data;
  },

  downloadAMTResult: (jobId: string): string => {
    return `${API_BASE_URL}/api/amt/download/${jobId}`;
  },

  // Health Check
  healthCheck: async (): Promise<{ status: string; service: string }> => {
    const response = await api.get('/api/health');
    return response.data;
  },
};

export default bandMusicAPI;
