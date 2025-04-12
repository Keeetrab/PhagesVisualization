import streamlit as st
import pandas as pd
import plotly.express as px
import time

# Set page config
st.set_page_config(
    page_title="Phage Therapy Analysis",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
    st.session_state.analysis_complete = False
    st.session_state.progress = 0
    st.session_state.current_step = 0

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('data/result.csv')

def reset_analysis_state():
    st.session_state.analysis_complete = False
    st.session_state.progress = 0
    st.session_state.current_step = 0

def show_home_page():
    # Center-aligned container
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🧬 Phage Therapy Analyzer")
        
        # Instructions box
        st.markdown("""
        <div style='padding: 20px; border-radius: 10px; border: 2px solid #f0f2f6; margin-bottom: 20px;'>
            <h2 style='text-align: center; color: #0066cc;'>Sample Collection Instructions</h2>
            <ol style='font-size: 18px;'>
                <li>Clean the sampling area thoroughly</li>
                <li>Use the sterile swab provided in the kit</li>
                <li>Collect the sample with a rolling motion</li>
                <li>Place the swab in the analyzer port</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        # Animation of sample placement
        animation_placeholder = st.empty()
        animation_placeholder.markdown("""
        <div style='text-align: center; font-family: monospace; font-size: 20px; white-space: pre;'>
        Insert sample here:
        
        ┌──────────┐
        │          │
        │    ▼     │
        └──────────┘
        </div>
        """, unsafe_allow_html=True)
        
        # Process button
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("Process Sample", key="process_button", use_container_width=True):
            reset_analysis_state()
            st.session_state.current_page = "Sample Analysis"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Status indicator
        st.markdown("""
        <div style='text-align: center; margin-top: 20px;'>
            <p style='color: #00cc00;'>✓ Device Ready</p>
            <p style='font-size: 14px; color: #666;'>Please ensure proper sample collection before processing</p>
        </div>
        """, unsafe_allow_html=True)

def show_analysis_page():
    st.header("Sample Analysis")
    st.write("""
    ### Processing Status
    Please do not remove the sample during analysis.
    """)
    
    # Simulate processing steps
    progress_bar = st.progress(st.session_state.progress)
    status_text = st.empty()
    
    steps = [
        "Initializing sequencer...",
        "Processing sample...",
        "Analyzing genetic material...",
        "Identifying bacterial strain...",
        "Calculating phage effectiveness..."
    ]

    # Only update progress if analysis is not complete
    if not st.session_state.analysis_complete:
        if st.session_state.current_step < len(steps):
            # Add initial delay for the first step
            if st.session_state.current_step == 0:
                status_text.text("Preparing analysis...")
                time.sleep(2)  # Initial delay before starting
            
            status_text.text(steps[st.session_state.current_step])
            st.session_state.progress = (st.session_state.current_step + 1) / len(steps)
            progress_bar.progress(st.session_state.progress)
            time.sleep(1.5)  # Slightly longer delay between steps
            st.session_state.current_step += 1
            st.rerun()
        else:
            st.session_state.analysis_complete = True
            st.rerun()
    
    # Show completion messages and button only when analysis is done
    if st.session_state.analysis_complete:
        status_text.text("Analysis completed!")
        st.success('Analysis complete!')
        st.info('Identified bacteria: GL538315')
        if st.button("View Results"):
            st.session_state.current_page = "Results"
            st.rerun()

def show_results_page():
    st.header("Analysis Results")
    
    # Load and display data
    df = load_data()
    
    # Hardcode the bacterium
    bacterium = "GL538315"
    st.success(f"Identified Bacteria: {bacterium}")
    
    # Filter data
    filtered_df = df[df['bacterium'] == bacterium]
    
    # Display results
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Phage Recommendations")
        # Sort by key_gene_output and show top 5
        top_phages = filtered_df.sort_values('key_gene_output', ascending=False).head()
        st.dataframe(top_phages[['phage', 'key_gene_output', 'wgs_output']])
        
    with col2:
        st.subheader("Visualization")
        fig = px.bar(
            top_phages,
            x='phage',
            y='key_gene_output',
            title='Phage Effectiveness Scores',
            labels={'key_gene_output': 'Effectiveness Score', 'phage': 'Phage ID'}
        )
        st.plotly_chart(fig)
        
    # Additional information
    st.subheader("Detailed Information")
    st.write("""
    - **Key Gene Output**: Score based on key gene matching (higher is better)
    - **WGS Output**: Score based on whole genome sequence analysis
    """)
    
    # Show all available phages
    st.subheader("All Available Phages")
    st.dataframe(filtered_df[['phage', 'key_gene_output', 'wgs_output']].sort_values('key_gene_output', ascending=False))

# Main app
def main():
    if st.session_state.current_page == "Home":
        show_home_page()
    elif st.session_state.current_page == "Sample Analysis":
        show_analysis_page()
    elif st.session_state.current_page == "Results":
        show_results_page()

if __name__ == "__main__":
    main() 