# Adaptive LLaMA Proxy (ALP) - Frontend

## Project Overview

Adaptive LLaMA Proxy (ALP) is a proof-of-concept system that demonstrates adaptive model compression for Llama 3.1, optimizing for different tasks while balancing performance and efficiency. This repository contains the frontend application for ALP, built with Next.js and React.

The ALP frontend provides an interactive interface for users to input prompts, visualize model selection, compare different model compressions, and analyze performance metrics.

## Key Features

- Multi-tab interface for input, model selection, response, and performance metrics
- Interactive model visualization
- Real-time complexity analysis of user input
- Comparison mode to run prompts through different model compressions
- Performance dashboard with cumulative metrics
- Educational tooltips for key terms and metrics

## Prerequisites

- Node.js 14.x or later
- npm 6.x or later

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/adaptive-llama-proxy-frontend.git
   cd adaptive-llama-proxy-frontend
   ```

2. Install the dependencies:
   ```
   npm install
   ```

3. Create a `.env.local` file in the root directory and add the following environment variables:
   ```
   NEXT_PUBLIC_API_URL=http://your-backend-api-url
   ```
   Replace `http://your-backend-api-url` with the actual URL of your backend API.

## Running the Application

To run the application in development mode:

npm run dev


Open [http://localhost:3000](http://localhost:3000) in your browser to see the result.

To build the application for production:

npm start


## Project Structure

- `src/app`: Main application code
  - `components/`: React components
  - `context/`: React context for state management
  - `lib/`: Utility functions and API calls
  - `api/`: API routes for the Next.js backend
- `public/`: Static assets

## Key Components

- `InputTab`: Handles user input and complexity analysis
- `ModelVisualization`: Visualizes the selected model based on input complexity
- `ModelSelectionTab`: Displays the selected model and reason for selection
- `ResponseTab`: Shows the generated response from the model
- `PerformanceMetricsTab`: Displays performance metrics for the current request
- `PerformanceDashboard`: Shows cumulative performance metrics and model usage statistics
- `ComparisonMode`: Allows users to compare results from different model compressions

## State Management

The application uses React Context for state management. The main context provider is located in `src/app/context/AppContext.tsx`.

## API Integration

The application communicates with the backend API through functions defined in `src/app/lib/api.ts`. The actual API calls are proxied through Next.js API routes in `src/app/api/` to avoid CORS issues and add an additional layer of security.

## License

This project is licensed under the MIT License

