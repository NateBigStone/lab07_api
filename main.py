import requests
import pandas as pd
from env import *
import time
from datetime import datetime
import logging


key = os.environ.get('WEATHER_KEY')
url = os.environ.get('BASE_URL')
env = os.environ.get("ENV")
log_level = logging.DEBUG if env == "stage" else logging.ERROR
logging.basicConfig(filename='weather-messages.log',
                    filemode='a',
                    format='%(levelname)s %(asctime)s - %(message)s',
                    level=log_level)


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
        table_data = {}
        indexes = []
        table_data['Temperature'] = []
        table_data['Wind'] = []
        forecast_items = data['list']
        for forecast in forecast_items:
            timestamp = forecast['dt']
            """
            The API does not include the timezone offset of the city, so the choices are either UTC, or UTC converted
            to the system time where this app is run. Ideally, it'd be nice to have the time zone of the city, but that
            would require another API call. I'm opting to keep it the system time of the user
            """
            friendly_time = datetime.fromtimestamp(timestamp).strftime('%H:%M')
            day = time.strftime('%A', time.localtime(timestamp))
            temp = forecast['main']['temp']
            wind = forecast['wind']['speed']
            table_data['Temperature'].append(f'{temp}°F')
            table_data['Wind'].append(f'{wind}MPH')
            indexes.append(f'{day} {friendly_time}')
        table = pd.DataFrame(table_data, index=indexes)
        print(f'\n{table}')


def api_call(city, country, query_type):
    return_resp = None
    if key and url:
        try:
            query = {'q': f'{city},{country}', 'units': 'imperial', 'appid': key}
            resp = requests.get(f'{url}{query_type}', params=query).json()
            response_code = resp['cod']
            if int(response_code) == 200:
                return_resp = resp
                logging.debug(resp)
            else:
                raise Exception(f'Bad response: {response_code}')
        except Exception as e:
            print(f'Error- {e}')
            logging.error(e)
    else:
        logging.error('Missing environment variable(s)')
    return return_resp


if __name__ == '__main__':
    main()
