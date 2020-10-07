import requests
from env import *

key = os.environ.get('WEATHER_KEY')
url = os.environ.get('BASE_URL')


def main():
    city = input('Please enter a city:\n').lower().strip()
    country = input('Please enter a country code:\n').lower().strip()
    query_type = 'weather'

    data = api_call(city, country, query_type)
    print(data)
    if data:
        weather_description = data['weather'][0]['description']
        temp = data['main']['temp']
        print(f'The weather is {weather_description}, the temperature is {temp:.2f}F.')


def api_call(city, country, query_type):
    return_resp = None
    if key and url:
        try:
            query = {'q': f'{city},{country}', 'units': 'imperial', 'appid': key}
            resp = requests.get(f'{url}{query_type}', params=query).json()
            print(resp)
            response_code = resp['cod']
            if response_code == 200:
                return_resp = resp
            else:
                raise Exception(f'Bad response: {response_code}')
        except Exception as e:
            print(e)
    else:
        print('Missing environment variable(s)')
    return return_resp


if __name__ == '__main__':
    main()






#"http://api.openweathermap.org/data/2.5/weather?q=paris,fr&units=imperial&appid=6b9aabd5fe36a23f54cc26c372236a65"
# Part 1: Weather Forecast
#
# Use the forecast API to create a detailed, neatly formatted 5-day forecast, for anywhere the user chooses.
#
# Make sure your your API key is not coded into your program. It should read the key from an environment variable.
#
# Use a query parameter dictionary in the request.
#
# Your forecast should show the temperature and unit (F or C), weather description, and wind speed for every three hour interval, over the next 5 days.
#
# Your program should handle errors. What type of errors do you anticipate? How will you deal with them?
#
# Part 2: Time choice
#
# Will you show the local time in Minnesota, or the UTC time? Why? Add some comments to your program explaining your choice. Reading: Unix Time
#
# Part 3: Logging vs Print
#
# When do you use one, when do you use the other? Replace any message that are only of interest to the developer with logging. When you run your program, it should only print user-friendly messages.
#
# Make sure you can find the log output from your program.
#
# Should you log sensitive information, for example, values of API keys?
#
# To Submit: create GitHub repository for this program, with example log output. Submit repository link to the D2L dropbox.
