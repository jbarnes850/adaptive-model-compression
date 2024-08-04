"use client";

import React from 'react';
import { useAppContext } from '../context/AppContext';
import Tooltip from './Tooltip';

const ModelSelectionTab: React.FC = () => {
  const { apiResponse, complexity } = useAppContext();

  return (
    <div className="bg-gray-100 p-4 rounded-lg shadow-md">
      <h2 className="text-xl sm:text-2xl font-semibold mb-4">Model Selection</h2>
      {apiResponse ? (
        <div className="space-y-2">
          <p className="flex items-center flex-wrap">
            <span className="mr-2">Selected Model:</span>
            <span className="font-bold">{apiResponse.model}</span>
            <Tooltip content="The model is selected based on the complexity of the input task.">
              <span className="ml-1 cursor-help text-gray-500">ⓘ</span>
            </Tooltip>
          </p>
          <p className="text-sm sm:text-base">
            Reason: <span className="font-medium">{complexity.level}</span> task complexity detected
          </p>
        </div>
      ) : (
        <p className="text-sm sm:text-base">No model selected yet. Send a prompt to see the selection.</p>
      )}
    </div>
  );
};

export default ModelSelectionTab;