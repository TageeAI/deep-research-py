from deep_research_py.data_acquisition.local_search import Crawl4AIEngine, Crawl4AIScraper
import asyncio
import json
#read from  storage_state.json file as storage_state


searcher = Crawl4AIEngine()

scraper = Crawl4AIScraper()


#main function
async def main():
    # results = await searcher.search("tesla R&D")
    # for result in results:
    #     print(result)
    bad_url = ["http://www.sina.com.cn",
               "https://pic.bankofchina.com/bocappd/rareport/202501/P020250108516286149745.pdf",
               "https://assets.kpmg.com/content/dam/kpmg/cn/pdf/zh/2023/03/key-points-of-the-two-sessions-2023.pdf",
               "http://www.bulletin.cas.cn/doi/10.16418/j.issn.1000-3045.20241225002",
               "http://www.news.cn/politics/20250306/119ea65c9bd84808a8a75ae5772d7f8b/c.html",
               "http://lianghui.people.com.cn/2025/n1/2025/0312/c460142-40437673.html",
               "http://www.news.cn/politics/20240313/40b5dc54d6db4470ab90be0323b638ff/c.html"]
    result = await scraper.scrape(bad_url[1])

    print(result.text)

asyncio.run(main())
