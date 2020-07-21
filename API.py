import requests
import re

def genderize_api_connect(company_name, location):
    location = location.split(',')[0]
    print('ok',location)
    keyword = company_name + ' ' + location
    print('ok4',company_name)
    keyword = re.sub(' +', ' ',keyword).replace(' ','%20')
    print('ok2', keyword)
    URL = f"""https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={keyword}&inputtype=textquery&language=en&fields=name,business_status,formatted_address,name,rating,opening_hours,geometry&key=AIzaSyCPeGAxeCGRvnb5b_Q6ctkmtqvIdOyVxVk"""
    try:
        print('ok3', URL)
        response = requests.get(URL)
        content = response.json()
        print(content)
        adress= content['candidates'][0]['formatted_address']
        business_status = content['candidates'][0]['business_status']
        latitude = content['candidates'][0]['geometry']['location']['lat']
        longitude = content['candidates'][0]['geometry']['location']['lng']
        name = content['candidates'][0]['name']
        rating = content['candidates'][0]['rating']
        return adress, business_status, latitude, longitude, name, rating
    except IndexError:
        pass

