# Phage Therapy Visualization Prototype

## Project Overview
This project is a prototype visualization tool for phage therapy selection. It demonstrates how machine learning can assist in identifying the most effective phages to combat specific bacterial infections.

## Problem Context
Bacteriophages (phages) are viruses that infect and kill bacteria. They represent a promising alternative to antibiotics, especially for antibiotic-resistant infections. However, selecting the right phages for specific bacterial infections is complex and requires sophisticated analysis.

## Solution
Our prototype provides a simple, user-friendly interface to visualize phage-bacterium interactions and their probabilities. The system follows these steps:

1. **Sample Collection**: User collects a bacterial sample via swab
2. **Sequencing**: Sample is processed through a portable sequencer
3. **Analysis**: Machine learning model analyzes the sequence data
4. **Visualization**: Results are displayed showing:
   - Identified bacteria
   - Recommended phages
   - Interaction probabilities
   - Key gene information

## Technical Implementation
- Built using Streamlit for rapid prototyping
- Visualizes pre-computed results from ML model
- Focuses on clear, intuitive presentation of complex data
- Includes interactive elements for exploring phage-bacterium relationships

## Data Structure
The visualization uses a CSV file containing:
- Phage identifiers
- Bacterium identifiers
- Key gene output scores
- Whole genome sequence (WGS) output scores
- Number of key genes for both phages and bacteria

## Future Enhancements
- Real-time data processing
- Integration with sequencing hardware
- More detailed visualization of gene interactions
- Clinical trial data integration
- Treatment success prediction

## Getting Started
1. Install required dependencies
2. Run the Streamlit application
3. Explore the visualization interface

## Note
This is a hackathon prototype focusing on demonstrating the concept rather than production-ready implementation. 