import requests
import sqlite3
import time
import pathlib

from bs4 import BeautifulSoup
from loguru import logger
from collections import namedtuple
from typing import List

Announcement = namedtuple("Announcement", ["title", "date", "link"])

class Crawler():

    def __init__(self, db_path: pathlib.Path) -> None:
        self.url        = "https://jwb.shu.edu.cn/index/tzgg.htm"
        self.db_path    = db_path
        self.conn       = sqlite3.connect(self.db_path)
        self.c          = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS announcements (
                            id      INTEGER PRIMARY KEY AUTOINCREMENT, 
                            title   TEXT, 
                            date    DATE,
                            link    TEXT)''')
        self.conn.commit()
    
    def __del__(self) -> None:
        self.conn.close()
        
    def update_database(self) -> None:
        """update the database with the latest announcements from the website
        """
        response = requests.get(self.url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        only_list_div = soup.find('div', class_='only-list')
        
        if not only_list_div:
            logger.error("未找到通知列表的 div")
            return
        
        announcements = only_list_div.find_all('li')
        for announcement in announcements:
            title = announcement.a.get_text(strip=True)
            date = announcement.span.get_text(strip=True)
            date = date.replace("年", "-").replace("月", "-").replace("日", "")
            link = announcement.a['href']
            link = "https://jwb.shu.edu.cn" + link.lstrip("..")
            
            self.c.execute("SELECT * FROM announcements WHERE title = ?", (title,))
            existing_announcement = self.c.fetchone()
            
            if not existing_announcement:
                self.c.execute("INSERT INTO announcements (title, date, link) VALUES (?, ?, ?)", (title, date, link))
                logger.info(f"发现新通知 '{title}'，已插入数据库")
            
        self.conn.commit()
        
    def get_latest_announcements(self, limit: int=1) -> List[Announcement]:
        """get the latest announcements from the database

        Args:
            limit (int, optional): the number of announcements to get. Defaults to 1.

        Returns:
            List[Announcement]: a list of Announcement objects
        """
        self.c.execute("SELECT * FROM announcements ORDER BY date DESC LIMIT ?", (limit,))
        announcements = self.c.fetchall()
        return [Announcement(*announcement[1:]) for announcement in announcements]