from .ai.providers import get_client_response_2
from datetime import datetime
import openai
from typing import List, Dict, TypedDict, Optional
from pydantic import BaseModel
import json
import ollama
import re

convert_system_prompt = """"""

convert_prompt ="""
今天是{}。请从以下反思的内容中把需要去求证或获取的信息提炼出来，并转换成一组适合google搜索引擎的搜索关键词，为了进一步查询备用：
{}
"""

class SerpQuery(BaseModel):
    query: str
    research_goal: str

class Queries(BaseModel):
    queries: List[SerpQuery]
    

#从<meta>...<queries>...</queries> <goal></goal></meta>中分别提取<meta>...</meta> 的内容、<queries>...</queries>的内容, <goal>...</goal>的内容
def extract_meta_thinks(outline: str) -> dict:
    # 匹配包含三个分组的正则表达式
    pattern = r'<meta>(.*?)<queries>(.*?)</queries>.*?<goals>(.*?)</goals>.*?</meta>'
    matches = re.findall(pattern, outline, flags=re.DOTALL)
    
    meta = []
    for m in matches:
        queries = m[1].strip().split(", ")
        goals = m[2].strip().split(", ")
        meta.append({
            "meta_thinks": m[0].strip(),
            "queries": queries,
            "goals": goals
        })

    # 结构化成字典返回
    return meta
    