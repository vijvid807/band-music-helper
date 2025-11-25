import React from 'react';

interface PipelineInfoProps {
  steps: Array<{
    title: string;
    description: string;
  }>;
}

const PipelineInfo: React.FC<PipelineInfoProps> = ({ steps }) => {
  return (
    <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
      <h3 className="font-semibold text-gray-900 mb-3">Pipeline Steps:</h3>
      <ol className="space-y-2 text-sm text-gray-700">
        {steps.map((step, index) => (
          <li key={index} className="flex items-start">
            <span className="font-bold mr-2">{index + 1}.</span>
            <span>
              <strong>{step.title}:</strong> {step.description}
            </span>
          </li>
        ))}
      </ol>
    </div>
  );
};

export default PipelineInfo;
