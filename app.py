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
        
        # Show completion messages and automatically move to results
        if st.session_state.analysis_complete:
            status_text.text("Analysis completed!")
            st.success('Analysis complete!')
            st.info('Identified bacteria: GL538315')
            time.sleep(1)  # Show completion message for 2 seconds
            st.session_state.current_page = "Results"
            st.rerun()
            
        # Add vertical spacing at the bottom
        st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

def show_results_page():
    st.header("Analysis Results")
    
    # Load and display data
    df = load_data()
    
    # Hardcode the bacterium
    bacterium = "GL538315"
    st.success(f"Identified Bacteria: {bacterium}")
    
    # Filter data and prepare for display
    filtered_df = df[df['bacterium'] == bacterium].copy()
    filtered_df['Probability (%)'] = (filtered_df['key_gene_output'] * 100).round(3)
    filtered_df = filtered_df.sort_values('Probability (%)', ascending=False)
    
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
        st.markdown("""
        <div style='padding: 20px; margin-top: 50px;'>
            <h3 style='color: #ffd700; font-size: 24px;'>Phage Cocktail GL-538315 - Yellow</h3>
            <p style='color: #ffffff; font-size: 20px; margin-top: 20px;'>Recommended dosage: 1 vial per day</p>
            <p style='color: #ffffff; font-size: 18px; margin-top: 20px;'>Target: Staphylococcus aureus GL538315</p>
        </div>
        """, unsafe_allow_html=True)
    
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
        display_df = filtered_df[['phage', 'Probability (%)']].rename(columns={'phage': 'Phage'})
        styled_df = display_df.style.apply(highlight_recommended, axis=1).format({'Probability (%)': '{:.1f}%'})
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
    with col2:
        st.subheader("Visualization")
        # Create a bar chart with highlighted recommended phages
        fig = px.bar(
            filtered_df,
            x='phage',
            y='Probability (%)',
            title='Phage Effectiveness',
            color=filtered_df['Probability (%)'] > 75,
            color_discrete_map={True: '#00cc00', False: '#2196F3'},
            labels={'phage': 'Phage ID', 'Probability (%)': 'Effectiveness (%)'}
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