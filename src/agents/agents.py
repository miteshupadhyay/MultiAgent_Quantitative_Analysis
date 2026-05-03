"""
    Agents Defintions Module

    Defines the specific AI personas that will execute the financial analysis workflow
    Each Agent is equipped with a distinct set of tools and a backstory

    Agents: 
        Quantitative Analyst Agent : Focuses on Financial Metrics
        Investment Strategist Agent: Focus on qualitative news, sentiment , synthesis
"""
from typing import Tuple
from crew import Agent
from src.agents.tools.financial import FundamentalAnalysisTool, CompareStocksTool
from src.agents.tools.scraper import SentimentSearchTool

def create_agents() -> Tuple[Agent, Agent]:
    '''
        Factory Pattern

        It returns a tuple containing (quant_agent, strategist_agent)
    '''

    # Quant Analyst Agent : Use yfinance tools
    quant_agent  = Agent(
        role= "Senior Quantitative Analyst",
        goal = "Analyze the financial health and historical performance of the stock",
        backstory= (
            "You are a veteran financial analyst with over 2 decades of experience\
             you do not care about news headlines or rumors, you only trust data\
             you judge the companies basis their balance sheet, P/E Ratios, earning growth(EPS)\
             and volatility(Beta)\
            Your reports are concise and number heavy"
        ),
        verbose = True,
        memory = True,
        tools = [
            FundamentalAnalysisTool(),
            CompareStocksTool()
        ],
        allow_delegation = False # We want our agent to do it's own work
    )


    # Strategist Agent : uses firecrawl
    # Job of this agent is to explain "why" the numbers are the way they are

    strategist_agent = Agent(
        role="Cheif Investment Strategist",
        goal = "Synthesize quantitative data with the market sentiment to form a recommandation",
        backstory =(
            "You are a visionary investment strategist, who looks beyond spreadsheets\
            You understand stock prices and driven by human psychology, news and \
            leadership changes. You read the news to find 'narrative' behind any stock.\
            You combine the Quant's numbers with your news findings to give a final\
            'BUY','SELL','HOLD' recommandations."
        ),
        verbose = True,
        memory = True,
        tools = [
            SentimentSearchTool()
        ],
        allow_delegation = False # We want our agent to do it's own work
    )

    return quant_agent, strategist_agent