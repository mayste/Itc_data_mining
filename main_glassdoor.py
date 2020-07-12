"""
Program main function to create DB & logging & init the scraper
Authors: May Steinfeld & Sheryl Sitruk
"""

from datetime import datetime
import logging
import os
import constants as cst
from create_database import Database
from jobs_list_scraping import JobsListScraper

if __name__ == "__main__":
    if not os.path.exists(os.path.join(cst.LOGGING_DIR_NAME)):  # we don't have this directory
        os.mkdir(os.path.join(cst.LOGGING_DIR_NAME))  # create directory
    log_file_name = os.path.join(cst.LOGGING_DIR_NAME,
                                 cst.LOGGING_FILE + f'{datetime.now().strftime(cst.DATE_FORMAT)}' + cst.LOG)
    logging.basicConfig(level=logging.INFO, filename=log_file_name, filemode=cst.FILE_MODE, format=cst.LOGGING_FORMAT,
                        datefmt=cst.DATE_FORMAT)
    database = Database()
    database.create_db()
    glassdoor_scraper = JobsListScraper()
    glassdoor_scraper.set_search_keywords()
    glassdoor_scraper.collecting_data_from_pages(database)
    database.close_connection_database()
