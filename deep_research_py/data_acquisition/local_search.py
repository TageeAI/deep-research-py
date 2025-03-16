from deep_research_py.test.test_pdf_download import download_pdf
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
import requests
import os
from urllib.parse import urlparse


class Crawl4AIScraper(Scraper):
    def __del__(self):
        pass
    async def setup(self):
        """Initialize the scraper resources."""
        await self.crawler.start()
        pass

    async def teardown(self):
        """Clean up the scraper resources."""
        await self.crawler.close()
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
            semaphore_count=1
        )
        
        self.crawler = AsyncWebCrawler(config=self.browser_config)
        
        return 
    
    def download_pdf(self, url, parent_dir:str = './') -> bool:
        """
        检查 URL 是否为 PDF 文件，如果是，则下载到指定父目录。
        
        参数:
        - url: 要检查和下载的 URL 字符串
        - parent_dir: 保存 PDF 文件的父目录路径
        """
        try:
            # 确保父目录存在，如果不存在则创建
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir)

            # 发送 HEAD 请求检查文件类型（避免直接下载整个文件）
            # response = requests.head(url, allow_redirects=True)
            # content_type = response.headers.get('Content-Type', '').lower()
            content_type = ""
            # 检查是否为 PDF 类型
            if 'application/pdf' in content_type or url.lower().endswith('.pdf'):
                print(f"检测到 PDF 文件: {url}")
                
                # 获取文件名（从 URL 中提取，或使用默认名）
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path)
                if not filename:
                    filename = 'downloaded_file.pdf'  # 默认文件名
                elif not filename.lower().endswith('.pdf'):
                    filename += '.pdf'

                # 构建保存路径
                # 如果filename长度超过100，则截断最后100个字符
                if len(filename) > 100:
                    filename = filename[-100:]
                save_path = os.path.join(parent_dir, filename)

                # 下载文件
                print(f"正在下载到: {save_path}")
                response = requests.get(url, stream=True, timeout=30)  # 使用流模式下载大文件
                response.raise_for_status()  # 检查请求是否成功

                # 以二进制写入文件
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):  # 分块写入
                        if chunk:
                            f.write(chunk)
                print(f"下载完成: {save_path}")
                return True
            else:
                print(f"URL 不是 PDF 文件: {url} (Content-Type: {content_type})")
                return False

        except requests.exceptions.RequestException as e:
            print(f"下载失败: {e}")
            return True
        except Exception as e:
            print(f"发生错误: {e}")
            return True
    async def scrape(self, url: str, **kwargs) -> ScrapedContent:
        #如果url 是pdf，则下载pdf文件
        downloaded = self.download_pdf(url, parent_dir="./PDFs")
        if downloaded :
            return ScrapedContent(
                url=url,
                html="",
                text="",
                status_code=200,
                metadata={
                    # "title": title,
                    # "headers": response.headers if response else {},
                },
            )

        # async with AsyncWebCrawler(config=self.browser_config) as crawler:
        #     result = await crawler.arun(
        #         url=url,
        #         config=self.scrape_config
        #     )
        result = await self.crawler.arun(
            url=url,
            config=self.scrape_config
        )
        if result.success:            
            main_text = trafilatura.extract(result.html,favor_precision=True) 
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
            return ScrapedContent(
                url=url,
                html="",
                text="",
                status_code=200,
                metadata={
                    # "title": title,
                    # "headers": response.headers if response else {},
                },
            ) 
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
            extraction_strategy=JsonCssExtractionStrategy(schema)            
        )   # Default crawl run configuration

        
        self.scrape_config = CrawlerRunConfig(
            magic=True,
            simulate_user=True,
            override_navigator=True,
            scan_full_page=True,
            #scroll_delay=1,
            cache_mode=CacheMode.DISABLED
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

