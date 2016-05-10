#!/usr/bin/env python2
'''
 A Script to fetch data from the rrd database
 and to print out the JSON format for it.
'''

import rrdtool
import json

def header(rrd_file):
    """
    Returns a tuple of headers in the rrd file
    rrd_file - path to rrd file.
    """
    rrd_file = str(rrd_file)
    header_index = 1
    return rrdtool.fetch(rrd_file, 'MAX', '-s end-1min')[header_index]

def package_data(rrd_file, time_period, columns):
    '''
    Packages the data ready to be dumped to json notation so it can 
    be used in a web application. 
    The function takes
    rrd_file - path to an rrd file
    time_peroid - time peorid as per rrdtool e.g. 1m (1 month) 1h (1 hour)
    columns - list of column names to package
    returns an array of dictionaries
    '''
    #---------------------------------------------------------------------    
    # convert all inputs to str as sometimes passed unicode and rrd choaks
    #---------------------------------------------------------------------
    rrd_file = str(rrd_file)
    time_period = str(time_period)
    columns = [str(col) for col in columns]
    rrd_output = rrdtool.fetch(rrd_file, 'MAX', '-s end-' + time_period)

    #------------------------------------------------------------
    # Work out the timings in milli seconds
    # This needs to be done as javascript works in milliseconds
    # For the time period
    #------------------------------------------------------------
    timing_index = 0
    timing = rrd_output[timing_index]
    start = timing[0] * 1000
    end = timing[1] * 1000
    step = timing[2] * 1000
    time = range(start, end, step)

    #------------------------------------------------------------
    # Get the data for the column for time period
    #------------------------------------------------------------
    data_index = 2
    data = rrd_output[data_index]
    column_packages = []

    for column_name in columns:
        column_name_index = header(rrd_file).index(column_name)
        used = []
        for row in data:
            # Round the numbers as you cannot have a floating point for 
            # license usage.
            value = row[column_name_index]
            if value is None:
                used.append(value)
            else:
                used.append(round(value))

            #-------------------------------------
            # zip the time and the data together 
            #-------------------------------------
            values = zip(time, used)
        column_packages.append({'key':column_name.upper(), 'values':values})
    return column_packages

if __name__ == '__main__':
    DATABASE_NAME = '/tmp/test.rrd'
    print (header(DATABASE_NAME))
    print package_data(DATABASE_NAME, '5m', ['used','total'])

