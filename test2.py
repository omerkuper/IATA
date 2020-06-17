import time
from datetime import date, timedelta

YesNo = {'y': 'true', 'n': 'false'}

start = ['LHR', 'akl', 'NYC', 'AMS']
end = ['akl', 'NYC', 'AMS', 'LHR']
date_i = [200901]
stay_in = [19, 7, 10, 56]
loop = 3
direct_flight = 'y'


def look(counter_out, destination):
    if len(date_i) == 1:
        dates = 0
    elif len(date_i) == len(start):
        dates = counter_out
    else:
        dates = destination

    if len(stay_in) == 1:
        staying = 0
    elif len(stay_in) == len(start):
        staying = counter_out
    else:
        staying = destination
    return dates, staying


def urls(*args):
    route = args[0]
    if route == 'OneWay':
        departure, destination, date_return_i = args[1], args[2], args[3]
        url_sky = f'https://www.skyscanner.co.il/transport/flights/{departure}/{end[destination]}/{date_return_i}/?adultsv2=1&cabinclass=economy&childrenv2=&inboundaltsenabled=false&outboundaltsenabled=false&preferdirects={YesNo[direct_flight]}&rtn=0&priceSourceId=&priceTrace=&qp_prevCurrency=USD&qp_prevPrice=OneWayNone&qp_prevProvider=ins_month'
        url_jet = f'https://search.jetradar.com/flights?marker=google&origin_iata={departure.upper()}&destination_iata={end[destination].upper()}&depart_date={date_return_i}&with_request=true&adults=1&children=0&infants=0&trip_class=0&locale=en&one_way=false&ct_guests=1+passenger&ct_rooms=1'
        url_mom = f'https://www.momondo.com/flight-search/{departure}-{end[destination]}/{date_return_i}?sort=bestflight_a'

    elif route == 'RoundTrip':
        departure, destination, date_return_i, date_return_q = args[1], args[2], args[3], args[4]
        url_sky = f'https://www.skyscanner.net/transport/flights/{departure}/{end[destination]}/{date_return_i}/{date_return_q}?flexible_origin=true&flexible_depart=direct&flexible_return=direct&adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=1&preferdirects={YesNo[direct_flight]}&outboundaltsenabled=false&inboundaltsenabled=false&ref=home&currency=USD#results'
        url_jet = f'https://search.jetradar.com/flights?marker=google&origin_iata={departure.upper()}&destination_iata={end[destination].upper()}&depart_date={date_return_i}&return_date={date_return_q}&with_request=true&adults=1&children=0&infants=0&trip_class=0&locale=en&one_way=false&ct_guests=1+passenger&ct_rooms=1'
        url_mom = f'https://www.momondo.com/flight-search/{departure}-{end[destination]}/{date_return_i}/{date_return_q}?sort=bestflight_a'

    elif route == 'MultiCity':
        stay_long, date_return_i = args[1], args[2]
        url_sky = f'https://www.skyscanner.net/transport/flights/{start[stay_long]}/{end[stay_long]}/{date_return_i}?flexible_origin=true&flexible_depart=direct&flexible_return=direct&adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=0&preferdirects={YesNo[direct_flight]}&outboundaltsenabled=false&inboundaltsenabled=false&ref=home&currency=USD#results'
        url_jet = f'https://search.jetradar.com/flights?marker=google&origin_iata={start[stay_long].upper()}&destination_iata={end[stay_long].upper()}&depart_date={date_return_i}&with_request=true&adults=1&children=0&infants=0&trip_class=0&locale=en&one_way=false&ct_guests=1+passenger&ct_rooms=1'
        url_mom = f'https://www.momondo.com/flight-search/{start[stay_long].upper()}-{end[stay_long].upper()}/{date_return_i}?sort=bestflight_a'
    return url_sky, url_jet, url_mom


def date_returns(*args):
    route = args[0]
    counter = args[1]
    if route is not 'MultiCity':
      dates =  args[2]
      date_return = time.strptime(str(date_i[dates[0]]), '%y%m%d')
      date_return_i = date(date_return.tm_year, date_return.tm_mon,
                            date_return.tm_mday) + timedelta(counter)
      try:
        dates_staying = args[3]
        date_return_q = date(date_return.tm_year, date_return.tm_mon,
                                      date_return.tm_mday) + timedelta(counter + stay_in[dates_staying[1]])
        return date_return_i, date_return_q
      except:
        return date_return_i
    else:
      adding = args[2]
      date_return_i = date(date_return.tm_year, date_return.tm_mon,
                                 date_return.tm_mday) + timedelta(counter + adding)





def OneWay():
    lst = []
    for departure in range(len(start)):
        for destination in range(len(end)):
            counter = 0
            for _ in range(loop):
                dates = look(departure, destination)
                date_return = time.strptime(str(date_i[dates[0]]), '%y%m%d')
                date_return_i = date(date_return.tm_year, date_return.tm_mon,
                                     date_return.tm_mday) + timedelta(counter)
                url = urls('OneWay', start[departure], destination, date_return_i)
                lst.append(url)
                counter += 1
    return lst


def RoundTrip():
    lst = []
    for departure in range(len(start)):
        for destination in range(len(end)):
            counter = 0
            for _ in range(loop):
                dates = look(departure, destination)

                date_return = time.strptime(str(date_i[dates[0]]), '%y%m%d')
                date_return_i = date(date_return.tm_year, date_return.tm_mon,
                                     date_return.tm_mday) + timedelta(counter)

                date_return_q = date(date_return.tm_year, date_return.tm_mon,
                                     date_return.tm_mday) + timedelta(counter + stay_in[dates[1]])
                url = urls('RoundTrip', start[departure], destination, date_return_i, date_return_q)
                lst.append(url)
                counter += 1
    return lst


def MultiCity():
    lst = []
    counter = 0
    stay = [0] + stay_in
    for stay_long in range(len(stay)):
        for _ in range(loop):
            date_return = time.strptime(str(date_i[0]), '%y%m%d')
            date_return_i = date(date_return.tm_year, date_return.tm_mon,
                                 date_return.tm_mday) + timedelta(counter + _)
            url = urls('MultiCity', stay_long, date_return_i)
            lst.append(url)
        try:
            counter += stay[stay_long + 1]
        except:
            pass
    return lst


# for u in MultiCity():
#     print(u)

for u in RoundTrip():
    print(u)
