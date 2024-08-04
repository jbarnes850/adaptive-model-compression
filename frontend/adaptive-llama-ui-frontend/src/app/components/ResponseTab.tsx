"use client";

import React from 'react';
import { useAppContext } from '../context/AppContext';

const ResponseTab: React.FC = () => {
  const { apiResponse, isLoading } = useAppContext();

  return (
    <div className="bg-gray-100 p-4 rounded-lg shadow-md">
      <h2 className="text-xl sm:text-2xl font-semibold mb-4">Response</h2>
      {isLoading ? (
        <p className="text-sm sm:text-base">Loading response...</p>
      ) : apiResponse ? (
        <div className="bg-white p-2 sm:p-4 rounded border">
          <p className="text-sm sm:text-base break-words">{apiResponse.response}</p>
        </div>
      ) : (
        <p className="text-sm sm:text-base">No response yet. Send a prompt to get started!</p>
      )}
    </div>
  );
};

export default ResponseTab;