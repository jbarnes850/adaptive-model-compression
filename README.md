# Adaptive LLaMA Proxy (ALP)

## Project Overview

Adaptive LLaMA Proxy (ALP) is a proof-of-concept system developed for the South Park Commons Llama 3 Hackathon. It demonstrates adaptive model compression for Llama 3.1, optimizing for different tasks while balancing performance and efficiency. ALP showcases a novel approach to language model deployment, adapting to task complexity in real-time.

## Key Features

- Multi-stage compression using different quantization levels (2-bit, 4-bit, 8-bit, and full precision)
- Dynamic task complexity classification using a lightweight machine learning model
- Adaptive model selection based on input complexity
- Memory-efficient model loading and unloading
- Continuous learning and classifier updates
- Comprehensive evaluation suite for accuracy, latency, and memory usage
- Streamlit demo for interactive exploration

## Prerequisites

- Python 3.8+
- MLX framework
- 16GB+ RAM
- Access to Llama 3.1 model files (subject to licensing restrictions)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/adaptive-llama-proxy.git
   cd adaptive-llama-proxy
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the Llama 3.1 model files according to the provided instructions (not included in this repository due to licensing).

## Usage

To run the Adaptive LLaMA Proxy:

python src/adaptive_llama_mlx.py


This will start an interactive session where you can input prompts and receive responses from the appropriate model based on task complexity.

## Project Structure

- `src/`: Core implementation files
  - `adaptive_llama_mlx.py`: Main implementation of the Adaptive LLaMA Proxy
  - `task_classifier.py`: Task complexity classifier
- `data/`: Data files for training and evaluation
- `scripts/`: Utility scripts for training and evaluation
  - `train_classifier.py`: Script for training and updating the task classifier
  - `evaluate_model.py`: Comprehensive evaluation suite
- `tests/`: Unit tests
- `demo/`: Streamlit demo application

## Task Classifier

The task classifier is a crucial component of ALP. To train or update the classifier:

python scripts/train_classifier.py


This script handles both initial training and continuous updates based on new data.

## Evaluation

To run the evaluation suite:

python scripts/evaluate_model.py

This generates a detailed report on model performance across different task complexities, including accuracy, latency, and memory usage metrics. Results are visualized and saved as `evaluation_results.png`.

## Demo

Experience ALP's capabilities through our Streamlit demo:

streamlit run demo/streamlit_app.py


## Contributing

This project was developed during the South Park Commons Llama 3.1 Hackathon. While we're not actively seeking contributions, we encourage you to fork the project and experiment with your own ideas!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Meta AI for the Llama 3.1 model
- Apple for the MLX framework
- South Park Commons for hosting the Llama 3 Hackathon
