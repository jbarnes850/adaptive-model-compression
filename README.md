# Adaptive LLaMA 3.1 Proxy (ALP 3.1)

<div style="display: flex; justify-content: space-between;">
  <img src="./assets/Demo Screenshot 1.png" alt="Demo Screenshot 1" width="48%">
  <img src="./assets/Demo Screenshot 2.png" alt="Demo Screenshot 2" width="48%">
</div>

Adaptive model compression dynamically adjusts the size and complexity of machine learning models based on the task at hand, balancing performance and efficiency. This approach allows for optimal use of computational resources while maintaining high-quality outputs.

## Project Overview

Adaptive LLaMA Proxy (ALP) is a proof-of-concept system developed for the South Park Commons Llama 3 Hackathon. It demonstrates adaptive model compression for Llama 3.1, optimizing for different tasks while balancing performance and efficiency. ALP showcases a novel approach to language model deployment, adapting to task complexity in real-time.

## Key Features

- Multi-stage compression using different quantization levels (2-bit, 4-bit, 8-bit, and full precision)
- Dynamic task complexity classification using a lightweight machine learning model
- Adaptive model selection based on input complexity
- Memory-efficient model loading and unloading
- Continuous learning and classifier updates
- Comprehensive evaluation suite for accuracy, latency, and memory usage
- Interactive web interface for exploring ALP's capabilities

## How It Works

ALP uses a lightweight machine learning model to classify the complexity of incoming tasks. Based on this classification, it selects an appropriately compressed version of the Llama 3.1 model (2-bit, 4-bit, 8-bit, or full precision). This adaptive approach ensures optimal resource usage while maintaining high-quality outputs.

## Project Structure

The project consists of two main components:

1. Backend: Python-based API using FastAPI and MLX framework
2. Frontend: Next.js application with React and TypeScript

### Backend Structure

- `src/`: Core implementation files
  - `adaptive_llama_mlx.py`: Main implementation of the Adaptive LLaMA Proxy
  - `task_classifier.py`: Task complexity classifier
  - `api.py`: FastAPI application for serving the ALP
- `data/`: Data files for training and evaluation
- `scripts/`: Utility scripts for training and evaluation
- `tests/`: Unit tests
- `demo/`: Streamlit demo application (deprecated, see frontend for new interface)

### Frontend Structure

- `src/app/`: Main application code
  - `components/`: React components
  - `context/`: React context for state management
  - `lib/`: Utility functions and API calls
  - `api/`: API routes for the Next.js backend

## Prerequisites

### Backend
- Python 3.8+
- MLX framework
- 16GB+ RAM
- Access to Llama 3.1 model files (subject to licensing restrictions)

### Frontend
- Node.js 14.x or later
- npm 6.x or later

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/adaptive-llama-proxy.git
   cd adaptive-llama-proxy
   ```

2. Set up the backend:
   ```
   cd backend
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```
   cd ../frontend
   npm install
   ```

4. Set up environment variables:
   - Backend: Create a `.env` file in the `backend` directory with:
     ```
     API_KEY=your_secret_api_key
     ```
   - Frontend: Create a `.env.local` file in the `frontend` directory with:
     ```
     NEXT_PUBLIC_API_URL=http://localhost:8000
     API_KEY=your_secret_api_key
     ```

5. Set up the Llama 3.1 model files according to the provided instructions (not included in this repository due to licensing).

## Usage

1. Start the backend server:
   ```
   cd backend
   python scripts/run_api.py
   ```

2. In a new terminal, start the frontend development server:
   ```
   cd frontend
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:3000` to access the ALP interface.

## Key Components

- InputTab: Handles user input and complexity analysis
- ModelVisualization: Visualizes the selected model based on input complexity
- ResponseTab: Shows the generated response from the model
- PerformanceMetricsTab: Displays performance metrics for the current request
- PerformanceDashboard: Shows cumulative performance metrics and model usage statistics
- ComparisonMode: Allows users to compare results from different model compressions

## API Integration

The frontend communicates with the backend API through functions defined in `src/app/lib/api.ts`. The actual API calls are proxied through Next.js API routes in `src/app/api/` to avoid CORS issues and add an additional layer of security.

## Evaluation

To run the backend evaluation suite:

cd backend
python scripts/evaluate_model.py


This generates a detailed report on model performance across different task complexities, including accuracy, latency, and memory usage metrics.

## Future Work

We are exploring several avenues for improving ALP:
1. Implementing more fine-grained compression levels
2. Enhancing the task complexity classifier with active learning
3. Extending support to other large language models
4. Developing a more sophisticated caching mechanism for frequently used model configurations


## Contributing

This project was developed during the South Park Commons Llama 3.1 Hackathon. While we're not actively seeking contributions, we encourage you to fork the project and experiment with your own ideas!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Meta AI for the Llama 3.1 model
- Apple for the MLX framework
- South Park Commons for hosting the Llama 3 Hackathon
