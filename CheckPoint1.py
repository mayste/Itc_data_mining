from selenium import webdriver  # allows us to open a browser and do the navigation
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import time
import pandas as pd

URL = 'https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=&locT=N&locId=119&jobType=&context=Jobs&sc.keyword=&dropdown=0'
browser = webdriver.Chrome()
browser.get(URL)
jobs_list = []


def collecting_data(num_of_jobs):
    while len(jobs_list) < num_of_jobs:

        time.sleep(3)  # Wait until the page load

        try:
            browser.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass
        time.sleep(40)

        # try:
        #     browser.find_element_by_class_name("SVGInline-svg modal_closeIcon-svg").click()  # clicking to the X.
        # except NoSuchElementException:
        #     pass

        # try:
        #     browser.find_element_by_class_name("modal_main jaCreateAccountModalWrapper").click()  # clicking to the X.
        # except NoSuchElementException:
        #     pass

        job_click_button = browser.find_elements_by_class_name("jl")  # Button on each job we want to click on
        # #job_click_button = browser.find_elements_by_class_name("jl react-job-listing gdGrid ")

        for button_job in job_click_button:
            if len(jobs_list) >= num_of_jobs:
                break
            button_job.click()
            time.sleep(3)

            # collect Data for one job
            employer_name = browser.find_element_by_xpath(
                './/div[@class="employerName"]').text  # browser.find_elements_by_class_name("employerName")
            job_title = browser.find_element_by_xpath('.//div[@class="title"]').text
            job_location = browser.find_element_by_xpath('.//div[@class="location"]').text

            jobs_list.append({"employer name": employer_name, "job title": job_title, "job location": job_location})

            # Clicking on the "next page" button
        try:
            browser.find_element_by_xpath('.//li[@class="next"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_of_jobs,len(jobs_list)))
            break

    #print(jobs_list)
    #print(len(jobs_list))
    print(pd.DataFrame(jobs_list))

collecting_data(50)
