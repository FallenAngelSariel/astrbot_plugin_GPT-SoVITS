from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult, CommandResult, MessageChain
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.all import *

from .GPT_SoVITS import GPTSOVITS_apiv2
import os
import re


@register("TTS", "AstralGuardian", "TTS Through GPT-SoVITS", "1.0.0", "")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.api = GPTSOVITS_apiv2()
        self.api.Open_GPTSOVITS_apiv2()
        self.api.GPTSOVITS_SetModel()
    
    # 注册指令的装饰器。指令名为 。注册成功后，发送 `` 就会触发这个指令，并回复 ``
    @filter.command("hiyaa")
    async def helloworld(self, event:AstrMessageEvent):
        ''' this is a 'hi' command trigger by /hiyaa ''' # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        yield event.plain_result(f"你好呀，旅行者!") # 发送一条纯文本消息
    
    @filter.on_decorating_result()
    async def on_decorating_result(self, event:AstrMessageEvent):
        # get and process bot message
        result = event.get_result()
        self.text = result.get_plain_text()
        cleaned_text = self.remove_complex_emoticons(self.text)

        # tts, send voice
        audio_output_path = self.api.tts(cleaned_text)
        logger.info(audio_output_path)
        voice = MessageChain()
        voice.chain.append(Record(audio_output_path))
        await event.send(voice)
        
    def remove_complex_emoticons(self,text):
        pattern = r"""
                [a-zA-Z]                # 匹配所有英文字母
                |                       # 或
                \([^()]+\)              # 匹配括号内的复杂颜表情
                |                       # 或
                [^\u4e00-\u9fff，。？！、]  # 匹配非中文、非标点符号、非空格的字符
        """
        regex = re.compile(pattern, re.VERBOSE)
        cleaned_text = regex.sub('', text)
        return cleaned_text
    









