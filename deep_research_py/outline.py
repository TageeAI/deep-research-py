from datetime import datetime
from typing import List
import openai
import json
from .prompt import system_prompt
from .ai.providers import get_client_response
# use meta recognition to complete research outline

# meta system prompt
meta_think_system_prompt = """
元认知通过随时随地监督自己的思考过程，并且使用以下结构，对思考过程进行优化
元认知的结构如下：
    1. 元认知知识: 你对自己和他人在思考、解决问题和学习过程方面的了解。包括陈述性知识，程序性知识、条件性知识。
        1. 是否有足够的、精确的、及时的陈述性知识，如果没有应该怎么获得：关于自己和任务的事实，不包含任务本身的事实
        2. 是否有合适、精准的程序性知识，如果没有应该怎么获得：知道如何执行策略
        3. 是否有合适、足够深度的条件性知识，如果没有应该怎么获得：知道何时及为何使用策略
    2. 元认知调节: 你用来控制思维的活动和策略。包括规划、监控和评估。
        1. 是否进行了规划，规划的宽度和深度是否足够，是否收集到足够的需求并进行了足够深度的理解：在开始任务前制定目标和选择策略。例如，决定在阅读前先浏览标题和问题以了解重点。
        2. 是否在过程中完成了过程本身的监控，是否及时的根据监控结果进行评估改进：如何在任务进行中检查进展和理解程度？例如，边读边问自己“我明白了吗？” 
        3. 是否在每一个小任务完成后，对人物的产出进行了评估，是否将评估结果应用到改进循环中：任务完成后反思结果和策略的有效性。例如，考试后回顾哪些复习方法最有用。
    3. 元认知体验: 学习新知识或尝试解决问题时产生的想法和感受。通过对体验的感知来更好的监控自己的思考过程。以下是其主要类型：
        1. 知道感（Feeling of Knowing, FOK）  
            定义：在回忆信息前，觉得自己知道答案的一种感觉。  
            示例：考试时，看到问题后觉得答案就在嘴边，但尚未完全回忆起来。  
            作用：这种感觉可以指导是否继续努力回忆或转向其他策略。
        2. 舌尖现象（Tip-of-the-Tongue Experience, TOT）  
            定义：知道某事但暂时无法回忆起来的感觉，通常伴随部分相关信息的激活。  
            示例：试图回忆演员的名字，但只记得他们的电影角色。  
            作用：这种体验提示记忆检索的接近性，可能促使个体通过提示或上下文辅助回忆。
        3. 信心判断（Confidence Judgments）  
            定义：对自己答案或决定的确定程度评估。  
            示例：在选择题中，感觉某个选项非常正确，决定不更改。  
            作用：影响决策，如是否坚持答案或重新检查。
        4. 难度评估（Difficulty Assessments）  
            定义：感知任务的难易程度或所需努力。  
            示例：阅读复杂文章时，感觉需要更多时间理解，决定放慢速度。  
            作用：帮助调整策略，如分解任务或寻求帮助。
        5. 情绪反应（Emotional Responses）  
            定义：学习过程中伴随的情绪，如满足、挫折或焦虑。  
            示例：掌握新概念后感到满足，或因反复失败感到挫折。  
            作用：情绪反应可能触发策略调整，如因挫折而选择更简单的学习方法。
        6. 监控理解（Monitoring Comprehension）  
            定义：在阅读或听讲时检查理解程度。  
            示例：边读边问自己“我明白了吗？”发现不理解后重读。  
            作用：实时调整学习过程，确保理解。
        7.自我提问（Self-Questioning）  
            定义：通过提问检查理解或进展。  
            示例：学习后问自己“这个概念的主要点是什么？”以确认掌握。  
            作用：增强主动学习，识别知识缺口。
        8.反思性思考（Reflective Thinking）  
            定义：任务完成后反思学习过程，评估策略效果。  
            示例：考试后思考哪些复习方法有效，决定下次改进。  
            作用：为未来学习提供反馈，优化方法。

反思过程使用元认知结构分析，反思内容采用结构化思维模型
"""

outline_prompt = """
今天是{}，请你根据需求：{}，写出一份{}的投研报告，在书写的思考过程中注意务必使用基于元认知结构进行反思，插入基于元认知结构的反思内容。
在标注时，请使用<meat></meta>来插入您的注释，格式为：<meta>...</meta>。
例如，‘我需要先规划在执行’编辑为‘我需要先规划在执行<meta>元认知式反思：在规划前是否对需求足够了解？</meta>’。
"""

async def generate_outline(target: str, requests: str, client: openai.OpenAI, model: str) -> str:
    #get nowday 
    nowday = datetime.now().strftime("%Y-%m-%d")
    response = await get_client_response(
        client=client,
        model=model,
        messages=[
            {"role": "system", "content": meta_think_system_prompt},
            {
                "role": "user",
                "content": outline_prompt.format(nowday, requests, target),
            },
        ],
        response_format={"type": "str"},
    )
    
    return response
