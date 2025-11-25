import React from 'react';
import OMRConverter from './components/OMRConverter';
import AMTConverter from './components/AMTConverter';
import { ToastContainer, ErrorBoundary } from './components/common';
import { ToastProvider } from './contexts/ToastContext';
import './App.css';

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <ToastProvider>
        <div className="app-container">
          <ToastContainer />
          
          <header className="header">
            <h1 className="text-4xl font-bold text-white">🎼 Band Music Converter</h1>
            <p className="text-blue-100 mt-2">
              AI-Powered Music Sheet & Audio Conversion
            </p>
          </header>

          <main className="container mx-auto px-4 py-8">
            <div className="grid md:grid-cols-2 gap-8">
              <ErrorBoundary>
                <OMRConverter />
              </ErrorBoundary>
              <ErrorBoundary>
                <AMTConverter />
              </ErrorBoundary>
            </div>

            <footer className="text-center mt-12 text-gray-600">
              <p>
                Powered by <strong>Oemer</strong>, <strong>Basic Pitch</strong>, <strong>music21</strong>, 
                <strong> FluidSynth</strong>, and <strong>LilyPond</strong>
              </p>
              <p className="text-sm mt-2">
                Open source music processing tools for everyone
              </p>
            </footer>
          </main>
        </div>
      </ToastProvider>
    </ErrorBoundary>
  );
};

export default App;
