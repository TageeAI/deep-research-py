import json
from deep_research_py.outline import generate_outline, extract_queries, extract_facts, extract_main_content
from deep_research_py.deep_research import deep_research, search_service
from deep_research_py.ai.providers import AIClientFactory
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

print(os.getenv("OLLAMA_HOST_ENDPOINT"))
print(os.getenv("OLLAMA_NUM_CTX"))
print(os.getenv("OLLAMA_NUM_PREDICT"))

model = os.getenv("OLLAMA_MODEL", "gemma3:27b-it-fp16")
client = AIClientFactory.get_client()
#outline.generate_outline("tesla", "研究恐慌情绪", client, "qwen2.5:latest")
async def test_outline():
    outline = await generate_outline("tesla", "研究市场恐慌情绪对股价的影响", client, model)

    print(outline)
    with open("tesla_001.txt", "w+", encoding='utf-8') as f:
        f.write(outline)
    return outline

async def test_scrape_content():
    current_path = os.path.dirname(os.path.abspath(__file__))
    with open("outline.txt", "r", encoding='utf-8') as f:
         outline = f.read()
    semaphore = asyncio.Semaphore(1)
    #print(outline)
    #把 research results 按行保存在 jsonl 格式文件中：
    with open("research_results.jsonl", "w+", encoding='utf-8') as f:
        
        for meta, goals, query in extract_queries(outline):
            print(query)
            
            research_results = await search_service.search(query,max_concurrent_scrapes=3)
            #research_results = await w(j, 1, 1, 1, client, model)
            print(research_results)
            
            research_results["meta"] = meta
            research_results["goals"] = goals
        

            f.write(json.dumps(research_results, ensure_ascii=False) + "\n")
            #break
    await search_service.cleanup()

from deep_research_py.outline import Facts

async def test_extract_facts():
    #print(f"fact is {Facts.model_json_schema()}")
    #return
    # read research_results.jsonl file into a list of dictionaries
    research_results = []
    with open("research_results.jsonl", "r", encoding='utf-8') as f:
        for line in f:
            research_results.append(json.loads(line))
    
    # write facts into a jsonl file
    with open("facts.jsonl", "w+", encoding='utf-8') as facts_file:
        for research_result in research_results:
            #print(research_result)
            for c in research_result["data"]:
                #print(c)
                facts = await extract_facts(research_result['meta'], research_result['goals'], c["title"], c["content"], 1, 1, client, model)
                print(facts)
                facts_file.write(json.dumps(facts, ensure_ascii=False) + "\n")
                
async def test_extract_main_content():
    #print(f"fact is {Facts.model_json_schema()}")
    #return
    # read research_results.jsonl file into a list of dictionaries
    research_results = []
    with open("research_results_badcase.jsonl", "r", encoding='utf-8') as f:
        for line in f:
            research_results.append(json.loads(line))
    
    # write facts into a jsonl file
    with open("facts.jsonl", "w+", encoding='utf-8') as facts_file:
        for research_result in research_results:
            #print(research_result)
            for c in research_result["data"]:
                #print(c)
                facts = await extract_main_content(research_result['meta'], research_result['goals'], c["title"], c["content"], 3, 1, client, model)
                print(facts)
                facts_file.write(json.dumps(facts, ensure_ascii=False) + "\n")
async def main():
    await test_outline()
    #await test_scrape_content()
    #await test_extract_facts()
    


asyncio.run(main())