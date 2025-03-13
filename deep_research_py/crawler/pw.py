#使用playwright 打开 chromium 浏览器，访问网站，等待60s，保存 storage_state 到 deep_research_py/state.json
import asyncio
from playwright.async_api import async_playwright

async def save_browser_state():
    async with async_playwright() as p:
        # 启动 Chromium 浏览器（headless 模式可关闭调试）
        browser = await p.chromium.launch(headless=False)
        
        # 创建浏览器上下文
        context = await browser.new_context(storage_state='deep_research_py/state.json')
        
        # 创建新页面
        page = await context.new_page()
        
        # 访问目标网站
        await page.goto("https://www.google.com")  # 替换为你的目标网址
        
        # 等待 60 秒（单位：毫秒）
        await page.wait_for_timeout(60000)
        
        # 保存浏览器状态到文件
        await context.storage_state(path="deep_research_py/state.json")
        
        # 关闭浏览器
        await browser.close()

# 运行异步函数
asyncio.run(save_browser_state())