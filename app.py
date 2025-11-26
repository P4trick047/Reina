#importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
import datetime
from datetime import datetime

def load_data(uploaded_file):
    """Loads dataset from an uploaded CSV file."""
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None
