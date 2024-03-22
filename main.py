import botpy
import os

from loguru import logger
from crawler import SHUCrawler
from bot import SHUBot
from botpy.ext.cog_yaml import read

def main():
    logger.add("announcements.log")
    
    config = {
        "appid":    os.environ.get("SHU_BOT_APPID"),
        "secret":   os.environ.get("SHU_BOT_SECRET")
    }
    
    crawler = SHUCrawler(db_path="announcements.sqlite")
    intents = botpy.Intents(public_guild_messages=True)
    client = SHUBot(intents=intents, crawler=crawler)
    
    client.run(appid=config["appid"], secret=config["secret"])
    
if __name__ == "__main__":
    main()