import React from 'react';

interface ProgressBarProps {
  progress: number;
  label?: string;
  color?: 'blue' | 'purple' | 'green';
}

const ProgressBar: React.FC<ProgressBarProps> = ({
  progress,
  label,
  color = 'blue',
}) => {
  const colorClasses = {
    blue: 'bg-blue-600',
    purple: 'bg-purple-600',
    green: 'bg-green-600',
  };

  const bgColorClasses = {
    blue: 'bg-blue-200',
    purple: 'bg-purple-200',
    green: 'bg-green-200',
  };

  return (
    <div className="w-full">
      {label && (
        <p className="text-sm text-gray-700 mb-2">{label}</p>
      )}
      <div className={`w-full ${bgColorClasses[color]} rounded-full h-2`}>
        <div
          className={`${colorClasses[color]} h-2 rounded-full transition-all duration-300`}
          style={{ width: `${progress}%` }}
        />
      </div>
      <p className="text-xs text-gray-600 mt-1 text-right">{progress}%</p>
    </div>
  );
};

export default ProgressBar;
