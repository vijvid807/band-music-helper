import React from 'react';
import bandMusicAPI from '../services/api';
import { useFileConverter } from '../hooks/useFileConverter';
import { useFileUpload } from '../hooks/useFileUpload';
import { useToast } from '../contexts/ToastContext';
import FileUpload from './common/FileUpload';
import Alert from './common/Alert';
import StatusDisplay from './common/StatusDisplay';
import PipelineInfo from './common/PipelineInfo';

const OMRConverter: React.FC = () => {
  const { showToast } = useToast();
  const [instrument, setInstrument] = React.useState<string>('piano');
  
  const fileUpload = useFileUpload({
    accept: '.pdf,.png,.jpg,.jpeg',
    maxSize: 100 * 1024 * 1024, // 100MB
  });

  const converter = useFileConverter({
    uploadFn: async (file: File) => {
      return bandMusicAPI.uploadImageForOMR(file, instrument);
    },
    getStatusFn: async (jobId: string) => {
      return bandMusicAPI.getOMRStatus(jobId);
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
      const url = bandMusicAPI.downloadOMRResult(converter.jobId);
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
    { title: 'Preprocessing', description: 'Enhance image quality and prepare for OMR' },
    { title: 'OMR Recognition', description: 'Extract musical notation using Oemer AI' },
    { title: 'MusicXML Processing', description: 'Parse and validate musical structure' },
    { title: 'MIDI Conversion', description: 'Convert to MIDI format with music21' },
    { title: 'Audio Synthesis', description: 'Generate MP3 audio using FluidSynth' },
  ];

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-blue-900">📄 Image/PDF to Music</h2>
        <span className="badge-blue">OMR Pipeline</span>
      </div>

      <p className="text-gray-700 mb-6">
        Upload a music sheet (PDF or image) and convert it to playable audio.
        Our OMR (Optical Music Recognition) system uses AI to recognize notes and generate audio.
      </p>

      <div className="space-y-6">
        {/* Instrument Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            🎺 Select Instrument
          </label>
          <select
            value={instrument}
            onChange={(e) => setInstrument(e.target.value)}
            disabled={converter.uploading || converter.status !== null}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
          >
            <option value="piano">🎹 Piano</option>
            <option value="trombone">🎺 Trombone</option>
            <option value="trumpet">🎺 Trumpet</option>
          </select>
          <p className="mt-1 text-sm text-gray-500">
            Choose the instrument sound for the generated audio
          </p>
        </div>

        <FileUpload
          accept=".pdf,.png,.jpg,.jpeg"
          onChange={fileUpload.handleFileChange}
          disabled={converter.uploading}
          label="Select Music Sheet"
          file={fileUpload.file}
          error={fileUpload.error}
          formatFileSize={fileUpload.formatFileSize}
        />

        {converter.error && (
          <Alert type="error" message={converter.error} />
        )}

        {!converter.status && (
          <button
            onClick={handleUpload}
            disabled={!fileUpload.file || converter.uploading}
            className="btn-primary w-full"
          >
            {converter.uploading ? '⏳ Processing...' : '🎵 Convert to Audio'}
          </button>
        )}

        {converter.status && (
          <StatusDisplay
            status={converter.status}
            color="blue"
            onDownload={handleDownload}
            onReset={handleReset}
            downloadButtonText="Download MP3 Audio"
            audioUrl={converter.jobId ? bandMusicAPI.downloadOMRResult(converter.jobId) : undefined}
          />
        )}

        <PipelineInfo steps={pipelineSteps} />
      </div>
    </div>
  );
};

export default OMRConverter;
