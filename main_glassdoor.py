from scraper import Scraper
from datetime import datetime
import logging
import os
import constants as cst
from create_database import Database


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
    log_file_name = os.path.join(cst.LOGGING_DIR_NAME,f'glassdoor_scrap_{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.log')
    logging.basicConfig(level=logging.INFO, filename=log_file_name, filemode='w', format='%(asctime)s - %(name)s - '
                                                                                          '%(levelname)s - %(message)s'
                        ,datefmt='%Y-%m-%d %H:%M:%S')
    database = Database()
    database.create_db()
    glassdoor_scraper = Scraper()
    glassdoor_scraper.set_search_keywords()
    glassdoor_scraper.collecting_data_from_pages(database)



