from datetime import datetime
from cv2 import merge
from flask import request
from ollama import chat, Client
from sqlalchemy import all_
from sympy import Q
from deep_research_py.outline_prompt import meta_think_system_prompt, outline_prompt
from deep_research_py.deep_research import deep_research, search_service
from deep_research_py.outline import extract_answers, extract_facts
from deep_research_py.ai.providers import AIClientFactory
import re
import os
from dotenv import load_dotenv
load_dotenv()

import asyncio

print(os.getenv("OLLAMA_HOST_ENDPOINT"))
print(os.getenv("OLLAMA_NUM_CTX"))
print(os.getenv("OLLAMA_NUM_PREDICT"))

ai_model = "gemma3:27b-it-fp16"
model = os.getenv("OLLAMA_MODEL", "gemma3:27b-it-fp16")

print(f"env model is {model}")
print(f"ai_model is {ai_model}")
client = Client(os.getenv("OLLAMA_HOST_ENDPOINT"))
ai_client = AIClientFactory.get_client()
nowday = datetime.now().strftime("%Y-%m-%d")
requests = "恐慌情绪对股价的影响"
target = "TSLA"

def search_query_tool(query:str) -> str:
  """
    use input query to call google search engine to get search results
  """
  return "google"


stream = client.chat(
    model=ai_model,
    messages=[
        {"role": "system", "content": meta_think_system_prompt},
            {
                "role": "user",
                "content": outline_prompt.format(nowday, requests, target, target),
            },],
    stream=True,
    #tools=[search_query_tool]
)

stream = [{"message":{"content":"""## 特斯拉 (TSLA) 恐慌情绪对股价影响研究分析报告 (2025-03-17)

**免责声明：** 本报告仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。

**摘要：** 本报告旨在分析当前市场环境下，恐慌情绪对特斯拉(TSLA)股价的影响。我们将评估近期影响TSLA股价的负面因素，分析恐慌情绪的蔓延程度，并结合技术分析和基本面分析，预测TSLA未来一个月的股价目标价。

**1. 引言**

当前全球经济形势复杂，地缘政治风险加剧，市场波动性上升。特斯拉作为一家高成长性、高估值公司，其股价对市场情绪尤为敏感。近期，关于特斯拉需求放缓、竞争加剧、以及马斯克个人风险等负面消息不断涌现，导致市场恐慌情绪蔓延，TSLA股价承压。本报告将深入分析这些因素，评估恐慌情绪对TSLA股价的具体影响。

<meta_cognition> 意识到当前任务是撰写一份投资分析报告，需要结合宏观经济、行业趋势、公司基本面和技术分析，并预测股价。需要保持客观中立，避免主观臆断。初步判断需要收集的数据 包括：宏观经济数据、行业报告、特斯拉财务报表、新闻报道、社交媒体情绪分析等。</meta_cognition>
<step> 收集并整理相关数据，包括宏观经济数据、行业报告、特斯拉财务报表、新闻报道、社交媒体情绪分析等。</step>
<goals> 收集2024年Q4和2025年Q1的宏观经济数据，特斯拉财务报表，至少50篇关于特斯拉的新闻报道，社交媒体情绪分析报告。</goals>
<queries> 全球经济展望2025, 特斯拉财务报表, 特斯拉新闻, 特斯拉社交媒体情绪分析, 电动汽车行业报告2025</queries>
<questions> (1) 当前全球经济形势对电动汽车行业的影响？ (2) 特斯拉的竞争对手在技术和市场份额方面有哪些优势？ (3) 社交媒体情绪分析如何准确反映市场对特斯拉的看法？</questions>"""}}]

content = """东南亚电动汽车市场正迎来快速增长期。图为老挝首都万象的一家电动汽车4S店前，一辆中国品牌电动出租车在充电。本报记者 杨 一摄

　　德国巴登—符滕堡州太阳能和氢能研究中心近日发布的一份报告显示，2023年，全球电动汽车（包括纯电动汽车、插电式混合动力汽车和增程式电动汽车）保有量达到近4200万辆，比上一年增长约50%。其中，中国电动汽车保有量约为2340万辆，占全球一半以上。据德国Statista数据平台统计，2024年，全球电动汽车市场营收有望达到7862亿美元，并将在2024—2029年间保持稳定的年复合增长率6.63%。业内人士认为，当前全球环保低碳理念越发深入人心，电动汽车领域技术快速迭代创新，预计2024年全年全球电动汽车销售将继续保持强劲增长势头。

　　整体销售数据增量可观

　　根据这份最新报告，2023年全球共注册1480万辆电动汽车。其中，中国以超过900万辆电动汽车的注册量明显领先。欧盟以250万辆新注册电动汽车成为全球第二大市场，美国以150万辆电动汽车位居第三。

　　市场研究公司ABI Research报告表明，从2019年到2023年，全球电动汽车销量增长了506%。据国际能源署此前发布的《2024年全球电动汽车展望》报告，2024年全球电动汽车销量预计达1700万辆，占全球汽车总销量的1/5以上。2024年，中国电动汽车销量将增至1000万辆左右，约占中国国内汽车销量的45%；在欧洲和美国，电动汽车销量占比预计分别约为1/4和1/9。

　　2024年麦肯锡针对欧洲消费者的一项调查显示，在尚未购买电动汽车的购车者中，38%的人表示他们的下一辆汽车将是电动汽车。彭博社的市场分析报告认为，新兴市场的电动汽车需求正在加速增长，将成为2024年电动汽车销售的重要市场，泰国、印度尼西亚等国的商用电动汽车全年销量可能出现激增。

　　标普全球公司发布的报告认为，全球汽车行业正加速电动化转型。未来电动汽车销售增量可观，市场前景广阔。到2030年，新售出的乘用车中电动汽车占比将超过1/4。

　　产业发展拥有广阔前景

　　世界经济论坛的一篇文章表示，随着电池续航、汽车成本、充电基础设施等问题不断优化解决，全球电动汽车的市场需求有望进一步迸发。在各国激励措施出台、产业技术迭代创新、充电基础设施发展、消费者偏好改变等多重利好因素推动下，全球电动汽车市场正加速扩大。

　　国际能源署的一份报告认为，随着市场竞争和规模化生产促成电动汽车价格逐步下降，电动汽车需求预计会呈现指数级增长。电动汽车是各国正大力推广的一项重要减排措施。电池技术、充电技术的不断更新，电动汽车与人工智能、互联网、大数据等多种变革性技术的融合，将持续开拓新的市场空间。

　　《2024年全球电动汽车展望》显示，确保公共充电设施的可用性与电动汽车的销售保持同步，对于稳步扩大电动汽车市场至关重要。与2022年相比，2023年全球安装的公共充电桩数量增长了40%，快速充电桩的增长速度更快。为了实现各国政府承诺的电动汽车部署目标，预计到2035年充电网络还需要增长6倍。

　　国际能源署预计，未来10年全球电动汽车需求将持续强劲增长。电动汽车需求激增将重塑全球汽车业，并显著降低道路交通领域的石油消耗量。相关研究显示，汽车产业连接上下游众多产业链条，在绿色转型、低碳发展中发挥着难以替代的重要作用。2023年，电动汽车的使用为全球减少了超过2.2亿吨的温室气体排放，而2022年这一数字为8000万吨。

　　中国制造助力绿色转型

　　世界经济论坛的一篇文章表示，随着智能电动汽车时代的到来，消费者观念改变和新技术进步，全球汽车市场正在经历重要转变，其中中国汽车产业在电动化转型进程中表现突出。未来，中国在电动汽车领域将继续保持快速增长势头。

　　中国汽车工业协会的统计数据显示，2023年，中国新能源汽车产销保持快速增长，分别为958.7万辆和949.5万辆，同比分别增长35.8%和37.9%。目前，中国汽车制造商的电动汽车产量占全球电动汽车产量的一半以上。

　　据德国《商报》报道，电池和充电技术已成为全球电动汽车领域的研发重点，而中国在其中占据重要地位。中国拥有大量充电技术专利，在专利申请方面的“数量和专有技术令人印象深刻”。中国汽车制造商、供应商、大学和初创企业组成的密集网络在充电技术专利领域占据领先地位。这促使德国制造商持续在中国开展合作。宝马、奥迪、大众等车企正通过寻找中国供应商、与中国电动汽车公司成立合资企业、共同研发新型电动汽车等方式开展合作。

　　根据国际能源署测算，为实现碳中和目标，2030年全球新能源汽车销量需要达到约4500万辆，是2023年的3倍多。当前产能远不能满足全球市场需求。泰国电动汽车协会副会长素罗·桑尼表示，全球发展新能源产业是大势所趋。中国作为全球电动汽车领域的领先者，在应对全球气候变暖方面作出了重要贡献。“在经济全球化背景下，加强与中国在电动汽车领域的合作，可以让世界各国尤其是发展中国家从发展新能源产业中受益。”素罗说。"""
async def test_outline():
    merged_chunk = ""
    all_content = ""
    for chunk in stream:
        #print(chunk['message']['content'], end='', flush=True)
        merged_chunk = merged_chunk + chunk['message']['content']
        #print(merged_chunk, end='', flush=True)
        all_content = all_content + chunk['message']['content']
        #使用正则表达式,从merged_chunk中读取<queries>...</queries>的内容
        
        meta_thinks = re.findall(r"<meta_cognition>(.*?)</meta_cognition>(.*?)<goals>(.*?)</goals>(.*?)<queries>(.*?)</queries>(.*?)<questions>(.*?)</questions>", merged_chunk, flags=re.DOTALL)

        if len(meta_thinks) > 0:
            client._client.close()
            #break
            for think in meta_thinks:
                meta = think[0]
                goals = think[2]
                split_queries = re.split(r"[,，]", think[4])
                quesitons = think[6]
                
                for query in split_queries:
                    research_result = await search_service.search(query, max_concurrent_scrapes=5)
                    #print(data)
                    #research_result = {}
                    #research_result["data"] = [{"title":"查理·芒格的100个思维模型", "content":content}]
                    for c in research_result["data"]:
                        print(f"extract query:{query} facts from {c["content"]}")
                        answers = await extract_answers(meta, quesitons, c["title"], c["content"], 1, 1, ai_client, ai_model)
                        print(answers)
                        facts = await extract_facts(meta, goals, c["title"], c["content"], 1, 1, ai_client, ai_model)
                        print(facts)
                        
    return all_content
async def main():
    rt = await test_outline()
    #print(rt)
    #await test_scrape_content()
    #await test_extract_facts()
    


asyncio.run(main())