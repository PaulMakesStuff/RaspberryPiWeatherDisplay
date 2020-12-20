from infowindow import InfoWindow
from metoffice import getForecast, getFullDayTemps, getDayRecords, weatherType, getIcon
from datetime import datetime
import json


def displayWeather():
    
    iw = InfoWindow()
    head = 3
    line = 22
    tim = 31
    ico = 48
    flt = 88
    ppy = 110

    # draw the top bar background, and display the time and date.
    iw.line( 3, line, 247, line, 1 )
    timenow = datetime.now()
    iw.text(5, head, timenow.strftime("%H:%M"), 'chikarego24', 1)
    iw.text(245, head, timenow.strftime("%d/%m"), 'chikarego24', 1, 'rt')

    # get weather information.
    recs = getDayRecords()
    record_one = recs[0]
    weather_int = record_one['forecast']['W']
    weather_desc = weatherType(weather_int)
    icon_name = weather_desc.replace(' ', '').lower() + '.bmp'

    # for a bit of debugging, save the information to the file.
    with open('24hrforecast.json', 'w') as f:
        f.write(json.dumps(recs, indent=2, sort_keys=True, default=str))

    # display the weather icon, and description.
    iw.text(20, tim, recs[0]['time'], 'chikarego16', 1, "mt")
    iw.text(56, tim, recs[1]['time'], 'chikarego16', 1, "mt")
    iw.text(91, tim, recs[2]['time'], 'chikarego16', 1, "mt")
    iw.text(126, tim, recs[3]['time'], 'chikarego16', 1, "mt")
    iw.text(161, tim, recs[4]['time'], 'chikarego16', 1, "mt")
    iw.text(196, tim, recs[5]['time'], 'chikarego16', 1, "mt")
    iw.text(231, tim, recs[6]['time'], 'chikarego16', 1, "mt")

    iw.setIcon(3, ico, getIcon(recs[0]['forecast']['W'], recs[0]['isDay']))
    iw.setIcon(38, ico, getIcon(recs[1]['forecast']['W'], recs[1]['isDay']))
    iw.setIcon(73, ico, getIcon(recs[2]['forecast']['W'], recs[2]['isDay']))
    iw.setIcon(108, ico, getIcon(recs[3]['forecast']['W'], recs[3]['isDay']))
    iw.setIcon(143, ico, getIcon(recs[4]['forecast']['W'], recs[4]['isDay']))
    iw.setIcon(178, ico, getIcon(recs[5]['forecast']['W'], recs[5]['isDay']))
    iw.setIcon(213, ico, getIcon(recs[6]['forecast']['W'], recs[6]['isDay']))

    iw.text(20, flt, recs[0]['forecast']['F'] + "°", 'chikarego22', 1, "mt")
    iw.text(56, flt, recs[1]['forecast']['F'] + "°", 'chikarego22', 1, "mt")
    iw.text(91, flt, recs[2]['forecast']['F'] + "°", 'chikarego22', 1, "mt")
    iw.text(126, flt, recs[3]['forecast']['F'] + "°", 'chikarego22', 1, "mt")
    iw.text(161, flt, recs[4]['forecast']['F'] + "°", 'chikarego22', 1, "mt")
    iw.text(196, flt, recs[5]['forecast']['F'] + "°", 'chikarego22', 1, "mt")
    iw.text(231, flt, recs[6]['forecast']['F'] + "°", 'chikarego22', 1, "mt")

    iw.text(20, ppy, f"{recs[0]['forecast']['Pp']}%", 'chikarego20', 1, "mt")
    iw.text(56, ppy, f"{recs[1]['forecast']['Pp']}%", 'chikarego20', 1, "mt")
    iw.text(91, ppy, f"{recs[2]['forecast']['Pp']}%", 'chikarego20', 1, "mt")
    iw.text(126, ppy, f"{recs[3]['forecast']['Pp']}%", 'chikarego20', 1, "mt")
    iw.text(161, ppy, f"{recs[4]['forecast']['Pp']}%", 'chikarego20', 1, "mt")
    iw.text(196, ppy, f"{recs[5]['forecast']['Pp']}%", 'chikarego20', 1, "mt")
    iw.text(231, ppy, f"{recs[6]['forecast']['Pp']}%", 'chikarego20', 1, "mt")

    # display the image on the display, or save to a file if on pc.

    iw.displayImage()