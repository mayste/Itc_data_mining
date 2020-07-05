"""
This class create an instance of comapny with all the information.
Authors: May Steinfeld & Sheryl Sitruk
"""


class Company:
    def __init__(self, company_name, company_rating):
        """
        constructor
        :param company_name: string
        :param company_rating: float
        #TODO: check maybe it list of strings
        """
        self.company_name = company_name
        self.company_rating = company_rating

        self.company_size = None
        self.company_founded = None
        self.company_industry = None
        self.company_sector = None
        self.company_type = None
        self.company_competitors = []
        self.company_revenue = None
        self.company_headquarters = None

    def get_name(self):
        """
        get company name
        :return: string
        """
        return self.company_name

    def set_name(self, value):
        """
        set company name
        :param value: string
        :return:
        """
        self.company_name = value

    def get_company_size(self):
        """
        get company size
        :return: string
        """
        return self.company_size

    def set_company_size(self, value):
        """
        set company size
        :param value: string
        :return:
        """
        self.company_size = value

    def get_company_founded(self):
        """
        get company founded year
        :return: year
        """
        return self.company_founded

    def set_company_founded(self, value):
        """
        set company founded year
        :param value: year
        :return:
        """
        self.company_founded = value

    def get_company_industry(self):
        """
        get company industry
        :return: string
        """
        return self.company_industry

    def set_company_industry(self, value):
        """
        set company industry
        :param value: string
        :return:
        """
        self.company_industry = value

    def get_company_sector(self):
        """
        get company sector
        :return: string
        """
        return self.company_sector

    def set_company_sector(self, value):
        """
        set company sector
        :param value: string
        :return:
        """
        self.company_sector = value

    def get_company_type(self):
        """
        get company type
        :return: string
        """
        return self.company_type

    def set_company_type(self, value):
        """
        set company type
        :param value: string
        :return:
        """
        self.company_type = value

    def get_company_rating(self):
        """
        get company rating
        :return: float
        """
        return self.company_rating

    def set_company_rating(self, value):
        """
        set company rating
        :param value: float
        :return:
        """
        self.company_rating = value

    def get_company_competitors(self):
        """
        get company competitors
        :return: string
        """
        return self.company_competitors

    def set_company_competitors(self, value):
        """
        set company competitors
        :param value: string
        :return:
        """
        #TODO: Check if working
        self.company_competitors + value

    def get_company_revenue(self):
        """
        get company revenue
        :return: string
        """
        return self.company_revenue

    def set_company_revenue(self, value):
        """
        set company revenue
        :param value: string
        :return:
        """
        self.company_revenue = value

    def get_company_headquarters(self):
        """
        get company headquarters
        :return: string
        """
        return self.company_headquarters

    def set_company_headquarters(self, value):
        """
        set company headquarters
        :param value: string
        :return:
        """
        self.company_headquarters = value

    def __repr__(self):  # TODO: temp function to print
        return ''.join(f'\ncompany: {self.company_name}\nsize: {self.company_size}\ncompany_founded: '
                       f'{self.company_founded}\ncompany_industry: {self.company_industry}\ncompany_sector: '
                       f'{self.company_sector}\ncompany_type: {self.company_type}\ncompany_rating: '
                       f'{self.company_rating}\ncompany_competitors: {self.company_competitors}\ncompany_revenue: '
                       f'{self.company_revenue}\ncompany_headquarters: {self.company_headquarters}')
