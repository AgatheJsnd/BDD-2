
try:
    import streamlit
    print("streamlit ok")
    import pandas
    print("pandas ok")
    import plotly
    print("plotly ok")
    import openpyxl
    print("openpyxl ok")
    import tqdm
    print("tqdm ok")
    import mistralai
    print("mistralai ok")
    from src.profile_generator import ProfileGenerator
    print("profile_generator ok")
    from src.csv_processor import CSVProcessor
    print("csv_processor ok")
    print("All imports successful!")
except Exception as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
