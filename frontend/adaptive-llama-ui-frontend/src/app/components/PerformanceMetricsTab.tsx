"use client";

import React from 'react';
import { useAppContext } from '../context/AppContext';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip as ChartTooltip, Legend } from 'chart.js';
import CustomTooltip from './Tooltip';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, ChartTooltip, Legend);

const PerformanceMetricsTab: React.FC = () => {
  const { apiResponse, complexity } = useAppContext();

  const chartData = {
    labels: ['Latency', 'Memory Usage', 'Complexity Score'],
    datasets: [
      {
        label: 'Performance Metrics',
        data: apiResponse ? [
          apiResponse.metrics.latency,
          apiResponse.metrics.memoryUsage,
          complexity.score
        ] : [],
        backgroundColor: [
          'rgba(255, 99, 132, 0.5)',
          'rgba(54, 162, 235, 0.5)',
          'rgba(255, 206, 86, 0.5)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          boxWidth: 12,
          font: {
            size: 10,
          },
        },
      },
      title: {
        display: true,
        text: 'Performance Metrics',
        font: {
          size: 14,
        },
      },
    },
  };

  return (
    <div className="bg-gray-100 p-4 rounded-lg">
      <h2 className="text-xl sm:text-2xl font-semibold mb-4">Performance Metrics</h2>
      {apiResponse ? (
        <>
          <div className="mb-4 h-64 sm:h-80">
            <Bar data={chartData} options={chartOptions} />
          </div>
          <ul className="space-y-2 text-sm sm:text-base">
            <li className="flex items-center flex-wrap">
              <span className="mr-1">Latency:</span>
              <span className="font-bold">{apiResponse.metrics.latency}ms</span>
              <CustomTooltip content="The time taken to process the input and generate a response.">
                <span className="ml-1 cursor-help text-gray-500">ⓘ</span>
              </CustomTooltip>
            </li>
            <li className="flex items-center flex-wrap">
              <span className="mr-1">Memory Usage:</span>
              <span className="font-bold">{apiResponse.metrics.memoryUsage}GB</span>
              <CustomTooltip content="The amount of memory used by the model during processing.">
                <span className="ml-1 cursor-help text-gray-500">ⓘ</span>
              </CustomTooltip>
            </li>
            <li className="flex items-center flex-wrap">
              <span className="mr-1">Task Complexity:</span>
              <span className="font-bold">{complexity.level}</span>
              <span className="ml-1">(Score: {complexity.score.toFixed(2)})</span>
              <CustomTooltip content="Complexity is determined by factors such as input length, unique words, and special characters.">
                <span className="ml-1 cursor-help text-gray-500">ⓘ</span>
              </CustomTooltip>
            </li>
            <li>Input Length: <span className="font-bold">{complexity.factors.length}</span> characters</li>
            <li>Unique Words: <span className="font-bold">{complexity.factors.uniqueWords}</span></li>
            <li>Avg. Word Length: <span className="font-bold">{complexity.factors.averageWordLength.toFixed(2)}</span> characters</li>
            <li>Special Characters: <span className="font-bold">{complexity.factors.specialCharacters}</span></li>
          </ul>
        </>
      ) : (
        <p className="text-sm sm:text-base">No metrics available yet. Send a prompt to see performance data.</p>
      )}
    </div>
  );
};

export default PerformanceMetricsTab;