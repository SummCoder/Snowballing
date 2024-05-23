# 基于glm4进行需要滚雪球文章的分类

from zhipuai import ZhipuAI

client = ZhipuAI(api_key="")


def glm_analyse(content):
    tools = [{
        "type": "web_search",
        "web_search": {
            "enable": False,
            "search_result": False,  # 禁用False，启用：True，默认为禁用
        }
    }]
    messages = [
        {
            "role": "system",
            "content": "你是一个乐于助人的论文阅读专家，热心解答用户提供的相关论文的分析"
        },
        {
            "role": "user",
            "content": """根据以下论文的摘要内容""" + content + """。\n"
                       + "你应该按照下列方式进行思考：\n"
                         "1.总结该篇文章内容\n"
                         "2.然后判断是否是关于代码模型任务而非其他领域例如nlp领域，注意与自然语言处理相区分，要实际涉及到代码相关任务\n"
                         "3.接着分析是否涉及针对代码任务模型安全领域如攻击和防御\n"
                         "4.最后给出一个**综合分类**，第二点和第三点都是的话，输出1，否则0，注意最后只有一位数字0或者1"
                         """
        }]

    response = client.chat.completions.create(
        model="glm-4",
        messages=messages,
        tools=tools
    )
    return response

