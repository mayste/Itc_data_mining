import requests
import re
import configparser

class ApiInfo:
    def __init__(self, name=None, address=None, longitude=None, latitude=None):
        """
         constructor
        :param name: string
        :param address: string
        :param longitude: string
        :param latitude: string
        """
        self.company_name_google = name
        self.address_google = address
        self.longitude_google = longitude
        self.latitude_google = latitude

    def get_company_name_google(self):
        """
        get company name from google places API
        :return: string
        """
        return self.company_name_google

    def get_address_google(self):
        """
        get address from google places API
        :return: string
        """
        return self.address_google

    def set_address_google(self, value):
        """
        set address from job table
        :param value: string
        :return:
        """
        self.address_google = value

    def get_longitude_google(self):
        """
        get longitude from google places API
        :return: string
        """
        return self.longitude_google

    def get_latitude_google(self):
        """
        get latitude from google places API
        :return: string
        """
        return self.latitude_google

    def __repr__(self):
        """
        function to print the class
        :return:
        """
        return ''.join(
            f"\ncomapny_name_google: {self.company_name_google}\naddress_google: {self.address_google}"
            f"\nlongitude_google: {self.longitude_google}\nlatitude_google: {self.latitude_google}")


def create_api_connect(company_name, location, key_api):
    config = configparser.ConfigParser(interpolation=None)
    config.read('Constants')
    location = location.split(config['Constant']['COMA'])[int(config['Constant']['FIRST_ELEMENT'])]
    keyword = company_name + ' ' + location
    keyword = re.sub(' +', ' ', keyword).replace(' ', config['Constant']['SPACE_20'])
    url_api = config['Path']['API_URL_FIRST_PART'] + keyword + config['Path']['API_URL_SECOND_PART'] + key_api
    try:
        response = requests.get(url_api)
        content = response.json()
        address = content[config['Constant']['CANDIDATES']][int(config['Constant']['FIRST_ELEMENT'])][
            config['Constant']['FORMATTED']]
        latitude = content[config['Constant']['CANDIDATES']][int(config['Constant']['FIRST_ELEMENT'])][
            config['Constant']['GEOMETRY']][config['Constant']['LOCATION']][config['Constant']['LATITUDE']]
        longitude = content[config['Constant']['CANDIDATES']][int(config['Constant']['FIRST_ELEMENT'])][
            config['Constant']['GEOMETRY']][config['Constant']['LOCATION']][config['Constant']['LONGITUDE']]
        name = content[config['Constant']['CANDIDATES']][int(config['Constant']['FIRST_ELEMENT'])][
            config['Constant']['NAME']]
        google_api = ApiInfo(name, address, longitude, latitude)
    except IndexError:
        google_api = ApiInfo()
    finally:
        return google_api
