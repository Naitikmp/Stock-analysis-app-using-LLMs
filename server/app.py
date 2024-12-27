from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
from bs4 import BeautifulSoup
import requests
import re
from langchain.agents import Tool, initialize_agent
from langchain_community.chat_models import ChatOpenAI
# from langchain_community.tools import DuckDuckGoSearchRun

app = Flask(__name__)
CORS(app)

def get_stock_price(ticker):
    if "." in ticker:
        ticker = ticker.split(".")[0]
    ticker = ticker.replace(" ", "") + ".NS"    
    stock = yf.Ticker(ticker)
    df = stock.history(period="1y")
    df = df[["Close","Volume"]]
    df.index=[str(x).split()[0] for x in list(df.index)]
    df.index.rename("Date",inplace=True)
    return df.to_string()

def google_query(search_term):
    if "news" not in search_term:
        search_term = search_term+" stock news"
    url = f"https://www.google.com/search?q={search_term}"
    url = re.sub(r"\s","+",url)
    return url

def get_recent_stock_news(company_name):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    g_query = google_query(company_name)
    res=requests.get(g_query,headers=headers).text
    soup = BeautifulSoup(res,"html.parser")
    news=[]
    for n in soup.find_all("div","n0jPhd ynAwRc tNxQIb nDgy9d"):
        news.append(n.text)
    for n in soup.find_all("div","IJl0Z"):
        news.append(n.text)
    
    if len(news) > 6:
        news = news[:4]
    
    news_string = "Recent News:\n\n" + "\n".join([f"{i}. {n}" for i, n in enumerate(news)])
    return news_string

def get_financial_statements(ticker):
    if "." in ticker:
        ticker = ticker.split(".")[0]
    ticker = ticker.replace(" ", "") + ".NS"
    company = yf.Ticker(ticker)
    balance_sheet = company.balance_sheet
    if balance_sheet.shape[1]>3:
        balance_sheet = balance_sheet.iloc[:,:3]
    balance_sheet = balance_sheet.dropna(how="any")
    return balance_sheet.to_string()

def get_stock_ticker(company_name):
    try:
        ticker = yf.Ticker(company_name)
        if ticker.info:
            print("TIcker info",ticker.ticker)
            return ticker.ticker
    except Exception:
        return "Ticker not found"

def create_agent(api_key):
    llm = ChatOpenAI(temperature=0, model_name='gpt-4o-mini', api_key=api_key)
    # search = DuckDuckGoSearchRun()
    
    tools = [
        Tool(
            name="Stock Ticker Search",
            func=get_stock_ticker,
            description="Use only when you need to get stock ticker from internet"
        ),
        Tool(
            name="Get Stock Historical Price",
            func=get_stock_price,
            description="Use when you need historic share price data"
        ),
        Tool(
            name="Get Recent News",
            func=get_recent_stock_news,
            description="Use this to fetch recent news about stocks"
        ),
        Tool(
            name="Get Financial Statements",
            func=get_financial_statements,
            description="Use this to get financial statement of the company"
        )
    ]

    agent = initialize_agent(
        llm=llm,
        agent="zero-shot-react-description",
        tools=tools,
        verbose=True,
        max_iteration=4,
        handle_parsing_errors=True
    )
    
    stock_prompt="""You are a financial advisor. Give stock recommendations for given query.
    Everytime first you should identify the company name and get the stock ticker symbol for the stock.
    Answer the following questions as best you can. You have access to the following tools:

    Get Stock Historical Price: Use when you are asked to evaluate or analyze a stock. This will output historic share price data. You should input the stock ticker to it 
    Stock Ticker Search: Use only when you need to get stock ticker from internet, you can also get recent stock related news. Dont use it for any other analysis or task
    Get Recent News: Use this to fetch recent news about stocks
    Get Financial Statements: Use this to get financial statement of the company. With the help of this data company's historic performance can be evaluaated. You should input stock ticker to it

    steps- 
    Note- if you fail in satisfying any of the step below, Just move to next one
    1) Get the company name and search for the "company name + stock ticker" on internet. Dont hallucinate extract stock ticker as it is from the text. Output- stock ticker. If stock ticker is not found, stop the process and output this text: This stock does not exist
    2) Use "Get Stock Historical Price" tool to gather stock info. Output- Stock data
    3) Get company's historic financial data using "Get Financial Statements". Output- Financial statement
    4) Use this "Get Recent News" tool to search for latest stock related news. Output- Stock news
    5) Analyze the stock based on gathered data and give detailed analysis for investment choice. provide numbers and reasons to justify your answer. Output- Give a single answer if the user should buy,hold or sell. You should Start the answer with Either Buy, Hold, or Sell in Bold after that Justify.

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do, Also try to follow steps mentioned above
    Action: the action to take, should be one of [Get Stock Historical Price, Stock Ticker Search, Get Recent News, Get Financial Statements]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times, if Thought is empty go to the next Thought and skip Action/Action Input and Observation)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    Begin!

    Question: {input}
    Thought:{agent_scratchpad}"""
    
    agent.agent.llm_chain.prompt.template = stock_prompt
    return agent

@app.route('/analyze', methods=['POST'])
def analyze_stock():
    data = request.json
    api_key = data.get('apiKey')
    stock = data.get('stock')
    
    if not api_key or not stock:
        return jsonify({'error': 'Missing API key or stock name'}), 400
    
    try:
        agent = create_agent(api_key)
        response = agent(f'Is {stock} a good investment choice right now?')
        return jsonify({'analysis': response['output']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)