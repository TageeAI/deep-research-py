from deep_research_py.outline import generate_outline
from deep_research_py.ai.providers import AIClientFactory
import asyncio
client = AIClientFactory.get_client()
#outline.generate_outline("tesla", "研究恐慌情绪", client, "qwen2.5:latest")

async def main():
    outline = await generate_outline("tesla", "研究恐慌情绪", client, "qwen2.5:latest")
    print(outline)

asyncio.run(main())