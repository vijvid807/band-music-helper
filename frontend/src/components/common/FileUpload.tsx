import React from 'react';

interface FileUploadProps {
  accept: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  disabled?: boolean;
  label: string;
  file?: File | null;
  error?: string | null;
  formatFileSize?: (size: number) => string;
}

const FileUpload: React.FC<FileUploadProps> = ({
  accept,
  onChange,
  disabled = false,
  label,
  file,
  error,
  formatFileSize,
}) => {
  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-700">
        {label}
      </label>
      <input
        type="file"
        accept={accept}
        onChange={onChange}
        disabled={disabled}
        className="input-file"
      />
      {file && formatFileSize && (
        <p className="mt-2 text-sm text-gray-600">
          Selected: <span className="font-medium">{file.name}</span>{' '}
          ({formatFileSize(file.size)})
        </p>
      )}
      {error && (
        <p className="mt-2 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};

export default FileUpload;
