import unittest
from crawler import SHUCrawler

from loguru import logger
logger.add("logs.log")

class TestSHUCrawler(unittest.TestCase):
    def test_update_database(self):
        crawler = SHUCrawler(db_path="test.sqlite")
        crawler.update_database()
        print(crawler.get_latest_announcements())
        print(crawler.get_latest_announcements(5))