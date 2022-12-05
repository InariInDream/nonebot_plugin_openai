import openai
from nonebot import logger
from nonebot.params import CommandArg

from nonebot import on_startswith, on_command, require, get_driver
from nonebot.adapters.onebot.v11 import (
    GROUP,
    GroupMessageEvent,
    MessageSegment,
    Message
)

# 设置访问密钥
try:
    openai.api_key = get_driver().config.API_KEY
except:
    openai.api_key = ""

chat = on_command("/chat",  priority=5, block=False)


@chat.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    if not openai.api_key:
        await chat.finish("请先设置API_KEY")

    args = arg.extract_plain_text().strip()
    if args == "":
        await chat.finish("请输入要聊天的内容")

    # 设置请求数据
    data = {
        "prompt": f"{args}",
        "model": "text-davinci-002",
        "max_tokens": 512,
        "temperature": 0.5,

    }

    # 调用OpenAI API，获取答案
    response = openai.Completion.create(engine=data["model"], prompt=data["prompt"], max_tokens=data["max_tokens"], n=1, temperature=data["temperature"])

    # 打印返回的结果
    print(response["choices"][0]["text"])