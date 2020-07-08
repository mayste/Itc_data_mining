from page_scraping import PageScraping
from scraper import Scraper
from datetime import datetime
import logging
import os
from create_database import Database

# TODO: delete after using
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
    # TODO: change the path / logging to fit linux and windows
    if not os.path.exists('./logging'):  # we don't have this directory
        os.mkdir('./logging')  # create directory
    log_file_name = f'./logging/glassdoor_scrap_{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.log'
    logging.basicConfig(level=logging.DEBUG, filename=log_file_name, filemode='w', format='%(asctime)s - %(name)s - '
                                                                                          '%(levelname)s - %(message)s'
                        , datefmt='%Y-%m-%d %H:%M:%S')
    database = Database()
    database.create_db()

    glassdoor_scraper = Scraper()
    current_url = glassdoor_scraper.set_search_keywords()
    logging.info(current_url)
    # print(current_url)

    glassdoor_number_pages = glassdoor_scraper.get_num_pages(current_url)
    print(glassdoor_number_pages)

    list_urls = glassdoor_scraper.generate_pages_links(current_url, glassdoor_number_pages)
    print(list_urls)

    for url in list_urls:
        page = PageScraping(url)
        page.collecting_data_from_page(database)
        print(page.get_companies_page_list())
        print(page.get_jobs_page_list())
