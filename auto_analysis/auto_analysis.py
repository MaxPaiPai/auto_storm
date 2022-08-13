# Author: Max Zhao
import numpy as np
import pandas as pd
from datetime import datetime
import logging
import os

# User input storm number: al******
# number = input("Please input the storm number (format: al______): ")
number = 'al072021'

def generate_time(storm):
    """
    @param: storm, pandas dataframe
    @return: (s_date, e_date, delta_days), tuple
    """
    try:
        data_start_y = int(storm[0][2][1:5])
        data_start_m = int(storm[0][2][5:7])
        data_start_d = int(storm[0][2][7:9])
        data_start_t = int(storm[0][2][9:])
        data_end_y = int(storm[event-1][2][1:5])
        data_end_m = int(storm[event-1][2][5:7])
        data_end_d = int(storm[event-1][2][7:9])
        data_end_t = int(storm[event-1][2][9:])

        s_date = datetime(data_start_y, data_start_m, data_start_d, data_start_t)
        e_date = datetime(data_end_y, data_end_m, data_end_d, data_end_t)
        delta = e_date - s_date
        delta_days = float(delta.total_seconds()/86400)
        
        return (s_date, e_date, delta_days)
    except:
        print('Something was wrong with data...')


def generate_gauge(storm):

    print(len(storm))
    print(storm[65][7])
    print(storm[65][6])





    return gauge_list


def generate_significance(storm):




    return "Stations in the US have evident surge patterns. Validation is encouraged."

 
def generate_storm_data(number):

    storm = pd.DataFrame(pd.read_csv(str('http://ftp.nhc.noaa.gov/atcf/archive/2021/b'+number+'.dat.gz'),
            sep=':', header=None,))

    storm = storm[0].str.split(',')

    return storm

def generate_station_data():

    return 


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

    report_time = generate_time(storm)

    # Log storm time info
    logging.info('===============Report of Time===============')
    logging.info('\n')
    logging.info(f'Data for the storm is available starting at {report_time[0]}')
    logging.info('\n')
    logging.info(f'Data for the storm is NOT available after {report_time[1]}')
    logging.info('\n')
    logging.info(f'{report_time[2]} days are ready to be simulated')
    logging.info('\n')
    logging.info('============================================')


    station_meta = pd.read_json('https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json')
    print(station_meta['stations'][0]['id'])
