import settings
import time

from ahref_spider.core import ASpider
from ahref_spider.utils import smart_run


if __name__ == '__main__':
    session = ASpider(settings.USERNAME, settings.PASSWORD, headless_browser=settings.BROWSER_IN_BACKGROUND, save_data_limit=500)
    with smart_run(session):
        session.search_backlinks(
                settings.INPUT_FILE_NAME,
                settings.OUTPUT_1_FILE_NAME,
                settings.SEARCH_BACKLINK_PROTOCOL,
                settings.SEARCH_BACKLINK_INDEX_MODE,
            )