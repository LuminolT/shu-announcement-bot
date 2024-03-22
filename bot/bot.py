import os
import botpy
import asyncio

from botpy import BotAPI
from botpy.ext.command_util import Commands
from botpy.message import Message
from botpy.ext.cog_yaml import read

from loguru import logger

from crawler import Crawler

is_fetching_enabled = False
is_first_run = True
latest_announcements = None

@Commands("start")
async def start(api: BotAPI, message: Message, **kwargs):
    global is_fetching_enabled
    if not is_fetching_enabled:
        is_fetching_enabled = True
        await message.reply(content="网页信息获取已启动。")
        asyncio.create_task(fetch_and_send(api, message, crawler=kwargs.get("crawler")))
    else:
        await message.reply(content="网页信息获取已经在运行中。")

@Commands("stop")
async def stop(api: BotAPI, message: Message, **kwargs):
    global is_fetching_enabled
    if is_fetching_enabled:
        is_fetching_enabled = False
        await message.reply(content="网页信息获取已停止。")
    else:
        await message.reply(content="网页信息获取未启动。")
        
async def fetch_and_send(api: BotAPI, message: Message, crawler: Crawler):
    
    while is_fetching_enabled:
        crawler.update_database()
        global is_first_run
        if is_first_run:
            is_first_run = False
            announcements = crawler.get_latest_announcements(5)[::-1]
            latest_announcements = announcements[0]
            await message.reply(content="首次运行，获取最近5条通知：")
            for announcement in announcements:
                content = f"（{announcement.date}）{announcement.title}"
                await message.reply(content=content)
        else:
            announcement = crawler.get_latest_announcements(1)[0]
            if announcement.title != latest_announcements.title:
                latest_announcements = announcement
                content = f"【新通知】（{announcement.date}）{announcement.title}"
                await message.reply(content=content)
            
        
        await asyncio.sleep(3600)

        
class SHUBot(botpy.Client):
    
    def __init__(self, crawler: Crawler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crawler = crawler
        
    async def on_at_message_create(self, message: Message):
        # 注册指令handler
        handlers = [
            start,
            stop,
        ]
        for handler in handlers:
            if await handler(api=self.api,
                                message=message,
                                crawler=self.crawler):
                return
