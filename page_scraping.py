from scraper import Scraper

class PageScraping(Scraper):

    def __init__(self,page_url):
        Scraper.__init__(self)
        #this class will get a url for page and scrap the data inside then create a list of job objects and company objects
        # in the end of this class we have a list with all the jobs and company for this page that we can return to glassdor class
 #   def get_first_url(self):
 #       return self._first_users_page_url

