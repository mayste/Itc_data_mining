from datetime import datetime
import logging
import os
import constants as cst
from create_database import Database
from jobs_list_scraping import JobsListScraper


#TODO: delete after using
"""
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
logging.exception('This is a critical message')
"""

# TODO: Try catch for all db and also all the project

if __name__ == "__main__":
    if not os.path.exists(os.path.join(cst.LOGGING_DIR_NAME)):  # we don't have this directory
        os.mkdir(os.path.join(cst.LOGGING_DIR_NAME))  # create directory
    log_file_name = os.path.join(cst.LOGGING_DIR_NAME,f'glassdoor_scrap_{datetime.now().strftime(cst.DATE_FORMAT)}.log')
    logging.basicConfig(level=logging.INFO, filename=log_file_name, filemode=cst.FILE_MODE, format=cst.LOGGING_FORMAT,
                        datefmt=cst.DATE_FORMAT)
    database = Database()
    database.create_db()
    glassdoor_scraper = JobsListScraper()
    glassdoor_scraper.set_search_keywords()
    glassdoor_scraper.collecting_data_from_pages(database)
    database.close_connection_database()



