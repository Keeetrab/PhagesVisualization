import streamlit as st
import pandas as pd
import plotly.express as px
import time

# Processing timing configuration
PROCESSING_TIMES = {
    'initial_delay': 1.5,  # Initial delay before starting analysis
    'step_delay': 1.5,   # Delay between processing steps
    'completion_delay': 2  # Delay before showing completion message
}

# Data file configuration
DATA_FILE = 'data/Modelresults_with_names_v4.csv'  # Path to the input data file

# Analysis configuration
SELECTED_BACTERIA = "NZ_CP029736"  # The bacterium to analyze

# Set page config
st.set_page_config(
    page_title="Phage Therapy Analysis",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimal CSS styling for button and progress bar
st.markdown("""
    <style>
        .stButton>button {
            background-color: #FD0363;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #CC095D;
            color: white;
        }
        .stProgress > div > div > div > div {
            background-color: #FD0363;
        }
        /* Toast notification styling */
        .stAlert {
            background-color: #FD0363 !important;
            border-color: #FD0363 !important;
        }
        .stAlert .stAlert-content {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
    st.session_state.analysis_complete = False
    st.session_state.progress = 0
    st.session_state.current_step = 0

# Load data
@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

def reset_analysis_state():
    st.session_state.analysis_complete = False
    st.session_state.progress = 0
    st.session_state.current_step = 0

def show_home_page():
    # Center-aligned container
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🧬 Phage Therapy Analyzer")
        
        # Create two columns for GIF and instructions
        gif_col, instr_col = st.columns([1, 1])
        
        with gif_col:
            # Display the GIF animation
            st.image("./assets/minION_manual_large.gif", output_format="GIF")
        
        with instr_col:
            # Instructions box
            st.markdown("""
            <div style='padding: 20px;'>
                <h2 style='text-align: center; color: #ffffff;'>Sample Collection Instructions</h2>
                <ol style='font-size: 18px;'>
                    <li>Clean the sampling area thoroughly</li>
                    <li>Use the sterile swab provided in the kit</li>
                    <li>Collect the sample with a rolling motion</li>
                    <li>Place the swab in the analyzer port</li>
                </ol>
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
    # Center-aligned container
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🧬 Sample Analysis")
        
        # Add vertical spacing
        st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <p style='color: #ffffff;'>Please do not remove the sample during analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        
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
                    time.sleep(PROCESSING_TIMES['initial_delay'])  # Initial delay before starting
                
                status_text.text(steps[st.session_state.current_step])
                st.session_state.progress = (st.session_state.current_step + 1) / len(steps)
                progress_bar.progress(st.session_state.progress)
                time.sleep(PROCESSING_TIMES['step_delay'])  # Slightly longer delay between steps
                st.session_state.current_step += 1
                st.rerun()
            else:
                st.session_state.analysis_complete = True
                st.rerun()
        
        # Show completion messages and automatically move to results
        if st.session_state.analysis_complete:
            # Load data to get bacterium name
            df = load_data()
            bacterium_name = df[df['bacterium'] == SELECTED_BACTERIA]['Bacterium name'].iloc[0]
            
            status_text.text("Analysis completed!")
            st.success('Analysis complete!')
            st.info(f'Identified bacteria: {bacterium_name} ({SELECTED_BACTERIA})')
            time.sleep(PROCESSING_TIMES['completion_delay'])  # Show completion message for 2 seconds
            st.session_state.current_page = "Results"
            st.rerun()
            
        # Add vertical spacing at the bottom
        st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

def show_results_page():
    st.header("Analysis Results")
    
    # Load and display data
    df = load_data()
    
    # Get the bacterium name for the selected ID
    bacterium_name = df[df['bacterium'] == SELECTED_BACTERIA]['Bacterium name'].iloc[0]
    st.success(f"Identified Bacteria: {bacterium_name} ({SELECTED_BACTERIA})")
    
    # Filter data and prepare for display
    filtered_df = df[df['bacterium'] == SELECTED_BACTERIA].copy()
    filtered_df['Probability (%)'] = (filtered_df['key_gene_output'] * 100).round(3)
    filtered_df = filtered_df.sort_values('Probability (%)', ascending=False)
    
    # Detailed results section
    st.markdown("""
    <div style='text-align: center; margin: 20px 0; padding: 20px; background-color: #1a1a1a; border-radius: 10px;'>
        <h2 style='color: #ffffff;'>Detailed Analysis</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Display detailed results in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Recommended Phages")
        st.markdown("""
        <div style='margin-bottom: 20px;'>
            <p style='color: #00cc00; font-size: 16px;'>Phages with probability >75% are recommended for treatment</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create a styled dataframe
        def highlight_recommended(row):
            if row['Probability (%)'] > 75:
                return ['background-color: #1a3d1a; color: #ffffff'] * len(row)
            return [''] * len(row)
        
        # Display only relevant columns with renamed columns
        display_df = filtered_df[['phage', 'Phage Name', 'Probability (%)']].rename(columns={
            'phage': 'Phage ID',
            'Phage Name': 'Phage Name',
            'Probability (%)': 'Probability (%)'
        })
        styled_df = display_df.style.apply(highlight_recommended, axis=1).format({'Probability (%)': '{:.1f}%'})
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
    with col2:
        st.subheader("Visualization")
        # Create a bar chart with highlighted recommended phages
        fig = px.bar(
            filtered_df,
            x='Phage Name',  # Changed from 'phage' to 'Phage Name'
            y='Probability (%)',
            title='Phage Effectiveness',
            color=filtered_df['Probability (%)'] > 75,
            color_discrete_map={True: '#00cc00', False: '#2196F3'},
            labels={'Phage Name': 'Phage Name', 'Probability (%)': 'Effectiveness (%)'}
        )
        # Update layout for dark mode
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Main vial display section
    st.markdown("""
    <div style='text-align: center; margin: 20px 0; padding: 20px; background-color: #1a1a1a; border-radius: 10px;'>
        <h2 style='color: #ffd700;'>Recommended Treatment</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for vial and information
    col1, col2 = st.columns([1, 1])
    
    # Left column - Vial image
    with col1:
        st.markdown("""
            <style>
                [data-testid="stImage"] {
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                }
            </style>
            """, unsafe_allow_html=True)
        st.image("./assets/yellow_vial.png", width=300)
    
    # Right column - Information
    with col2:
        st.markdown(f"""
        <div style='padding: 20px; margin-top: 50px;'>
            <h3 style='color: #ffd700; font-size: 24px;'>Phage Cocktail {SELECTED_BACTERIA} - Yellow</h3>
            <p style='color: #ffffff; font-size: 20px; margin-top: 20px;'>Recommended dosage: 1 vial per day</p>
            <p style='color: #ffffff; font-size: 18px; margin-top: 20px;'>Target: {bacterium_name} ({SELECTED_BACTERIA})</p>
        </div>
        """, unsafe_allow_html=True)
        
    # Additional information
    st.markdown("""
    <div style='margin-top: 20px; padding: 15px; background-color: #1a1a1a; border-radius: 5px;'>
        <h4 style='color: #ffffff;'>Treatment Recommendations</h4>
        <p style='color: #ffffff;'>Based on the analysis, the following phages are recommended for treatment:</p>
        <ul style='color: #ffffff;'>
            <li>Phages with effectiveness >75% are considered highly effective</li>
            <li>Multiple phages can be used in combination for better results</li>
            <li>Consult with a healthcare professional before proceeding with treatment</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

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