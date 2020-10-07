import requests
from env import *
from datetime import datetime

key = os.environ.get('WEATHER_KEY')
url = os.environ.get('BASE_URL')


def main():
    city = input('Please enter a city:\n').lower().strip()
    country = input('Please enter a country code:\n').lower().strip()
    query_type = 'forecast'

    data = api_call(city, country, query_type)
    if data and query_type == 'weather':
        weather_description = data['weather'][0]['description']
        temp = data['main']['temp']
        print(f'The weather is {weather_description}, the temperature is {temp:.2f}F.')
    elif data and query_type == 'forecast':
        forecast_items = data['list']
        for forecast in forecast_items:
            timestamp = forecast['dt']
            date = datetime.fromtimestamp(timestamp)
            temp = forecast['main']['temp']
            wind = forecast['wind']['speed']
            print(f'at {date} temp is {temp}F, and wind is {wind}')
        print(data)


def api_call(city, country, query_type):
    return_resp = None
    if key and url:
        try:
            query = {'q': f'{city},{country}', 'units': 'imperial', 'appid': key}
            resp = requests.get(f'{url}{query_type}', params=query).json()
            response_code = resp['cod']
            if int(response_code) == 200:
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
