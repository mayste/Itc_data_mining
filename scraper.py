# from command_args import args

# TODO: try to find better address
url = f'https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword' \
      f'=&locT=N&locId=119&jobType=&context=Jobs&sc.keyword=&dropdown=0 '

# SLEEP_FACTOR = args.sleep_factor

class Scraper():
    def __init__(self, start_url):
        pass

    def set_search_keywords(self):
        #return the search url link
        pass

    def get_num_pages(self, search_url):
        pass

    def generate_pages_links(self, search_url):
        #call page_analysis to scrap the first page and also save first page address
        #here implement click next and save a list with new url format from page 2 until number of pages
        #send this list to page _analysis
        pass