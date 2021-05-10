import settings
import time

from ahref_spider.core import ASpider
from ahref_spider.utils import smart_run


if __name__ == '__main__':
    session = ASpider(settings.USERNAME, settings.PASSWORD, headless_browser=settings.BROWSER_IN_BACKGROUND)
    with smart_run(session):
        batch_analysis = session.batch_analysis(
                settings.INPUT_FILE_NAME,
                settings.OUTPUT_2_FILE_NAME,
                settings.SEARCH_BACKLINK_PROTOCOL,
                settings.SEARCH_BACKLINK_INDEX_MODE,
            )
        if batch_analysis:
            session.merge_data(settings.OUTPUT_1_FILE_NAME, settings.OUTPUT_2_FILE_NAME, settings.OUTPUT_3_FILE_NAME)