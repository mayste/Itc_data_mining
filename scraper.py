from selenium import webdriver  # allows us to open a browser and do the navigation
from selenium.common.exceptions import NoSuchElementException
import logging
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
import configparser


class Scraper:
    """
       This class contains functions to scrap the website.
    """

    def __init__(self, driver_path):
        """
        Sets up the default URL.
        """
        options = Options()
        # options.headless = True
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        self.browser = webdriver.Firefox(executable_path=driver_path, firefox_options=options)
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # self.browser = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options)
        #self.browser.maximize_window()
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read('Constants')

    def close_popup(self):
        """
        This function use to close the popup message
        :return:
        """
        try:
            # Close pop up
            pop_up = self.browser.find_element_by_xpath(self.config['Path']['POP_UP_XPATH'])
            pop_up.click()
            logging.info(self.config['General']['POP_UP_CLOSE'])
        except NoSuchElementException:
            logging.exception(self.config['General']['NO_POP_UP'])
            pass

    def catch_optional_text_value_by_xpath(self, x_path):
        """
        This function take an Xpath as an argument and try to catch the text. If not succeed return none
        :param x_path: constant
        :return: String or None
        """
        try:
            text_value = self.browser.find_element_by_xpath(x_path).text
            # if the optional data unknown put None
            if self.config['Constant']['UNKNOWN_INFO'] in text_value.lower():
                return None
            return text_value
        except NoSuchElementException:
            logging.exception(self.config['General']['FAIL_TEXT_XPATH'])
            return None

    def convert_company_founded_year(self, company_founded):
        """
        The function get string and convert it to int
        :param company_founded: string
        :return: int or None
        """
        if company_founded is not None:
            try:
                company_founded = int(company_founded)
            except ValueError:
                logging.exception(self.config['General']['FAIL_CONVERT_YEAR'])
                company_founded = None
            finally:
                return company_founded
        else:
            return company_founded
