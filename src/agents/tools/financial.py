# Quantitative Analysis Toolkit

from typing import Type, Dict, Any, Optional
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import yfinance as yf

# Input Schemas (Input Rules that goes to the tool)

class StockAnalysisInput(BaseModel):
    '''
        Input Schema for the fundamental Analysis Tool
        Enforces that a ticket symbol which is provided as a string
        ... -> Elipses
    '''
    ticker : str = Field(...,description = "The stock Ticker Symbol (eg. 'AAPL','MSFT')")

class CompareStocksInput(BaseModel):
    '''
        Input Schema for Compare Stocks Tool
        Requires to distinct tickers : ticker_a and ticker_b
    '''
    ticker_a:  str = Field(..., description = "The First Stock Ticker to Analyze")
    ticker_b:  str = Field(..., description = "The Second Stock Ticker to Analyze Agains")

# Building tools (Tool Definitions)
class FundamentalAnalysisTool(BaseTool):
    '''
        CrewAI Tool that extracts the fundamental metrics for a stock.
        This tool will act as screening analyst , providing the raw data to
        determine - stock in Undervalued, Overvalued, Volatile
    '''
    name : str  = "Fetch Fundamental Metrics"
    description : str = ("Fetches key metrics for a specific stock ticker.\
                        useful for quantitative analysis , returns a JSON formatted.\
                        data including - P/E ration, Beta, Market Cap, EPS, 52 Week High and Low")
    
    args_schema = Type[BaseModel] = StockAnalysisInput

    def _run(self, ticker: str) -> str:
        '''
        Executes the data fetching from the yahoo finance
        Args: ticker (str) :
        returns: stringified JSON dictionary contains the selected metrics
        or an error message if it fails
        '''

        try:
            # Initialize the ticket object
            stock = yf.Ticker(ticker)
            info : Dict[str, Any] = stock.info

            # We explicitly select the robust metrics to avoid context-window bloat
            metrics = {
                "Ticker": ticker.upper(),
                "Current Price": info.get("currentPrice","N/A"),
                "Market Cap": info.get("marketCap","N/A"),
                "P/E Ratio (Trailing)": info.get("trailingPE","N/A"),
                "Forward P/E": info.get("forwardPE","N/A"),
                "PEG Ratio":info.get("pegRatio","N/A"),
                "Beta (Volatility)":info.get("beta","N/A"),
                "EPS (trailing)":info.get("trailingEps","N/A"),
                "52 Week High":info.get("fiftyTwoWeekHigh","N/A"),
                "52 Week Low":info.get("fiftyTwoWeekLow","N/A"),
                "Analyst Recommandation":info.get("recommandationKey","none")
            }

            return str(metrics)
        except Exception as e:
            return f"Error fetching fundamental data for '{ticker}' : {str(e)}'"
        

class CompareStocksTool(BaseTool):
    '''
    Calculates the relative performance between two assets
    answer the question "Did NVIDIA beat APPLE last year ?"
    calculates the percentage change in the price over 1-year period
    '''
    name: str = "Compare Stock Performance"
    description: str =("Compares the historical performance of two stocks over the \
                       last 365 days, returns the percentage gain or loss for both"
                       "assets")
    args_schema: Type[BaseModel] = CompareStocksInput

    def _run(self, ticker_a: str, ticker_b: str) -> str:
        '''
            fetch the historical data and calculates the percentage return
            formula: (last price - first price)/ (first price) * 100
        '''
        try:
            tickers = f"{ticker_a} {ticker_b}"
            data = yf.download(tickers, period="1y", progress=False)['Close']

            # Helper function to calculate the return
            def calculate_return(symbol:str) -> float:
                start_price = data[symbol].iloc[0] #price of day 1
                end_price = data[symbol].iloc[-1] #price today
                return ((end_price-start_price)/(start_price)*100)
            
            perf_a = calculate_return(ticker_a)
            perf_b = calculate_return(ticker_b)
            
            return f"Performance Comparison (Last 1 Year)"
        except Exception as e:
            return f"Error Comparing Stocks '{ticker_a}' and '{ticker_b}' : {str(e)}"