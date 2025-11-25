import React, { Suspense as ReactSuspense, ReactNode } from 'react';
import LoadingSpinner from './LoadingSpinner';

interface SuspenseWrapperProps {
  children: ReactNode;
  fallback?: ReactNode;
  fullScreen?: boolean;
}

const SuspenseWrapper: React.FC<SuspenseWrapperProps> = ({
  children,
  fallback,
  fullScreen = false,
}) => {
  const defaultFallback = (
    <LoadingSpinner
      size="lg"
      text="Loading component..."
      fullScreen={fullScreen}
    />
  );

  return (
    <ReactSuspense fallback={fallback || defaultFallback}>
      {children}
    </ReactSuspense>
  );
};

export default SuspenseWrapper;
