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
    bad_url = ["https://funds.hexun.com/2025-03-15/217917923.html",
        "https://www.spdbi.com/getfile/index/action/images/name/%E6%96%B0%E8%83%BD%E6%BA%90%E6%B1%BD%E8%BD%A6%E8%A1%8C%E4%B8%9A2025%E5%B9%B4%E5%B1%95%E6%9C%9B%EF%BC%9A%E7%BB%BF%E8%83%BD%E6%B5%AA%E6%BD%AE%E3%80%81%E5%87%BA%E6%B5%B7%E9%A2%86%E8%88%AA%E3%80%81%E6%99%BA%E9%A9%BE%E6%9C%AA%E6%9D%A5_%E6%B5%A6%E9%93%B6%E5%9B%BD%E9%99%85%E7%A0%94%E7%A9%B6.pdf",
               "http://www.sina.com.cn",
               "https://pic.bankofchina.com/bocappd/rareport/202501/P020250108516286149745.pdf",
               "https://assets.kpmg.com/content/dam/kpmg/cn/pdf/zh/2023/03/key-points-of-the-two-sessions-2023.pdf",
               "http://www.bulletin.cas.cn/doi/10.16418/j.issn.1000-3045.20241225002",
               "http://www.news.cn/politics/20250306/119ea65c9bd84808a8a75ae5772d7f8b/c.html",
               "http://lianghui.people.com.cn/2025/n1/2025/0312/c460142-40437673.html",
               "http://www.news.cn/politics/20240313/40b5dc54d6db4470ab90be0323b638ff/c.html"]
    await scraper.setup()
    result = await scraper.scrape(bad_url[0])
    
    await scraper.teardown()

    print(result.text)

asyncio.run(main())
