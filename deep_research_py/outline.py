from datetime import datetime
from typing import List
from unittest.mock import Base
import openai
import json
from .prompt import system_prompt
from .ai.providers import get_client_response, trim_prompt
import re
# use meta recognition to complete research outline
from pydantic import BaseModel, Field
# meta system prompt
from .outline_prompt import meta_think_system_prompt, outline_prompt_head, outline_prompt_tail
import os

async def generate_outline(target: str, requests: str, client: openai.OpenAI, model: str) -> str:
    #get nowday 
    nowday = datetime.now().strftime("%Y-%m-%d")
    print(f"nowday is {nowday}")
    print(f"system prompt is {meta_think_system_prompt}")
    print(outline_prompt_head.format(nowday, target, target))
    head = outline_prompt_head.format(nowday, target, target)
    user_prompt = head + outline_prompt_tail
    response = await get_client_response(
        client=client,
        model=model,
        messages=[
            {"role": "system", "content": meta_think_system_prompt},
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )
    
    return response

def extract_queries(content : str):
    #从content中抽取所有的query,这些query包含在<query>和</query>之间,query之间用逗号分隔的
    meta_thinks = re.findall(r"<meta_cognition>(.*?)</meta_cognition>(.*?)<goals>(.*?)</goals>(.*?)<queries>(.*?)</queries>(.*?)<questions>(.*?)</questions>", content, re.DOTALL)
    
    for think in meta_thinks:
        meta = think[0]
        goals = think[2]
        split_queries = re.split(r"[,，]", think[4])
        questions = think[6]
        for query in split_queries:
            yield (meta, goals, query.strip(), questions.strip())
    
class QAPair(BaseModel):
    '''问题和答案,注意是单个问题和答案'''
    question : str
    answer : str
class GFPair(BaseModel):
    '''goal and fact pair'''
    goal: str
    fact: str
    
class Answers(BaseModel):
    '''从文章中获取的问题和答案数组'''
    answers : list[QAPair] = Field(description="QAPair的数组")
class Facts(BaseModel):
    '''从文章中获取的满足目标要求的事实'''
    facts : list[GFPair] = Field(description="GFPair的数组")
    #unknown_facts : str = Field(description="（不为人知或容易被人忽视）且完整的事实")

async def extract_answers(meta : str, questions : str, title : str, content : str, key_cnt : int, rare_cnt: int, client: openai.OpenAI, model: str):
    
    if content is None:
        return {"key_facts": []}
    #
    if len(content) < 50:
        return {"key_facts": []}    
    
    content = content[:int(os.getenv("CONTEXT_SIZE", "128000"))]
    user_prompt = (f"""
你需要从网页内容中抽取关键事实性内容来回答问题：{questions}。

注意抽取的内容需要完整保留原文信息，并且便于他人进行交叉验证，以避免任何主观解读。
注意如果抽取困难，就不要抽取，直接输出空内容。
注意如果无法有效抽取，就不要抽取，直接输出空内容。
注意保证抽取的质量而不是数量。"""
    f"""以下是网页的具体内容：\n\n<html>{content}</html>\n\n""")
    system_prompt = f"""    
"""
    
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
        response_format=Answers.model_json_schema(),
        temperature=0.1
    )
    
    #print(user_prompt)
    #response['questions'] = questions
    return response
async def extract_facts(meta : str, goals : str, title : str, content : str, key_cnt : int, rare_cnt: int, client: openai.OpenAI, model: str):
    
    if content is None:
        return {"key_facts": []}
    #
    if len(content) < 50:
        return {"key_facts": []}    
    
    content = content[:int(os.getenv("CONTEXT_SIZE", "128000"))]
    user_prompt = (f"""
你需要从网页内容中抽取关键事实性内容来完成目标要求：{goals}。

注意抽取的内容需要完整保留原文信息，并且便于他人进行交叉验证，以避免任何主观解读。
注意如果抽取困难，就不要抽取，直接输出空内容。
注意如果无法有效抽取，就不要抽取，直接输出空内容。
注意保证抽取的质量而不是数量。"""
    f"""以下是网页的具体内容：\n\n<html>{content}</html>\n\n""")
    system_prompt = f"""    
"""
    
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
        temperature=0.1
    )
    
    #print(user_prompt)
    #response['questions'] = questions
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