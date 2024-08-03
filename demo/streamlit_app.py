import streamlit as st
import sys
import os
import time
import pandas as pd
import plotly.express as px
import psutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.adaptive_llama_mlx import AdaptiveLlamaProxy

@st.cache_resource
def load_alp():
    alp = AdaptiveLlamaProxy(max_memory_usage=90, model_cache_size=2)
    return alp

def main():
    st.title("Adaptive LLaMA Proxy Demo")
    
    alp = load_alp()

    st.sidebar.header("Mode Selection")
    mode = st.sidebar.radio("Select Mode", ["Adaptive", "Very Simple", "Simple", "Medium", "Complex"])

    st.header("Input")
    user_input = st.text_area("Enter your prompt:", height=100)

    if st.button("Generate"):
        if user_input:
            with st.spinner("Analyzing and generating response..."):
                start_time = time.time()
                if mode == "Adaptive":
                    response = alp.adaptive_generate(user_input)
                else:
                    response = alp.adaptive_generate(user_input, task_complexity=mode.lower())
                end_time = time.time()

            st.header("Task Analysis")
            st.write(f"Task Complexity: {response['task_complexity']}")
            st.write(f"Selected Model: {response['model_used']}")

            st.header("Response")
            st.write(response['response'])

            st.header("Performance Metrics")
            generation_time = end_time - start_time
            
            metrics_df = pd.DataFrame({
                'Metric': ['Generation Time', 'Memory Usage'],
                'Value': [f"{generation_time:.2f} seconds", f"{response['memory_usage']:.2f}%"]
            })
            st.table(metrics_df)

            # Visualize model selection
            models = ['2bit', 'full', '4bit', '8bit']
            model_sizes = [2, 16, 35, 70]  # Approximate sizes in GB
            selected_index = models.index(response['model_used'])
            colors = ['lightgrey' if i != selected_index else 'lightgreen' for i in range(len(models))]
            
            fig = px.bar(x=models, y=model_sizes, title="Model Selection",
                         labels={'x': 'Model', 'y': 'Model Size (GB)'})
            fig.update_traces(marker_color=colors)
            st.plotly_chart(fig)

        else:
            st.warning("Please enter a prompt.")

    st.sidebar.header("Model Management")
    if st.sidebar.button("Unload All Models"):
        alp.unload_all_models()
        st.sidebar.success("All models unloaded")

    loaded_models = alp.get_loaded_models()
    st.sidebar.write("Loaded Models:", ", ".join(loaded_models) if loaded_models else "None")

    st.sidebar.header("About")
    st.sidebar.info("""
    This demo showcases the Adaptive LLaMA Proxy system. 
    It dynamically selects the most appropriate model based on task complexity, 
    balancing performance and efficiency.
    """)

    # Display current memory usage
    memory_usage = alp.get_memory_usage()
    st.sidebar.info(f"Current memory usage: {memory_usage:.2f}%")

if __name__ == "__main__":
    main()