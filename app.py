from openai import OpenAI

# 用户信息配置
USER_INFO = {
    "birth_time": "1993-12-09 18:00",
    "gender": "男",
    "birthplace": "吉林省长春市榆树市",
    "coordinates": (126.55, 44.83),
    "calendar_type": "阳历"
}

# 专业提示词模板
BAZI_PROMPT = f"""
## 命理师资质要求
- 须通晓《渊海子平》《三命通会》《滴天髓阐微》《子平真诠》精髓
- 融合子平法/盲派/新派技法，结合纳音五行论命
- 熟练运用五虎遁、五鼠遁、夹拱暗带技法
- 精通干支作用关系（刑冲破害合会）

## 分析规范
### 基础参数
出生时间：{USER_INFO['birth_time']} ({USER_INFO['calendar_type']})
性别：{USER_INFO['gender']}
出生地：{USER_INFO['birthplace']}（经度{USER_INFO['coordinates'][0]}，纬度{USER_INFO['coordinates'][1]}）
排盘要求：包含节气交节时间、真太阳时校正

### 八字的计算方法
参考问真八字的排盘规则排八字，大运和流年的排算规范也要符合问真八字的规则，要检查出生时间以及现在的时间，确保年龄的准确性，确保大运流年与年龄对应关系是正确的，起运时的年龄不要算错。

### 核心分析模块
排盘：根据命主的出生信息排出命盘。
定调：对命局有一个简单的论断，确定大的方向。
过三关：包括父母关、兄弟关、婚姻关。
解析大运流年：详细分析大运流年，预测人生重大事项。
盲派算命有许多经典口诀，用于推断命主的命运，可以使用恰当的口诀来帮助命主理解命局。
也要综合《渊海子平》《三命通会》《滴天髓阐微》《子平真诠》等书籍的内容，结合命主的信息给出关键的解析。

"""

# 正确客户端配置
CLIENT_CONFIG = {
    "client_config": {
        "api_key": "your-key", # https://cloud.siliconflow.cn/account/ak
        "base_url": "https://api.siliconflow.cn/v1",
    },
    "request_params": {
        "model": "deepseek-ai/DeepSeek-R1",
        "temperature": 0.3,
        "max_tokens": 2500,
        "stream": True
    }
}

def get_bazi_analysis():
    """获取专业八字分析"""
    # 正确初始化客户端
    client = OpenAI(**CLIENT_CONFIG["client_config"])
    
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": BAZI_PROMPT}],
            **CLIENT_CONFIG["request_params"]  # 正确传递请求参数
        )
        
        # 流式输出处理
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                print(content, end='', flush=True)
                
    except Exception as e:
        print(f"请求异常：{str(e)}")

if __name__ == "__main__":
    get_bazi_analysis()
