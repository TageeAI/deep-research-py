import asyncio
from crawl4ai import AsyncWebCrawler, JsonCssExtractionStrategy
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
import json

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
            "name": "markdown",
            "selector": "[data-snf][data-sncf] ",
            "type": "text"
        }
    ]
}
async def main():
    browser_config = BrowserConfig(
        storage_state='./state.json',
        headless=False,
        use_persistent_context=True,
        user_data_dir='test/my_user_data')  # Default browser configuration
    run_config = CrawlerRunConfig(
        extraction_strategy=JsonCssExtractionStrategy(schema),
        scan_full_page=True,
        scroll_delay=2)   # Default crawl run configuration

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://www.google.com/search?q=apple",
            config=run_config
        )
        print(result.markdown)  # Print clean markdown content
        print(result.extracted_content)

if __name__ == "__main__":
    #open file path my_user_data
    with open("./state.json", "r") as f:
        state_data = json.load(f)
        #print(state_data)
    asyncio.run(main())