import botpy
import os

from loguru import logger
from crawler import Crawler
from bot import SHUBot
from botpy.ext.cog_yaml import read

def main():
    logger.add("announcements.log")
    config = read(os.path.join(os.path.dirname(__file__), "configs\\info.yaml"))
    
    crawler = Crawler(db_path="announcements.sqlite")
    intents = botpy.Intents(public_guild_messages=True)
    client = SHUBot(intents=intents, crawler=crawler)
    
    client.run(appid=config["appid"], secret=config["secret"])
    
if __name__ == "__main__":
    main()