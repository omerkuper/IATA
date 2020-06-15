import time
from datetime import date, timedelta

YesNo = {'y': 'true', 'n': 'false'}

start = ['LHR', 'ams', 'nyc', 'lax']
end = ['EZE', 'AKL', 'DPS']
date_i = [200901]
stay_in = [3, 12, 10, 7]
loop = 5
direct_flight = 'y'

pointA = start
pointB = end

if len(start) <= len(end):
    pointA = start
    pointB = end
    watch = 0
else:
    pointA = end
    pointB = start
    watch = 1


for s in pointA:
    for e in range(len(pointB)):
        counter = 0
        for _ in range(loop):
            date_return = time.strptime(str(date_i[0]), '%y%m%d')
            date_return_i = date(date_return.tm_year, date_return.tm_mon,
                                 date_return.tm_mday) + timedelta(counter)
            if watch is 0:
                print(s, end[e], date_return_i)
            else:
                print(start[e], s, date_return_i)
            counter += 1
        print()


# def Roundtrip():
#     for s in start:
#         for e in range(len(end)):
#             counter = 0
#             for _ in range(loop):
#                 date_return = time.strptime(str(date_i[0]), '%y%m%d')
#                 date_return_i = date(date_return.tm_year, date_return.tm_mon,
#                                      date_return.tm_mday) + timedelta(counter)
#                 print(s, end[e], date_return_i)
#                 counter += 1
#             print()
# # Roundtrip()



def Multi_city():
    lst = []
    counter = 0
    stay = [0] + stay_in
    for stay_long in range(len(stay)):
        for _ in range(loop):
            date_return = time.strptime(str(date_i[0]), '%y%m%d')
            date_return_i = date(date_return.tm_year, date_return.tm_mon,
                                 date_return.tm_mday) + timedelta(counter + _)
            url_sky = f'https://www.skyscanner.net/transport/flights/{start[stay_long]}/{end[stay_long]}/{date_return_i}?flexible_origin=true&flexible_depart=direct&flexible_return=direct&adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=0&preferdirects={YesNo[direct_flight]}&outboundaltsenabled=false&inboundaltsenabled=false&ref=home&currency=USD#results'
            url_jet = f'https://search.jetradar.com/flights?marker=google&origin_iata={start[stay_long].upper()}&destination_iata={end[stay_long].upper()}&depart_date={date_return_i}&with_request=true&adults=1&children=0&infants=0&trip_class=0&locale=en&one_way=false&ct_guests=1+passenger&ct_rooms=1'
            url_mom = f'https://www.momondo.com/flight-search/{start[stay_long].upper()}-{end[stay_long].upper()}/{date_return_i}?sort=bestflight_a'
            lst.append([url_sky, url_jet, url_mom])
        try:
            counter += stay[stay_long + 1]
        except:
            pass
    return lst





