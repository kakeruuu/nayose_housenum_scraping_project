import traceback

from selenium.common.exceptions import NoSuchElementException

from model.nayose import Nayose
from process.suumo.scraper import SuumoScraper

if __name__ == "__main__":
    from src.log.logger import setup_logger
else:
    from log.logger import setup_logger


def run_suumo_scraper(
    housenum0_record: list[Nayose], is_headless=False
) -> dict[str, list[dict[str, int | str]]]:
    logger = setup_logger("Scraper_logger", "scraper_error.log")
    with SuumoScraper(is_headless=is_headless) as bot:
        for record in housenum0_record:
            try:
                bot.scrape_suumo(record)

            except NoSuchElementException as e:
                logger.info(f"NoSuchElementException: {e}")
                logger.info(f"{traceback.format_exc()}")
                continue

            except Exception as e:
                logger.error(f"An error occurred: {e}")
                logger.error(f"{traceback.format_exc()}")
                return bot.row_data_dict

        return bot.row_data_dict
