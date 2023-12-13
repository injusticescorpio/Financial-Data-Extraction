import os

from openai import OpenAI
import json
from os.path import join, dirname
from dotenv import load_dotenv
import pandas as pd

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

API_KEY = os.environ.get("API_KEY")


client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("API_KEY"),
)

def prompt_financial(message):
    data="""
    Please retrieve company name, revenue, net income and earnings per share (a.k.a. EPS)
    from the following news article. If you can't find the information from this article 
    then return "". Do not make things up.    
    Then retrieve a stock symbol corresponding to that company. For this you can use
    your general knowledge (it doesn't have to be from this article). Always return your
    response as a valid JSON string. The format of that string should be this, 
    {
        "Company Name": "Walmart",
        "Stock Symbol": "WMT",
        "Revenue": "12.34 million",
        "Net Income": "34.78 million",
        "EPS": "2.1 $"
    }
    News Article:
    ============
    """
    return data +f"{message}"

def extract_financial_data(text):
    prompt=prompt_financial(text)
    print(prompt)    
    response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="gpt-3.5-turbo")
    try:
        data = json.loads(response.choices[0].message.content)
        df=pd.DataFrame(data.items(),columns=["Measure","Value"])
        return df
    except(json.JSONDecodeError,IndexError):
        pass
    return pd.DataFrame({
        "Measure":["Company Name","Stock Symbol","Revenue","Net Income","EPS"],
        "Value":["","","","",""]
    })
    
        
    







if __name__ == "__main__":
    df=extract_financial_data('''
    Tesla's Earning news in text format: Tesla's earning this quarter blew all the estimates. They reported 4.5 billion $ profit against a revenue of 30 billion $. Their earnings per share was 2.3 $
    ''')
    print(df)