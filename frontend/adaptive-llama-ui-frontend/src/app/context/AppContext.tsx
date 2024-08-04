"use client";

import React, { createContext, useState, useContext, ReactNode } from 'react';
import { ApiResponse } from '../lib/api';

interface ComplexityResult {
  score: number;
  level: 'Low' | 'Medium' | 'High';
  factors: {
    length: number;
    uniqueWords: number;
    averageWordLength: number;
    specialCharacters: number;
  };
}

interface AppContextType {
  input: string;
  setInput: (input: string) => void;
  apiResponse: ApiResponse | null;
  setApiResponse: (response: ApiResponse | null) => void;
  isLoading: boolean;
  setIsLoading: (isLoading: boolean) => void;
  complexity: ComplexityResult;
  setComplexity: (complexity: ComplexityResult) => void;
  cumulativeMetrics: {
    averageLatency: number;
    totalRequests: number;
  };
  updateCumulativeMetrics: (latency: number) => void;
  isComparisonMode: boolean;
  setIsComparisonMode: (isComparisonMode: boolean) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export function AppProvider({ children }: { children: ReactNode }) {
  const [input, setInput] = useState('');
  const [apiResponse, setApiResponse] = useState<ApiResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [complexity, setComplexity] = useState<ComplexityResult>({
    score: 0,
    level: 'Low',
    factors: { length: 0, uniqueWords: 0, averageWordLength: 0, specialCharacters: 0 },
  });
  const [cumulativeMetrics, setCumulativeMetrics] = useState({
    averageLatency: 0,
    totalRequests: 0,
  });
  const [isComparisonMode, setIsComparisonMode] = useState(false);
  const updateCumulativeMetrics = (latency: number) => {
    setCumulativeMetrics(prev => {
      const newTotalRequests = prev.totalRequests + 1;
      const newAverageLatency = (prev.averageLatency * prev.totalRequests + latency) / newTotalRequests;
      return {
        averageLatency: newAverageLatency,
        totalRequests: newTotalRequests,
      };
    });
  };

  return (
    <AppContext.Provider
      value={{
        input,
        setInput,
        apiResponse,
        setApiResponse,
        isLoading,
        setIsLoading,
        complexity,
        setComplexity,
        cumulativeMetrics,
        updateCumulativeMetrics,
        isComparisonMode,
        setIsComparisonMode,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext() {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
}