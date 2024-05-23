import requests
import pandas as pd
from utils.glm4 import glm_analyse
from utils.bs import spider
import re

df = pd.DataFrame(columns=["Type", "Title", "Description", "Classification"])

# 修改为相应论文的id
semantic_scholar_id = "efd9d88c9fff716340e6122d95db6d5219871331"

# 构造请求的URL
url = f"https://api.semanticscholar.org/v1/paper/{semantic_scholar_id}"

# 发起请求
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    data = response.json()
    print(data)
    print("Title======================================")
    print(data["title"])
    print("\n\n")
    references_data = [{"Type": "Title", "Title": data.get('title', 'No title available'), "Description": "initial",
                        "Classification": 1}]
    df = pd.concat([df, pd.DataFrame(references_data)], ignore_index=True)

    # 检查是否有引用文献
    if "references" in data and len(data["references"]) > 0:
        # 打印引用文献的信息，例如标题、作者、时间和Semantic Scholar-ID
        print("References=================================")
        for reference in data["references"]:
            # print(f"Title: {reference.get('title', 'No title available')}")
            print(f"{reference.get('title', 'No title available')}")
            url0 = reference.get('url').split("paper/")[-1]
            url1 = f"https://api.semanticscholar.org/v1/paper/{url0}"

            response0 = requests.get(url1)
            if response0.status_code == 200:
                response0 = response0.json()["abstract"]
                if response0 is None:
                    response0 = spider(reference.get('url'))
            else:
                response0 = None
            if response0 is not None:
                result = glm_analyse(response0)
                # 构建字典存储结果数据
                response_data = result.choices[0].message.content
                score = re.findall(r'\d+', response_data)[-1]
            else:
                response_data = "No abstract data available"
                # 存疑
                score = 1
            references_data = [{"Type": "Reference", "Title": reference.get('title', 'No title available'),
                                "Description": response_data, "Classification": score}]
            df = pd.concat([df, pd.DataFrame(references_data)], ignore_index=True)
    else:
        print("暂没有 References")
    print("\n\n")
    if "citations" in data and len(data["citations"]) > 0:
        print("Citations=================================")
        for citation in data["citations"]:
            # print(f"Title: {reference.get('title', 'No title available')}")
            print(f"{citation.get('title', 'No title available')}")
            url0 = citation.get('url').split("paper/")[-1]
            url1 = f"https://api.semanticscholar.org/v1/paper/{url0}"
            response0 = requests.get(url1)
            if response0.status_code == 200:
                response0 = response0.json()["abstract"]
                if response0 is None:
                    response0 = spider(citation.get('url'))
            else:
                response0 = None
            if response0 is not None:
                result = glm_analyse(response0)
                # 构建字典存储结果数据
                response_data = result.choices[0].message.content
                score = re.findall(r'\d+', response_data)[-1]
            else:
                response_data = "No abstract data available"
                score = 1
            citations_data = [{"Type": "Citation", "Title": citation.get('title', 'No title available'),
                               "Description": response_data, "Classification": score}]
            df = pd.concat([df, pd.DataFrame(citations_data)], ignore_index=True)
    else:
        print("暂没有 Citations")

    print("\n\n")
    # 将DataFrame写入CSV文件
    df.to_csv("result3.csv", index=False)

    print("数据已成功写入到result3.csv文件中。")
else:
    print(f"请求失败，状态码：{response.status_code}")
