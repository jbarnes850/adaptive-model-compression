"use client";

import React from 'react';
import { useAppContext } from '../context/AppContext';

const ModelVisualization: React.FC = () => {
  const { apiResponse, complexity } = useAppContext();

  const models = [
    { name: 'Full Model', color: 'bg-blue-500', bits: 32 },
    { name: '8-bit Model', color: 'bg-green-500', bits: 8 },
    { name: '4-bit Model', color: 'bg-yellow-500', bits: 4 },
  ];

  const getSelectedModel = () => {
    if (!apiResponse) return null;
    return models.find(model => model.name.toLowerCase().includes(apiResponse.model.toLowerCase()));
  };

  const getModelSize = (bits: number) => {
    const baseSize = 100; // Base size for visualization
    return baseSize * (bits / 32); // Scale based on bit size
  };

  const selectedModel = getSelectedModel();

  return (
    <div className="bg-gray-100 p-4 rounded-lg">
      <h2 className="text-xl sm:text-2xl font-semibold mb-4">Model Visualization</h2>
      <div className="flex flex-wrap justify-center sm:justify-between items-end gap-4">
        {models.map((model) => (
          <div key={model.name} className="text-center w-1/3 sm:w-auto">
            <div 
              className={`${model.color} rounded-t-full mx-auto mb-2 transition-all duration-300`}
              style={{
                width: `${getModelSize(model.bits) * 0.6}px`,
                height: `${getModelSize(model.bits) * 0.6}px`,
                maxWidth: '100%',
                opacity: selectedModel?.name === model.name ? 1 : 0.5,
                transform: selectedModel?.name === model.name ? 'scale(1.1)' : 'scale(1)',
              }}
            ></div>
            <p className={`text-xs sm:text-sm ${selectedModel?.name === model.name ? 'font-bold' : ''}`}>{model.name}</p>
          </div>
        ))}
      </div>
      {complexity && (
        <div className="mt-4 text-sm sm:text-base">
          <p>Task Complexity: <span className="font-bold">{complexity.level}</span></p>
          <p>Complexity Score: {complexity.score.toFixed(2)}</p>
        </div>
      )}
      {selectedModel && (
        <div className="mt-4 text-sm sm:text-base">
          <p>Selected Model: <span className="font-bold">{selectedModel.name}</span></p>
          <p>Reason: {complexity?.level} complexity task</p>
        </div>
      )}
    </div>
  );
};

export default ModelVisualization;