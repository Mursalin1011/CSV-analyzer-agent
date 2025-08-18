"""
Streamlit implementation for CSV Analyzer Agent
"""

import sys
import os

# Add the current directory to the Python path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Use the new modular implementation
if __name__ == "__main__":
    from csv_analyzer.ui.streamlit_app import main
    main()