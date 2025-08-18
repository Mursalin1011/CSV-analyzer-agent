import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Run the Streamlit app
if __name__ == "__main__":
    from csv_analyzer.ui.streamlit_app import main
    main()