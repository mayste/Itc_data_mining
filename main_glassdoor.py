import job
from page_scraping import PageScraping
import path
from scraper import Scraper
import element_id
import company
import constants


if __name__ == "__main__":
    glassdoor_scraper = Scraper()
    current_url = glassdoor_scraper.set_search_keywords()
    print(current_url)

    glassdoor_number_pages = glassdoor_scraper.get_num_pages(current_url)
    print(glassdoor_number_pages)

    list_urls = glassdoor_scraper.generate_pages_links(current_url, glassdoor_number_pages)
    print(list_urls)

    for url in list_urls:
        page = PageScraping(url)
        page.collecting_data_from_page()
        print(page.get_companies_page_list())
        print(page.get_jobs_page_list())
