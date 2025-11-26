import React from 'react';
import bandMusicAPI from '../services/api';
import { useFileConverter } from '../hooks/useFileConverter';
import { useFileUpload } from '../hooks/useFileUpload';
import { useToast } from '../contexts/ToastContext';
import FileUpload from './common/FileUpload';
import Alert from './common/Alert';
import StatusDisplay from './common/StatusDisplay';
import PipelineInfo from './common/PipelineInfo';

const AMTConverter: React.FC = () => {
  const { showToast } = useToast();
  
  const fileUpload = useFileUpload({
    accept: '.mp3,.wav,.ogg,.m4a',
    maxSize: 100 * 1024 * 1024, // 100MB
  });

  const converter = useFileConverter({
    uploadFn: async (file: File) => {
      return bandMusicAPI.uploadAudioForAMT(file);
    },
    getStatusFn: async (jobId: string) => {
      return bandMusicAPI.getAMTStatus(jobId);
    },
  });

  const handleUpload = async () => {
    if (!fileUpload.file) {
      showToast('Please select a file first', 'error');
      return;
    }
    
    await converter.handleUpload();
    
    if (converter.error) {
      showToast(converter.error, 'error');
    } else {
      showToast('File uploaded successfully! Processing...', 'success');
    }
  };

  const handleDownload = async () => {
    if (!converter.jobId) return;
    
    try {
      const url = bandMusicAPI.downloadAMTResult(converter.jobId);
      window.open(url, '_blank');
      showToast('File download started!', 'success');
    } catch (err) {
      showToast('Failed to download file', 'error');
    }
  };

  const handleReset = () => {
    converter.handleReset();
    fileUpload.clearFile();
  };

  // Sync file state
  React.useEffect(() => {
    converter.handleFileChange(fileUpload.file);
  }, [fileUpload.file]);

  const pipelineSteps = [
    { title: 'Audio Preprocessing', description: 'Normalize and prepare audio for transcription' },
    { title: 'AMT Recognition', description: 'Transcribe audio using Basic Pitch AI' },
    { title: 'MIDI Processing', description: 'Parse and validate transcribed notes' },
    { title: 'MusicXML Conversion', description: 'Convert to MusicXML with music21' },
    { title: 'PDF Rendering', description: 'Generate professional sheet music using LilyPond' },
  ];

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-purple-900">🎵 Music to Sheet</h2>
        <span className="badge-purple">AMT Pipeline</span>
      </div>

      <p className="text-gray-700 mb-6">
        Upload a music file (audio) and convert it to sheet music (PDF).
        Our AMT (Automatic Music Transcription) system uses AI to transcribe audio into notation.
      </p>

      <div className="space-y-6">
        <FileUpload
          accept=".mp3,.wav,.ogg,.m4a"
          onChange={fileUpload.handleFileChange}
          disabled={converter.uploading}
          label="Select Music File"
          file={fileUpload.file}
          error={fileUpload.error}
          formatFileSize={fileUpload.formatFileSize}
        />

        {converter.error && (
          <Alert type="error" message={converter.error} />
        )}

        {!converter.uploading && !converter.status && (
          <button
            onClick={handleUpload}
            disabled={!fileUpload.file}
            className="btn-primary w-full"
          >
            📄 Convert to Sheet Music
          </button>
        )}

        {(converter.uploading || converter.status) && (
          <StatusDisplay
            status={converter.status || {
              type: 'amt',
              status: 'processing',
              filename: fileUpload.file?.name || '',
              progress: 5,
              step: 'initializing',
              upload_path: '',
              output_path: '',
              error: ''
            }}
            color="purple"
            onDownload={handleDownload}
            onReset={handleReset}
            downloadButtonText="Download PDF Score"
          />
        )}

        <PipelineInfo steps={pipelineSteps} />
      </div>
    </div>
  );
};

export default AMTConverter;
