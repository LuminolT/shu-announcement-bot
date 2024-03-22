import unittest
from crawler import Crawler

from loguru import logger
logger.add("logs.log")

class TestCrawler(unittest.TestCase):
    def test_update_database(self):
        crawler = Crawler(db_path="test.sqlite")
        crawler.update_database()
        print(crawler.get_latest_announcements())
        print(crawler.get_latest_announcements(5))