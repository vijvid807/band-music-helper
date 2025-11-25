import React from 'react';

interface AlertProps {
  type: 'error' | 'success' | 'info' | 'warning';
  title?: string;
  message: string;
  onClose?: () => void;
}

const Alert: React.FC<AlertProps> = ({ type, title, message, onClose }) => {
  const styles = {
    error: {
      bg: 'bg-red-50',
      border: 'border-red-200',
      text: 'text-red-700',
      title: 'text-red-900',
    },
    success: {
      bg: 'bg-green-50',
      border: 'border-green-200',
      text: 'text-green-700',
      title: 'text-green-900',
    },
    info: {
      bg: 'bg-blue-50',
      border: 'border-blue-200',
      text: 'text-blue-700',
      title: 'text-blue-900',
    },
    warning: {
      bg: 'bg-yellow-50',
      border: 'border-yellow-200',
      text: 'text-yellow-700',
      title: 'text-yellow-900',
    },
  };

  const style = styles[type];

  return (
    <div className={`${style.bg} border ${style.border} ${style.text} px-4 py-3 rounded-lg relative`}>
      {onClose && (
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-gray-500 hover:text-gray-700"
        >
          ×
        </button>
      )}
      {title && (
        <p className={`font-medium ${style.title} mb-1`}>{title}</p>
      )}
      <p className="text-sm">{message}</p>
    </div>
  );
};

export default Alert;
