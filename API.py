import requests
import re

def genderize_api_connect(company_name, location, key_api):
    location = location.split(',')[0]
    keyword = company_name + ' ' + location
    keyword = re.sub(' +', ' ',keyword).replace(' ','%20')
    URL = f"""https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={keyword}&inputtype=textquery&language=en&fields=name,business_status,formatted_address,name,rating,opening_hours,geometry&key={key_api}"""
    try:
        response = requests.get(URL)
        content = response.json()
        adress= content['candidates'][0]['formatted_address']
        business_status = content['candidates'][0]['business_status']
        latitude = content['candidates'][0]['geometry']['location']['lat']
        longitude = content['candidates'][0]['geometry']['location']['lng']
        name = content['candidates'][0]['name']
        rating = content['candidates'][0]['rating']
        return adress, business_status, latitude, longitude, name, rating
    except IndexError:
        pass

