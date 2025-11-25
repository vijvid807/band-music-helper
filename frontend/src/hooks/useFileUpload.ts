import { useState, useCallback, ChangeEvent } from 'react';

export interface UseFileUploadOptions {
  accept?: string;
  maxSize?: number;
  onFileSelect?: (file: File) => void;
}

export interface UseFileUploadResult {
  file: File | null;
  error: string | null;
  handleFileChange: (event: ChangeEvent<HTMLInputElement>) => void;
  setFile: (file: File | null) => void;
  clearFile: () => void;
  formatFileSize: (bytes: number) => string;
}

export const useFileUpload = ({
  accept,
  maxSize = 100 * 1024 * 1024, // 100MB default
  onFileSelect,
}: UseFileUploadOptions = {}): UseFileUploadResult => {
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  const formatFileSize = useCallback((bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
  }, []);

  const validateFile = useCallback(
    (selectedFile: File): string | null => {
      // Check file size
      if (selectedFile.size > maxSize) {
        return `File size exceeds ${formatFileSize(maxSize)}`;
      }

      // Check file type if accept is specified
      if (accept) {
        const acceptedTypes = accept.split(',').map((type) => type.trim());
        const fileExtension = `.${selectedFile.name.split('.').pop()?.toLowerCase()}`;
        const mimeType = selectedFile.type;

        const isAccepted = acceptedTypes.some(
          (type) =>
            type === mimeType ||
            type === fileExtension ||
            (type.endsWith('/*') && mimeType.startsWith(type.replace('/*', '')))
        );

        if (!isAccepted) {
          return `File type not accepted. Accepted types: ${accept}`;
        }
      }

      return null;
    },
    [accept, maxSize, formatFileSize]
  );

  const handleFileChange = useCallback(
    (event: ChangeEvent<HTMLInputElement>) => {
      const selectedFile = event.target.files?.[0];
      
      if (!selectedFile) {
        setFile(null);
        setError(null);
        return;
      }

      const validationError = validateFile(selectedFile);
      
      if (validationError) {
        setError(validationError);
        setFile(null);
        event.target.value = '';
        return;
      }

      setFile(selectedFile);
      setError(null);
      onFileSelect?.(selectedFile);
    },
    [validateFile, onFileSelect]
  );

  const clearFile = useCallback(() => {
    setFile(null);
    setError(null);
  }, []);

  return {
    file,
    error,
    handleFileChange,
    setFile,
    clearFile,
    formatFileSize,
  };
};
