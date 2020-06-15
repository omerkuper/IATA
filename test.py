import time
from datetime import date, timedelta

YesNo = {'y': 'true', 'n': 'false'}

start = ['LHR', 'ams', 'nyc']
end = ['EZE', 'chc']
date_i = [200901]
stay_in = [3, 10, 8]
loop = 3
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

                if len(start) >= len(end) and len(stay_in) != 1:
                    y = counter_out
                elif len(start) >= len(end) and len(stay_in) == 1:
                    y = 0
                else:
                    y = destination

                date_return = time.strptime(str(date_i[x]), '%y%m%d')
                date_return_i = date(date_return.tm_year, date_return.tm_mon,
                                     date_return.tm_mday) + timedelta(counter)

                date_return_q = date(date_return.tm_year, date_return.tm_mon,
                                     date_return.tm_mday) + timedelta(counter + stay_in[y])
                url_sky = f'https://www.skyscanner.net/transport/flights/{departure}/{end[destination]}/{date_return_i}/{date_return_q}?flexible_origin=true&flexible_depart=direct&flexible_return=direct&adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=1&preferdirects={YesNo[direct_flight]}&outboundaltsenabled=false&inboundaltsenabled=false&ref=home&currency=USD#results'
                url_jet = f'https://search.jetradar.com/flights?marker=google&origin_iata={departure.upper()}&destination_iata={end[destination].upper()}&depart_date={date_return_i}&return_date={date_return_q}&with_request=true&adults=1&children=0&infants=0&trip_class=0&locale=en&one_way=false&ct_guests=1+passenger&ct_rooms=1'
                url_mom = f'https://www.momondo.com/flight-search/{departure}-{end[destination]}/{date_return_i}/{date_return_q}?sort=bestflight_a'
                lst.append([url_sky, url_jet, url_mom])
                counter += 1
        counter_out += 1
    return lst

for u in RoundTrip():
    print(u)


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
