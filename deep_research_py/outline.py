from datetime import datetime
from typing import List
import openai
import json
from .prompt import system_prompt
from .ai.providers import get_client_response, trim_prompt
import re
# use meta recognition to complete research outline
from pydantic import BaseModel, Field
# meta system prompt
from .outline_prompt import meta_think_system_prompt, outline_prompt
import os

async def generate_outline(target: str, requests: str, client: openai.OpenAI, model: str) -> str:
    #get nowday 
    nowday = datetime.now().strftime("%Y-%m-%d")
    print(f"nowday is {nowday}")
    print(f"system prompt is {meta_think_system_prompt}")
    print(outline_prompt.format(nowday, requests, target, target))
    response = await get_client_response(
        client=client,
        model=model,
        messages=[
            {"role": "system", "content": meta_think_system_prompt},
            {
                "role": "user",
                "content": outline_prompt.format(nowday, requests, target, target),
            },
        ],
    )
    
    return response

def extract_queries(content : str):
    #从content中抽取所有的query,这些query包含在<query>和</query>之间,query之间用逗号分隔的
    meta_thinks = re.findall(r"<meta>(.*?)</meta>(.*?)<goals>(.*?)</goals>(.*?)<queries>(.*?)</queries>", content, re.DOTALL)
    
    for think in meta_thinks:
        meta = think[0]
        goals = think[2]
        split_queries = re.split(r"[,，]", think[4])
        for query in split_queries:
            yield (meta, goals, query.strip())
    

class Facts(BaseModel):
    '''从文章中抽取的关键事实'''
    key_facts : list[str] = Field(description="关键且完整的事实")
    #unknown_facts : str = Field(description="（不为人知或容易被人忽视）且完整的事实")

async def extract_facts(meta : str, goals : str, title : str, content : str, key_cnt : int, rare_cnt: int, client: openai.OpenAI, model: str):
    
    if content is None:
        return {"key_facts": []}
    #
    if len(content) < 50:
        return {"key_facts": []}    
    
    content = content[:int(os.getenv("CONTEXT_SIZE", "128000"))]
    user_prompt = (f"""
注意：你在进行任何动作前先进行思考，思考的内容嵌入到<think></think>标签内。
注意：根据元认知（{meta}）的内容对思考过程和抽取行为进行监督。
你的目标是（{goals}），下面网页内容包含的文章的标题是《{title}》，为了达成你的目标，你需要从文章内容中抽取关键事实性内容作为你的备忘。
注意抽取的内容要和目标相关，并且能够便于他人进行交叉验证
注意抽取的内容需要完整保留原文信息，并且便于验证，以避免任何主观解读。
注意如果抽取困难，就不要抽取，直接输出空内容。
注意如果无法有效抽取，就不要抽取，直接输出空内容。
注意保证抽取的质量而不是数量。"""
    f"""以下是网页的具体内容：\n\n<html>{content}</html>\n\n""")
    system_prompt = f"""    
元认知监督认知的方法论：

1. 明确元认知的层次
元认知监督认知可以分为三个层次，每个层次都有其独特的作用：

知识层面
了解自己的认知策略、能力以及局限性。例如，你需要认识到自己在哪些情况下容易分心，或者在解决问题时倾向于依赖直觉而非逻辑分析。这种自我认知是元认知的基础。

监控层面
在认知活动进行时，实时监督自己的表现和理解程度。例如，在学习新知识时，可以定期停下来问自己：“我是否真正理解了这个概念？”、“我的注意力是否集中？”通过这种方式，你可以及时发现问题。

调节层面
根据监控的结果，调整自己的认知策略。例如，如果发现自己对某部分内容理解不深，可以放慢速度、查阅更多资料，或尝试不同的学习方法（如画图理解而非单纯阅读）。

2. 实践方法
以下是一些具体可行的实践方法，帮助你在日常生活中实现元认知监督认知：

自我提问
在学习或思考时，定期提出关键问题，例如：  
“我学到了什么？”  

“我还有哪些不明白的地方？”  

“我该如何改进我的方法？”
这种习惯可以增强对自身认知过程的觉察。

反思性日记
每天或每周花几分钟记录自己的学习过程、决策和结果。分析哪些方法有效、哪些失败，并总结经验教训。例如，你可以写下：“今天我在学习数学时分心了，下次可以尝试关闭手机通知。”

目标设定与评估
为每项认知任务设定具体、可衡量的目标，例如“理解这篇文章的主旨”或“完成10道练习题”。任务结束后，评估目标达成情况，找出需要改进的地方。

思维可视化
使用思维导图、流程图等工具，将复杂的思维过程整理成清晰的结构。这不仅有助于监督自己的思路，还能发现逻辑上的漏洞或遗漏。

模拟教学
尝试向他人（甚至是自己）解释所学内容。例如，把一个新概念用自己的话讲出来。这种方法能帮助你检测理解的深度，并暴露知识盲点。

3. 优化策略
为了让元认知监督认知更高效，可以采用以下策略：
主动调节
当发现认知偏差或错误时，立即调整方法。例如，如果你在阅读时感到疲倦，可以换个环境、休息一下，或尝试通过讨论来激活思维。

反馈循环
除了自我监控，还可以寻求外部反馈，例如向同伴、导师请教。他们可能会指出你未察觉的问题。将外部反馈与自我评估结合，形成一个持续改进的闭环。

元认知训练
通过冥想或正念练习，提升对当下思维的觉察能力。例如，每天花10分钟专注于呼吸，观察自己的念头而不加评判，这种练习能增强自我监控的敏感性。

4. 注意事项
在实施元认知监督认知时，需要注意以下几点，以确保其效果：
避免过度反思
元认知的目的是优化认知任务，而非成为负担。如果过度纠结于自我分析，可能会降低效率。因此，要保持适度，避免陷入无休止的自我怀疑。

适应性
根据任务的复杂性和个人状态，灵活调整元认知的强度。例如，简单任务可能只需偶尔监控，而复杂任务则需要更频繁的反思和调节。

注意使用中文进行思考和输出"""

    #print(user_prompt)
    response = await get_client_response(
        client=client,
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},

            {
                "role": "user",
                "content":user_prompt,
            },
        ],
        response_format=Facts.model_json_schema(),
        temperature=0.9
    )
    
    #print(user_prompt)
    response['goals'] = goals
    return response

class MainContent(BaseModel):
    main_content : str = Field(description="主要内容")
async def extract_main_content(meta : str, goals : str, title : str, content : str, key_cnt : int, rare_cnt: int, client: openai.OpenAI, model: str):
    if content is None:
        return {"main_content": []}
    #
    if len(content) < 50:
        return {"main_content": []}    
    
    content = content[:int(os.getenv("CONTEXT_SIZE", "128000"))]
    user_prompt = (f"""网页的标题是《{title}》从网页内容从抽取出完整的文章内容，注意不要修改文章的内容"""
                   """\n注意使用中文输出。\n"""
    f"""以下是爬取的网页内容：\n\n<page>{content}</page>\n\n""")
    system_prompt = ""#f"""来源与对网页的爬取，因此包含了和标题无关的内容。注意忽视这些和标题无关的内容。"""

    
    #user_prompt = trim_prompt(user_prompt)
    print(user_prompt)
    
    response = await get_client_response(
        client=client,
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},

            {
                "role": "user",
                "content":user_prompt,
            },
        ],
        response_format=MainContent.model_json_schema(),
        temperature=0
    )
    
    #print(user_prompt)
    #response['content'] = content
    return response