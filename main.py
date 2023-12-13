import streamlit as st
import pandas as pd
from util import extract_financial_data

# Set the display option to show all columns
pd.set_option('display.max_columns', None)
st.title("Financial Data Extraction Tool")


left_column, right_column = st.columns([4, 4])

financial_data_df = pd.DataFrame({
        "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
        "Value": ["  ", " ", " ", " ", " "]
    })

# Add elements to the left column
with left_column:
    news_article = st.text_area('', height=300,placeholder='Enter the news article here...')  # Larger text area
    if st.button('Extract'):
        financial_data_df=extract_financial_data(news_article)

# Add elements to the right column
with right_column:
    st.dataframe(financial_data_df,)