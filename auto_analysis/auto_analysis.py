# Author: Max Zhao
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import clawpack.geoclaw.util
from math import sin, cos, sqrt, atan2, radians
import re
import logging
import os

# User input storm number: al******
number = input("Please input the storm number (format: al______): ")


def generate_time(storm):
    """
    @param: storm, pandas dataframe
    @return: (s_date, e_date, delta_days), tuple
    """
    try:
        user_in = str(input("Please input the landfall time, format: year+month+date+time (no space in between): "))

        land_y = int(user_in[0:4])
        land_m = int(user_in[4:6])
        land_d = int(user_in[6:8])
        land_t = int(user_in[8:])

        data_start_y = int(storm[0][2][1:5])
        data_start_m = int(storm[0][2][5:7])
        data_start_d = int(storm[0][2][7:9])
        data_start_t = int(storm[0][2][9:])

        data_end_y = int(storm[event-1][2][1:5])
        data_end_m = int(storm[event-1][2][5:7])
        data_end_d = int(storm[event-1][2][7:9])
        data_end_t = int(storm[event-1][2][9:])

        l_date = datetime(land_y, land_m, land_d, land_t)
        s_date = datetime(data_start_y, data_start_m, data_start_d, data_start_t)
        e_date = datetime(data_end_y, data_end_m, data_end_d, data_end_t)

        before_landfall = float((l_date - s_date).total_seconds()/86400)
        after_landfall = float((e_date - l_date).total_seconds()/86400)
        delta_days = float((e_date - s_date).total_seconds()/86400)

        return (s_date, e_date, delta_days, before_landfall, after_landfall)
    except:
        print('Something was wrong with data...')

def convert_km(lat_1, lng_1, lat_2, lng_2):

    radius = 6371.0

    d_lat = radians(lat_2) - radians(lat_1)
    d_lng = radians(lng_2) - radians(lng_1)
    
    var_1 = sin(d_lat / 2)**2 + cos(radians(lat_1)) * cos(radians(lat_2)) * sin(d_lng / 2)**2
    var_2 = 2 * atan2(sqrt(var_1), sqrt(1 - var_1))
   
    distance = radius * var_2

    return distance


def generate_gauge(metadata):

    location = []
    for i in range(len(storm)):
        lat_raw = re.findall(r'\d+',storm[i][6])
        lon_raw = re.findall(r'\d+',storm[i][7])
        lat = float(int(lat_raw[0])/10)
        lon = float(int(lon_raw[0])/10)
        location.append((lat, lon))
    

    gauge = {}
    for i in location:
        for j in range(len(station_meta)):
            if (i[0]-0.5)<station_meta['stations'][j]['lat']<(i[0]+0.5):
                if (-i[1]-1)<station_meta['stations'][j]['lng']<(-i[1]+1):
                    if station_meta['stations'][j]['name'] not in gauge:
                        gauge[station_meta['stations'][j]['name']] = [station_meta['stations'][j]['id'],
                        station_meta['stations'][j]['lat'],station_meta['stations'][j]['lng'], 
                        round(convert_km(station_meta['stations'][j]['lat'], station_meta['stations'][j]['lng'], i[0], -i[1]), 3)]


    return gauge


def generate_significance(gauge, t0, tf):

    max_surge = {}
    max_surge_list = []
    dis_list = []
    index_list = []
    for item in gauge:
        date_time, water_level, prediction = clawpack.geoclaw.util.fetch_noaa_tide_data(gauge[item][0], report_time[0], report_time[1])
        date_time, mean_water_level, mean_prediction = clawpack.geoclaw.util.fetch_noaa_tide_data(gauge[item][0], report_time[0], report_time[1], datum='MSL')
        max_surge_list.append(round(np.max(water_level - prediction) - np.mean(mean_water_level - mean_prediction), 3))
        max_surge[gauge[item][0]] = round(np.max(water_level - prediction) - np.mean(mean_water_level - mean_prediction), 3)
        dis_list.append(gauge[item][3])
        index_list.append(item)
    if len(max_surge_list) == 0:
        logging.info('===============Report Storm Significance===============')
        logging.info('No gauge was detected...')
        logging.info('=======================================================')
        return pd.DataFrame({'A' : []})
    else:
        raw_data = {'max surge': max_surge_list, 'distance': dis_list}
        data = pd.DataFrame.from_dict(raw_data, orient='index', columns = index_list)

    return data
 

def generate_storm_data(number):

    storm = pd.DataFrame(pd.read_csv(str('http://ftp.nhc.noaa.gov/atcf/archive/2021/b'+number+'.dat.gz'),
            sep=':', header=None,))

    storm = storm[0].str.split(',')

    return storm

def generate_station_data():

    station_meta = pd.read_json('https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json')

    return station_meta


if __name__ == "__main__":
# Create and configure logger in current working directory with name 'auto_analysis_stormnumber.log'
    logging.basicConfig(filename=str(os.path.dirname(__file__)+'/auto_analysis_'+str(number)+'.log'), 
                        format='%(asctime)s %(message)s', 
                        filemode='w') 

    # Create an object 
    logger=logging.getLogger() 

    # Set the threshold of logger to DEBUG 
    logger.setLevel(logging.DEBUG) 


    storm = generate_storm_data(number)
    event = len(storm)

    # Log storm time info
    report_time = generate_time(storm)
    logging.info('===============Report of Time===============')
    logging.info('\n')
    logging.info(f'Data for the storm is available starting at {report_time[0]}')
    logging.info('\n')
    logging.info(f'Data for the storm is NOT available after {report_time[1]}')
    logging.info('\n')
    logging.info(f'{report_time[2]} days are ready to be simulated')
    logging.info(f'{round(report_time[3],2)} days before landfall')
    logging.info(f'{round(report_time[4],2)} days after landfall')
    logging.info('\n')
    logging.info('============================================')

    logging.info('\n')

    station_meta = generate_station_data()
    
    gauge = generate_gauge(station_meta)
    
    logging.info('==============Search for Gauge==============')
    for item in gauge:
        logging.info(f'{item, gauge[item]}')
    logging.info('==========================================')

    logging.info('\n')

    data = generate_significance(gauge, report_time[0], report_time[1])
    if data.empty:
        pass
    else:
        pd.set_option("display.max.columns", None)
        logging.info('\n \n ===========================Report Storm Significance===========================')
        logging.info(f'\n \n \n {data.head()}')
        logging.info('\n \n ===============================================================================')
    