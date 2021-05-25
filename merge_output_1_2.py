import settings

from ahref_spider.core import ASpider

if __name__ == '__main__':
    session = ASpider(settings.USERNAME, settings.PASSWORD, headless_browser=settings.BROWSER_IN_BACKGROUND)
    session.merge_data(settings.OUTPUT_1_FILE_NAME, settings.OUTPUT_2_FILE_NAME, settings.OUTPUT_3_FILE_NAME)