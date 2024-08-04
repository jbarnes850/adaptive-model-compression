"use client";

import React, { useState } from 'react';
import { useAppContext } from '../context/AppContext';
import { sendPrompt, ApiResponse } from '../lib/api';

interface ComparisonResult {
  full: ApiResponse | null;
  '8bit': ApiResponse | null;
  '4bit': ApiResponse | null;
}

const ComparisonMode: React.FC = () => {
  const { isComparisonMode, setIsComparisonMode, input } = useAppContext();
  const [comparisonResults, setComparisonResults] = useState<ComparisonResult>({
    full: null,
    '8bit': null,
    '4bit': null,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const handleComparisonToggle = () => {
    setIsComparisonMode(!isComparisonMode);
    if (!isComparisonMode) {
      runComparison();
    } else {
      setComparisonResults({ full: null, '8bit': null, '4bit': null });
      setError(null); // Clear any previous errors when disabling comparison mode
    }
  };

  const runComparison = async () => {
    if (!input.trim()) {
      setError('Please enter a prompt before running the comparison.');
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      const [fullModelResponse, eightBitResponse, fourBitResponse] = await Promise.all([
        sendPrompt(input, 'full').catch(e => {
          console.error('Error with full model:', e);
          return null;
        }),
        sendPrompt(input, '8bit').catch(e => {
          console.error('Error with 8bit model:', e);
          return null;
        }),
        sendPrompt(input, '4bit').catch(e => {
          console.error('Error with 4bit model:', e);
          return null;
        })
      ]);

      if (!fullModelResponse && !eightBitResponse && !fourBitResponse) {
        throw new Error('All model requests failed');
      }

      setComparisonResults({
        full: fullModelResponse,
        '8bit': eightBitResponse,
        '4bit': fourBitResponse,
      });
    } catch (error) {
      console.error('Error running comparison:', error);
      setError('An error occurred while running the comparison. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const renderComparisonResults = () => {
    return (
      <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {Object.entries(comparisonResults).map(([model, result]) => (
          <div key={model} className="bg-white p-4 rounded shadow">
            <h3 className="font-bold mb-2 text-lg">{model === 'full' ? 'Full Model' : `${model} Model`}</h3>
            {result ? (
              <>
                <p className="mb-2 text-sm sm:text-base">{result.response}</p>
                <ul className="text-xs sm:text-sm space-y-1">
                  <li>Latency: {result.metrics.latency}ms</li>
                  <li>Memory Usage: {result.metrics.memoryUsage}GB</li>
                  <li>Task Complexity: {result.metrics.taskComplexity}</li>
                </ul>
              </>
            ) : (
              <p className="text-sm">No data available</p>
            )}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="bg-gray-100 p-4 rounded-lg mt-8">
      <h2 className="text-xl font-semibold mb-4">Comparison Mode</h2>
      <button
        className={`px-4 py-2 rounded w-full sm:w-auto ${
          isComparisonMode ? 'bg-blue-500 hover:bg-blue-600 text-white' : 'bg-gray-300 hover:bg-gray-400'
        }`}
        onClick={handleComparisonToggle}
        disabled={isLoading}
      >
        {isComparisonMode ? 'Disable' : 'Enable'} Comparison Mode
      </button>
      {isLoading && <p className="mt-2 text-sm">Running comparison...</p>}
      {isComparisonMode && renderComparisonResults()}
    </div>
  );
};

export default ComparisonMode;