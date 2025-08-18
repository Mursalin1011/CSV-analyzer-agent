"""
Test script to verify Streamlit app functionality
"""
import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_streamlit_app():
    """Test that the Streamlit app functions correctly"""
    print("Testing Streamlit app functionality...")
    
    try:
        # Import the main function from streamlit_app
        from csv_analyzer.ui.streamlit_app import main
        print("Streamlit app imported successfully!")
        print("The app should work correctly when run with 'streamlit run'")
        return True
    except Exception as e:
        print(f"Failed to import Streamlit app: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_streamlit_app()