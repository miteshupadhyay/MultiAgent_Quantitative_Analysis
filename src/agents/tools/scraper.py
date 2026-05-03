'''
    Web Scraping and sentiment extraction Module
    this module integrate with firecrawl api to act as the eyes of the system
    it searches for qualitative data news, analyst opinions and market rumors

    class: SentimentSearchTool : Searches the web for recent articles

'''

from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from firecrawl import FirecrawlApp
from src.shared.config import settings

# Input Schema
class FireCrawlSearchInput(BaseModel):
    query: str = Field(..., description="The search query string(e.g. 'NVDA recent analyst rating')")

# Tool Definition
class SentimentSearchTool(BaseTool):
    '''
        Performs the semantic web search and returns the scraped content.
        use firecrawl , extract full page content in markdown format
    '''
    name: str = "Search Stock News"
    description: str = ("Searches the web for the latest news, analyst rating\
                        and surrounding market sentiment for a specific stock"
                        "Returns a summary for top 3 relevant articles")
    
    args_schema: Type[BaseTool] = FireCrawlSearchInput
    
    def _run(self, query: str) -> str:
        '''
        Executes the search via firecrawl
        Args: query(str): the search topic
        returns: markdown string format content of the top searched results
        '''

        # Ensure that API key is present
        if not settings.firecrawl_api_key:
            return "Error : FIRECRAWL API KEY is missing in configuration"
        
        try:
            app = FirecrawlApp(api_key=settings.firecrawl_api_key)

            #perform the web search : limit the results to 3
            results = app.search(query=query,
                                 limit=3,
                                 scrape_options = {"formats": ["markdown"]}
                                 )
            return str(results)
        except Exception as e:
            return f"Error Executing the FireCrawl search for query"
