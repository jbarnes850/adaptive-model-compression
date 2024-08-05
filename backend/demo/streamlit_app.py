"""
This file contains the Streamlit app for demonstrating the Adaptive LLaMA Proxy.

To run this Streamlit app:
1. Ensure all dependencies are installed (streamlit, plotly, etc.)
2. Navigate to the project root directory
3. Run the following command:
   streamlit run backend/demo/streamlit_app.py

This will start the Streamlit server and open the app in your default web browser.

The app allows users to:
- Select between adaptive and fixed complexity modes
- Input prompts for the model to process
- View the generated responses
- See performance metrics and visualizations of the model selection process

Note: Make sure the AdaptiveLlamaProxy is properly set up and the task classifier is trained before running this app.
"""

import streamlit as st
import sys
import os
import time
from typing import Dict, Any
import pandas as pd
import plotly.express as px

# Ensure the src directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.adaptive_llama_mlx import AdaptiveLlamaProxy

@st.cache_resource
def load_alp() -> AdaptiveLlamaProxy:
    try:
        return AdaptiveLlamaProxy()
    except FileNotFoundError as e:
        st.error(f"Error: {str(e)}")
        st.error("Please train the classifier before running the demo.")
        return None
    except Exception as e:
        st.error(f"An error occurred while initializing the AdaptiveLlamaProxy: {str(e)}")
        return None

def generate_response(alp: AdaptiveLlamaProxy, prompt: str, mode: str) -> Dict[str, Any]:
    start_time = time.time()
    if mode == "Adaptive":
        response = alp.adaptive_generate(prompt)
    else:
        response = alp.adaptive_generate(prompt, task_complexity=mode.lower())
    end_time = time.time()
    response['total_time'] = end_time - start_time
    return response

def display_metrics(response: Dict[str, Any]):
    st.header("Task Analysis")
    st.write(f"Task Complexity: {response['task_complexity']}")
    st.write(f"Selected Model: {response['model_used']}")

    st.header("Performance Metrics")
    metrics_df = pd.DataFrame({
        'Metric': ['Total Time', 'API Latency', 'Memory Usage'],
        'Value': [
            f"{response['total_time']:.2f} seconds",
            f"{response['generation_time']:.2f} seconds",
            f"{response['memory_usage']:.2f}%"
        ]
    })
    st.table(metrics_df)

def visualize_model_selection(response: Dict[str, Any]):
    models = ['simple', 'medium', 'complex']
    model_sizes = [8, 70, 405]  # Sizes in billions of parameters
    selected_index = models.index(response['model_used'])
    colors = ['lightgrey' if i != selected_index else 'lightgreen' for i in range(len(models))]
    
    fig = px.bar(
        x=models, 
        y=model_sizes, 
        title="Model Selection",
        labels={'x': 'Model', 'y': 'Model Size (B parameters)'},
        color=colors,
        color_discrete_map={
            'lightgrey': 'lightgrey',
            'lightgreen': 'lightgreen'
        }
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)

def main():
    st.set_page_config(page_title="Adaptive LLaMA Proxy Demo", page_icon="🦙", layout="wide")
    st.title("Adaptive LLaMA Proxy Demo")
    
    alp = load_alp()
    if alp is None:
        return

    st.sidebar.header("Mode Selection")
    mode = st.sidebar.radio("Select Mode", ["Adaptive", "Simple", "Medium", "Complex"])

    st.header("Input")
    user_input = st.text_area("Enter your prompt:", height=100)

    if st.button("Generate"):
        if user_input:
            with st.spinner("Analyzing and generating response..."):
                response = generate_response(alp, user_input, mode)

            st.header("Response")
            st.write(response['response'])

            col1, col2 = st.columns(2)
            with col1:
                display_metrics(response)
            with col2:
                visualize_model_selection(response)
        else:
            st.warning("Please enter a prompt.")

    st.sidebar.write("Loaded Models:", ", ".join(alp.get_loaded_models()))
    st.sidebar.header("About")
    st.sidebar.info("""
    This demo showcases the Adaptive LLaMA Proxy system. 
    It dynamically selects the most appropriate model based on task complexity, 
    balancing performance and efficiency using locally-hosted MLX models.
    """)

if __name__ == "__main__":
    main()