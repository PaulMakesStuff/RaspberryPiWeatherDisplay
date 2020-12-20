import requests
from datetime import datetime, timedelta, timezone
from PIL import Image
import json

base_url = 'http://datapoint.metoffice.gov.uk/public/data/'
key = '<SECRET_KEY_HERE>'
lid = '352877' #  weather station id

# F: Feels like temperature
# U: Max UV index
# Pp: Precipitation probability
# W: This gives the Weather Type
# V: This gives the Visibility
# T: This gives the Temperature
# S: This gives the Wind Speed
# P: This gives the Pressure
# G: This gives the Wind Gust
# D: This gives the Wind Direction
# Pt: This gives the pressure tendency
# Dp: This gives the Dew Point
# H: This gives the Screen Relative Humidity
# $: Hours in minutes after midnight UTC

WEATHER_TYPES = {
  'NA': 'Not available',
  '0': 'Clear night',
  '1': 'Sunny day',
  '2': 'Partly cloudy (night)',
  '3': 'Partly cloudy (day)',
  '4': '-',
  '5': 'Mist',
  '6': 'Fog',
  '7': 'Cloudy',
  '8': 'Overcast',
  '9': 'Light rain shower (night)',
  '10': 'Light rain shower (day)',
  '11': 'Drizzle',
  '12': 'Light rain',
  '13': 'Heavy rain shower (night)',
  '14': 'Heavy rain shower (day)',
  '15': 'Heavy rain',
  '16': 'Sleet shower (night)',
  '17': 'Sleet shower (day)',
  '18': 'Sleet',
  '19': 'Hail shower (night)',
  '20': 'Hail shower (day)',
  '21': 'Hail',
  '22': 'Light snow shower (night)',
  '23': 'Light snow shower (day)',
  '24': 'Light snow',
  '25': 'Heavy snow shower (night)',
  '26': 'Heavy snow shower (day)',
  '27': 'Heavy snow',
  '28': 'Thunder shower (night)',
  '29': 'Thunder shower (day)',
  '30': 'Thunder'
}

VISIBILITY = {
  'UN': 'Unknown',
  'VP': 'Very poor - Less than 1 km',
  'PO': 'Poor - Between 1-4 km',
  'MO': 'Moderate - Between 4-10 km',
  'GO': 'Good - Between 10-20 km',
  'VG': 'Very good - Between 20-40 km',
  'EX': 'Excellent - More than 40 km'
}

def weatherType( w ):
  try:
    return WEATHER_TYPES[w]
  except:
    return 'Not available'

def minutesToHours( minutes ):
  return '{:02d}:{:02d}'.format(*divmod(int(minutes), 60))

def getForecasts():
  url = f'{base_url}val/wxfcs/all/json/{lid}?res=3hourly&key={key}'
  r = requests.get(url)
  if r.status_code != 200: return
  return r.json()

def getForecast():
  day_forecasts = getForecasts()['SiteRep']['DV']['Location']['Period']
  first_forecast = day_forecasts[0]['Rep'][1]
  t = minutesToHours(first_forecast['$'])
  w = WEATHER_TYPES[first_forecast['W']]
  p = first_forecast['Pp'] + '%'
  f = first_forecast['F'] + 'C'  
  return (t, w, p, f)

def getDayRecords():
  start_daytime = datetime.strptime('06:00','%H:%M').time()
  end_daytime = datetime.strptime('18:00','%H:%M').time()
  day_forecasts = getForecasts()['SiteRep']['DV']['Location']['Period']
  out = []
  record_count = 0
  for forecast in day_forecasts:  # go thru each of five days
    date = forecast['value']      # get the date
    for rep in forecast['Rep']:   # get the actual forecast data for each time
      dt_obj = datetime.strptime(f'{date}{minutesToHours(rep["$"])}+0000', f'%Y-%m-%dZ%H:%M%z')
      d1 = datetime.now(timezone.utc) - timedelta(hours = 3)
      if dt_obj > d1:
        if record_count <= 8:
          record_count += 1
          is_day = dt_obj.time() >= start_daytime and dt_obj.time() < end_daytime
          out.append( {
            'time': dt_obj.strftime("%H%M"),
            'forecast': rep,
            'datetime': dt_obj,
            'isDay': is_day,
            'rec': rep
          })
  return out

def getFullDayTemps( recs ):
  temp_list = [int(rec['rec']['F']) for rec in recs] # feels like temp
  max_temp = max(temp_list) + 1
  min_temp = min(temp_list) - 1
  range_temp = max_temp - min_temp
  out = []
  for i in range(len(recs)):
    temp = ( temp_list[i] - min_temp ) / range_temp # adjusted to percentage
    is_day = recs[i]['isDay']
    out.append({
      't': temp,
      'is_day': is_day
    })
  return out

def getIcon( w, isday ):
  im = Image.open("weather_sprites/black.bmp") if isday else Image.open("weather_sprites/white.bmp")
  if w == 'NA': return
  w = int(w) + 1 # skip n/a in sprite sheet
  xi = (w % 6)
  yi = (w - xi) / 6
  x = xi * 35
  y = yi * 35
  cr = im.crop((x, y, x + 34, y + 34))
  return cr
