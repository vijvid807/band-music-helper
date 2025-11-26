import React from 'react';
import { JobStatus } from '../../services/api';
import ProgressBar from './ProgressBar';

interface StatusDisplayProps {
  status: JobStatus;
  color?: 'blue' | 'purple' | 'green';
  onDownload?: () => void;
  onReset?: () => void;
  downloadButtonText?: string;
  audioUrl?: string; // URL for audio playback
}

const StatusDisplay: React.FC<StatusDisplayProps> = ({
  status,
  color = 'blue',
  onDownload,
  onReset,
  downloadButtonText = 'Download Result',
  audioUrl,
}) => {
  const colorClasses = {
    blue: {
      bg: 'bg-blue-50',
      border: 'border-blue-200',
      text: 'text-blue-900',
      textSm: 'text-blue-700',
    },
    purple: {
      bg: 'bg-purple-50',
      border: 'border-purple-200',
      text: 'text-purple-900',
      textSm: 'text-purple-700',
    },
    green: {
      bg: 'bg-green-50',
      border: 'border-green-200',
      text: 'text-green-900',
      textSm: 'text-green-700',
    },
  };

  const style = colorClasses[color];

  return (
    <div className={`${style.bg} border ${style.border} rounded-lg p-4`}>
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center">
          {status.status === 'processing' && (
            <div className={`animate-spin rounded-full h-5 w-5 border-b-2 border-${color}-600 mr-2`}></div>
          )}
          <span className={`font-medium ${style.text}`}>
            {status.status === 'processing' ? 'Processing...' : 'Status'}
          </span>
        </div>
      </div>

      {status.step && (
        <div className="mb-2">
          <p className={`text-sm ${style.textSm}`}>
            Step: <span className="font-medium capitalize">{status.step}</span>
          </p>
        </div>
      )}

      {status.progress !== undefined && status.progress > 0 && (
        <div className="mt-2">
          <ProgressBar progress={status.progress} color={color} />
        </div>
      )}

      {status.status === 'completed' && onDownload && onReset && (
        <div className="mt-4 space-y-3">
          {audioUrl && (
            <div className="space-y-2">
              <p className={`text-sm font-medium ${style.text}`}>🎵 Preview Audio</p>
              <audio 
                controls 
                className="w-full"
                preload="metadata"
              >
                <source src={audioUrl} type="audio/mpeg" />
                Your browser does not support the audio element.
              </audio>
            </div>
          )}
          
          <div className="space-y-2">
            <button onClick={onDownload} className="btn-primary w-full">
              ⬇️ {downloadButtonText}
            </button>
            <button onClick={onReset} className="btn-secondary w-full">
              Convert Another File
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default StatusDisplay;
