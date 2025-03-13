from .search import SearchEngine, SearchResult
from typing import List, Dict, Any
from crawl4ai import JsonCssExtractionStrategy, BrowserConfig, CrawlerRunConfig, CacheMode, AsyncWebCrawler
import trafilatura
import json
import asyncio
import os
import types
from pydantic import BaseModel, Field
from deep_research_py.utils import logger
from urllib.parse import quote
from .scraper import Scraper, ScrapedContent

class Crawl4AIScraper(Scraper):

    async def setup(self):
        """Initialize the scraper resources."""
        pass

    async def teardown(self):
        """Clean up the scraper resources."""
        pass
    def __init__(self, headless: bool = False, storage_state: str=None):

        #获得本文件的路径
        current_file_path = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file_path)
        #读取本文件路径下的state.json文件
        state_file_path = os.path.join(current_dir, "state.json")
        
        #如果state_file_path文件存在，则读取文件内容，并转换为字典
        if os.path.exists(state_file_path):
            with open(state_file_path, "r") as f:
                logger.info("state.json文件存在，正在读取文件内容...")
                storage_state = json.load(f)
            
        
        self.browser_config = BrowserConfig(
            accept_downloads=True,
            headless=headless,
            storage_state=storage_state,  
            user_data_dir="./",
            use_managed_browser=True,
            use_persistent_context=True,

            
        )  # Default browser configuration


        self.scrape_config = CrawlerRunConfig(
            scan_full_page=True,
            scroll_delay=0.2,
            cache_mode=CacheMode.DISABLED,
            semaphore_count=1,
        )
        return 

    async def scrape(self, url: str, **kwargs) -> ScrapedContent:
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            result = await crawler.arun(
                url=url,
                config=self.scrape_config
            )
            
        if result.success:
            
            main_text = trafilatura.extract(result.html,favor_precision=True)

            #self.save_content({"url":url, "main_text":main_text})
            
            return ScrapedContent(
                url=url,
                html=result.html,
                text=main_text,
                status_code=result.status_code,
                metadata={
                    # "title": title,
                    # "headers": response.headers if response else {},
                },
            )

        else:
            print("Crawl failed:", result.error_message)
            return ""    
        return contents
    
class Crawl4AIEngine(SearchEngine):
    def __init__(self, storage_state: str=None):
        schema = {
            "name": "SERP",
            "baseSelector": "#search [jscontroller][data-hveid][data-ved]:nth-child(1):not([data-initq])",    # Repeated elements
            # "baseFields": [
            #     {"name": "url", "type": "attribute", "attribute": "mu"}
            # ],
            "fields": [
                {
                    "name": "title",
                    "selector": "[data-snf][data-snhf] h3",
                    "type": "text"
                },
                {
                    "name": "url",
                    "selector": "a",
                    "type": "attribute",
                    "attribute": "href"

                },
                {
                    "name": "description",
                    "selector": "[data-snf][data-sncf] ",
                    "type": "text"
                }
            ]
        }
        
        #获得本文件的路径
        current_file_path = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file_path)
        #读取本文件路径下的state.json文件
        state_file_path = os.path.join(current_dir, "state.json")
        
        #如果state_file_path文件存在，则读取文件内容，并转换为字典
        if os.path.exists(state_file_path):
            with open(state_file_path, "r") as f:
                logger.info("state.json文件存在，正在读取文件内容...")
                storage_state = json.load(f)
            
        
        self.browser_config = BrowserConfig(
            accept_downloads=True,
            headless=False,
            storage_state=storage_state,  

            use_managed_browser=True,
            use_persistent_context=True,

            
        )  # Default browser configuration
        self.search_config = CrawlerRunConfig(
            scan_full_page=True,
            scroll_delay=1,
            cache_mode=CacheMode.DISABLED,
            extraction_strategy=JsonCssExtractionStrategy(schema),
            semaphore_count=1,
            
        )   # Default crawl run configuration

        
        self.scrape_config = CrawlerRunConfig(
            magic=True,
            simulate_user=True,
            override_navigator=True,
            scan_full_page=True,
            #scroll_delay=1,
            cache_mode=CacheMode.DISABLED,
            semaphore_count=1,
        )
        return 

    async def search(
        self, query: str, num_results: int = 10, **kwargs
    ) -> List[SearchResult]:
        response = {"success":True}
        #url encode the query
        query = quote(query)
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            result = await crawler.arun(
                url=f"https://www.google.com.hk/search?q={query}",
                config=self.search_config
            )
            
        # iter over the results then crawl the links
        contents = result.extracted_content
        results = json.loads(contents)
        
        standardized_results = []
        for i, result in enumerate(results):
            standardized_results.append(
                SearchResult(
                    title=result.get("title", ""),
                    url=result.get("url", ""),
                    description=result.get("description", ""),
                    position=i + 1,
                    metadata=result,
                )
            )

        return standardized_results[:num_results]

