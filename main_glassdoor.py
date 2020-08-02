"""
Program main function to create DB & logging & init the scraper
Authors: May Steinfeld & Sheryl Sitruk
"""

from datetime import datetime
import logging
import os
from create_database import Database
from jobs_list_scraping import JobsListScraper
import configparser
import command_args


def main():
    key_api = command_args.args.Google_Key_API
    keyword_location = command_args.args.job_location
    keyword_job_title = command_args.args.job_title
    sql_password = command_args.args.database_password
    sql_user = command_args.args.database_user
    geckodriver_path = command_args.args.driver_path
    config = configparser.ConfigParser(interpolation=None)
    config.read('Constants')
    if not os.path.exists(os.path.join(config['Constant']['LOGGING_DIR_NAME'])):  # we don't have this directory
        os.mkdir(os.path.join(config['Constant']['LOGGING_DIR_NAME']))  # create directory
    log_file_name = os.path.join(config['Constant']['LOGGING_DIR_NAME'],
                                 config['Constant']['LOGGING_FILE'] + f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                                 + config['Constant']['LOG'])
    logging.basicConfig(level=logging.INFO, filename=log_file_name, filemode=config['Constant']['FILE_MODE'],
                        format=config['Constant']['LOGGING_FORMAT'], datefmt=config['Constant']['DATE_FORMAT'])
    database = Database(sql_password, sql_user)
    database.create_db()
    glassdoor_scraper = JobsListScraper(geckodriver_path, key_api, keyword_job_title, keyword_location)
    glassdoor_scraper.set_search_keywords()
    glassdoor_scraper.collecting_data_from_pages(database)
    database.close_connection_database()


if __name__ == "__main__":
    main()
