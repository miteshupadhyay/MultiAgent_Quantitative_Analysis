"""
Task Definitions Module:

Tasks that our Agent must execute.
It acts as a prompt engineering layer for our application/agentic system.

Key Features:
context injection :  strategist's task explictly waits for and receives the output from the Quant
Agent's task to ensure dta driven reasoning.
"""

from crewai import Task, Agent

def create_tasks(quant_agent: Agent, strategist_agent: Agent, ticker: str) -> list[Task]:
    '''
    Args:
     quant_agent: Financial metrics
     strat_agent: news and synthesis
     ticker: stock symbol


     returns the list of task objects in the order of execution
    '''

    quant_task = Task(
        description=(
            f"Analyze the financial health of ticker '{ticker}'"
            "1. Use the FundamentalAnalysisTool to fetch P/E, EPS, Beta and Market Cap"
            "2. USe the CompareStocksTool to compare '{ticker}' against 'SPY' (S&P 500)"
            " to see its relative performance over the last year"
            "3. Identify any major numerical red flags (e.g. negative EPS, extremly high P/E Ratio)"
            "and output the concise summary of the hard numbers"
        ),
        expected_output="A structured summary of financial metrics and 1-Year performance comparison",
        agent=quant_agent
    )


    recommandation_task= Task(
        description=(
            f"Formulate a final investment recommandation for '{ticker}'"
            "1. Read the financial metrics provided by the Quantitative Analyst"
            "2. Use the SentimentSearchTool to find the top 3 recent news articles"
            " or analyst ratings for '{ticker}'. Look for leadership changes,"
            " regulatory lawsuits, or product launches"
            " 3. SYNTHESIZE the number (Quant) with the narrative (News)"
            "    - If numbers are good but news is bad (eg.lawsuit), be cautios"
            "    - If numbers are bad but new is hype, be skeptical"
            "4. Provide a final verdict . "BUY", "SELL" or "HOLD", with a clear reason"
        ),
        expected_output=" A comprehensive Markdown report including the verdict , key metrics",
        agent=strategist_agent,
        context=[quant_task],  # Passes Task 1's output 
        output_file=f"investment_report_{ticker}.md" # Saves the final report to disk
    )

    return [quant_task, recommandation_task]