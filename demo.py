import datetime
from lunar_python import Lunar, Solar
from openai import OpenAI

# 配置默认的出生时间和性别
default_birth_year = 1994
default_birth_month = 10
default_birth_day = 9
default_birth_hour = 18
default_birth_minute = 0
default_birth_second = 0
default_gender = '男'


# 正确客户端配置
CLIENT_CONFIG = {
    "client_config": {
        "api_key": "your-api_key",
        "base_url": "https://api.siliconflow.cn/v1",
    },
    "request_params": {
        "model": "deepseek-ai/DeepSeek-R1",
        "temperature": 0.3,
        "max_tokens": 2500,
        "stream": True
    }
}

def validate_input_date(year, month, day, hour, minute, second):
    try:
        datetime.datetime(year, month, day, hour, minute, second)
        return True
    except ValueError:
        return False

def create_date_objects(year, month, day, hour, minute, second):
    solar = Solar.fromYmdHms(year, month, day, hour, minute, second)
    lunar = solar.getLunar()
    return solar, lunar

def calculate_age(year):
    """根据虚岁的计算方式，出生时即算1岁"""
    age = year - default_birth_year + 1
    return age

def get_bazi_and_luck_info():
    # 使用默认值创建日期对象
    solar, lunar = create_date_objects(default_birth_year, default_birth_month, default_birth_day,
                                       default_birth_hour, default_birth_minute, default_birth_second)
    
    current_year = datetime.datetime.now().year

    current_age = calculate_age(current_year)

    print(f"阳历时间：{solar.getYear()} 年{solar.getMonth()} 月{solar.getDay()} 日 {solar.getHour()} 时{solar.getMinute()} 分{solar.getSecond()} 秒")
    print(f"阴历时间：{lunar.getYear()} 年{lunar.getMonth()} 月{lunar.getDay()} 日 {lunar.getHour()} 时{lunar.getMinute()} 分 {lunar.getSecond()} 秒")
    print(f"当前年龄：{current_age} 岁")

    print("八字信息：")
    year_ganzhi = lunar.getYearInGanZhiExact()
    month_ganzhi = lunar.getMonthInGanZhiExact()
    day_ganzhi = lunar.getDayInGanZhiExact()
    time_ganzhi = lunar.getEightChar().getTime()
    print(year_ganzhi)  # 年柱
    print(month_ganzhi)  # 月柱
    print(day_ganzhi)  # 日柱
    print(time_ganzhi)  # 时柱

    print("性别:", default_gender)

    # 排大运流年
    gender_num = 1 if default_gender == '男' else 0
    yun = lunar.getEightChar().getYun(gender_num)
   
    start_solar = yun.getStartSolar()
    start_year = start_solar.getYear()
    start_age =calculate_age(start_year)
    print(f"起运年份：{start_year} 年, 起运年龄：{start_age}")

    # 起运前只打印流年
    bazi_info = f"八字：{year_ganzhi}{month_ganzhi}{day_ganzhi}{time_ganzhi}\n"
    luck_info_0 = ""
    if default_birth_year < start_year:
        for year in range(default_birth_year, start_year):
            current_lunar = Solar.fromYmdHms(year, 1, 1, default_birth_hour, default_birth_minute, default_birth_second).getLunar()
            luck_info_0 += f"{year}年 , {calculate_age(year)}岁: {current_lunar.getYearInGanZhiExact()}\n"
            print(f"流年: {current_lunar.getYearInGanZhiExact()} ({year}) ({calculate_age(year)}岁)")

    dayun_list = yun.getDaYun()
    n = 0
    luck_info = []
    for i, dy in enumerate(dayun_list):
        if dy.getGanZhi():
            start = start_year + n * 10
            end = start + 9
            luck_ = {"大运": dy.getGanZhi(), "此大运时间范围": ({start},{end}), "此大运下流年流年": []}
            print(f"大运: {dy.getGanZhi()}({start} - {end})")
            liunian_list = dy.getLiuNian()
            current_year = start
            for liunian in liunian_list:
                luck_["此大运下流年流年"].append({"年份": current_year, "流年": liunian.getGanZhi(),"年龄": calculate_age(current_year)})
                current_year += 1
            n += 1

    return luck_info_0, bazi_info, luck_info,start_year

def get_bazi_analysis():
    """获取专业八字分析"""
    luck_info_0, bazi_info, luck_info,start_year = get_bazi_and_luck_info()

    # 专业提示词模板
    BAZI_PROMPT = f"""
## 命理师资质要求
- 须通晓《渊海子平》《三命通会》《滴天髓阐微》《子平真诠》精髓
- 融合子平法/盲派/新派技法，结合纳音五行论命
- 精通干支作用关系（刑冲破害合会）

## 分析规范
### 基础参数
出生时间：{default_birth_year}-{default_birth_month}-{default_birth_day} {default_birth_hour}:{default_birth_minute} (阳历)
性别：{default_gender}

### 四柱八字及大运流年信息如下
排盘：{bazi_info}
起运年份为：{start_year}
起运前流年信息:{luck_info_0}
起运后的大运流年信息：{luck_info}

注意：
- 八字信息是根据出生时间计算的，起运前流年信息是根据出生时间和起运年份计算的，起运后的大运流年信息是根据起运年份和大运时间范围计算的。
- 起运之前的流年不一定存在也不一定等于10年,起运之后每个大运10年。

### 核心分析模块
定调：对命局有一个简单的论断，确定大的方向。
过三关：包括父母关、兄弟关、婚姻关。
解析大运流年：详细分析大运流年，预测人生重大事项。
你可以综合《渊海子平》《三命通会》《滴天髓阐微》《子平真诠》等书籍的内容，结合命主的信息给出关键的解析，盲派算命也有许多经典口诀，用于推断命主的命运，你也可以使用恰当的口诀来帮助命主理解命局。。
    """

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
