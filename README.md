# Adaptive LLaMA 3.1 Proxy (ALP 3.1)

<div style="display: flex; justify-content: space-between;">
  <img src="./assets/Demo Screenshot 1.png" alt="Demo Screenshot 1" width="48%">
  <img src="./assets/Demo Screenshot 2.png" alt="Demo Screenshot 2" width="48%">
</div>

Dynamic model selection optimizes the use of pre-compressed machine learning models based on the task at hand, balancing performance and efficiency. This approach allows for optimal use of computational resources while maintaining high-quality outputs.

## Project Overview

Adaptive LLaMA Proxy (ALP 3.1) is a proof-of-concept system developed for the South Park Commons Llama 3 Hackathon. It demonstrates on-device dynamic selection of pre-compressed large language models (LLMs), specifically Llama 3.1 8B 4-bit quantized, 70B 4-bit quantized, and 405B 2-bit quantized. ALP 3.1 uses a lightweight ML classifier to determine task complexity and dynamically select the most appropriate pre-compressed version of Llama 3.1 based on the input task, all while running locally on the user's device. This approach optimizes for different tasks while balancing performance and efficiency, without relying on cloud resources.

ALP 3.1 showcases a novel approach to local language model deployment, adapting to task complexity in real-time. By optimizing on-device resource usage through intelligent model selection, it maintains high-quality outputs while enhancing privacy and reducing latency compared to cloud-based solutions.

## Key Features

- Dynamic selection from multiple pre-compressed Llama 3.1 models (8B 4-bit, 70B 4-bit, and 405B 2-bit quantized)
- Task complexity classification using a lightweight machine learning model
- Adaptive model selection based on input complexity
- Memory-efficient model loading and unloading
- Local execution for enhanced privacy and reduced latency
- Comprehensive evaluation suite for accuracy, latency, and memory usage
- Interactive web interface for exploring ALP's capabilities

## How It Works

ALP uses a lightweight machine learning classifier to assess the complexity of incoming tasks. Based on this classification, it selects the most appropriate pre-compressed version of the Llama 3.1 model:

- 8B 4-bit quantized for simple tasks
- 70B 4-bit quantized for medium complexity tasks
- 405B 2-bit quantized for complex tasks

All models are implemented using the MLX framework, which enables efficient on-device inference. This adaptive approach ensures optimal resource usage while maintaining high-quality outputs.

The biggest technical challenge in developing ALP 3.1 was implementing efficient model loading and unloading mechanisms. These mechanisms are crucial for minimizing memory usage while maintaining low latency, especially when switching between different model sizes and quantization levels.


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
