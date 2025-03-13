from deep_research_py.outline import generate_outline
from deep_research_py.meta_think import extract_meta_thinks
from deep_research_py.ai.providers import AIClientFactory
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

print(os.getenv("OLLAMA_NUM_PREDICT"))
client = AIClientFactory.get_client()
#outline.generate_outline("tesla", "研究恐慌情绪", client, "qwen2.5:latest")

print(client)
async def test_outline():
    outline = await generate_outline("tesla", "研究恐慌情绪", client, "gemma3:27b-it-fp16")
    print(outline)
    with open("outline.txt", "w+", encoding='utf-8') as f:
        f.write(outline)
    return outline
async def main():
    await test_outline()

    # with open("outline.txt", "r", encoding='utf-8') as f:
    #     outline = f.read()
    
    
    # for l in (extract_meta_thinks(outline)):
    #     print(l)
    # # print(outline)
    # # meta_thinks = extract_meta_with_context(outline)
    # # print(meta_thinks)
    


asyncio.run(main())