  
import time
from datetime import date, timedelta

YesNo = {'y': 'true', 'n': 'false'}

start = ['LHR', 'ams', 'nyc']
end = ['EZE', 'ttt', 'aaa']
date_i = [200901, 230401, 220301]
stay_in = [3]
loop = 2
direct_flight = 'y'


def RoundTrip():
    lst = []
    counter_out = 0
    for departure in start:
        for destination in range(len(end)):
            counter = 0
            for _ in range(loop):

                if len(date_i) == 1:
                    x = 0
                elif len(start) >= len(end):
                    x = counter_out
                else:
                    x = destination
               
                
                if len(stay_in) == 1:
                    y = 0
                elif len(stay_in) == len(start) and len(start) != len(end):
                    y = counter_out
                elif len(stay_in) == len(end) and len(start) != len(end):
                    y = destination
                elif len(start) == len(end):
                    y = destination
                else:
                    y = destination


                date_return = time.strptime(str(date_i[x]), '%y%m%d')
                date_return_i = date(date_return.tm_year, date_return.tm_mon,
                                     date_return.tm_mday) + timedelta(counter)

                date_return_q = date(date_return.tm_year, date_return.tm_mon,
                                     date_return.tm_mday) + timedelta(counter + stay_in[y])
                print(departure, end[destination], date_return_i, date_return_q)
                counter += 1
        counter_out += 1
    return lst

for u in RoundTrip():
    print(u)
