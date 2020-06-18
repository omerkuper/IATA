import time
from datetime import date, timedelta

YesNo = {'y': 'true', 'n': 'false'}

start = ['LHR',  'AMS']
end = ['tlv']
date_i = [200901, 230909]
stay_in = [10]
loop = 10
run_loop  = 2
direct_flight = 'y'


def index_counting(counter_out, destination=None):
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
    return [dates, staying]


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

    elif route == 'EverywhereRoundTrip':
      departure, date_return_i, date_return_q = args[1], args[2], args[3]
      url_sky = f'https://www.skyscanner.co.il/transport/flights-from/{departure}/{date_return_i}/{date_return_q}/?adultsv2=1&cabinclass=economy&childrenv2=&inboundaltsenabled=false&outboundaltsenabled=false&preferdirects=false&rtn=1'
      return url_sky

    elif route == 'EverywhereOneWay':
      departure, date_return_i = args[1], args[2]
      # print(departure, date_return_i)
      url_sky = f'https://www.skyscanner.co.il/transport/flights-from/{departure}/{date_return_i}/?adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=0&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&ref=home'
      return url_sky


    elif route == 'MultiCity':
        stay_long, date_return_i = args[1], args[2]
        url_sky = f'https://www.skyscanner.net/transport/flights/{start[stay_long]}/{end[stay_long]}/{date_return_i}?flexible_origin=true&flexible_depart=direct&flexible_return=direct&adults=1&children=0&adultsv2=1&childrenv2=&infants=0&cabinclass=economy&rtn=0&preferdirects={YesNo[direct_flight]}&outboundaltsenabled=false&inboundaltsenabled=false&ref=home&currency=USD#results'
        url_jet = f'https://search.jetradar.com/flights?marker=google&origin_iata={start[stay_long].upper()}&destination_iata={end[stay_long].upper()}&depart_date={date_return_i}&with_request=true&adults=1&children=0&infants=0&trip_class=0&locale=en&one_way=false&ct_guests=1+passenger&ct_rooms=1'
        url_mom = f'https://www.momondo.com/flight-search/{start[stay_long].upper()}-{end[stay_long].upper()}/{date_return_i}?sort=bestflight_a'
    return url_sky, url_jet, url_mom


def date_returns(*args):
    route = args[0]
    add_day = args[1]
    if route != 'MultiCity':
      index_dates = args[2]
      main_date = time.strptime(str(date_i[index_dates]), '%y%m%d')
      sub_date = date(main_date.tm_year, main_date.tm_mon,
                            main_date.tm_mday) + timedelta(add_day)
      try:
        how_long_saty = args[3]
        run = args[4]
        sec_sub_date = date(main_date.tm_year, main_date.tm_mon,
                                      main_date.tm_mday) + timedelta(add_day + stay_in[how_long_saty] + run)
        return sub_date, sec_sub_date
      except:
        return sub_date
    else:
      adding = args[2]
      main_date = time.strptime(str(date_i[0]), '%y%m%d')
      sub_date = date(main_date.tm_year, main_date.tm_mon,
                                 main_date.tm_mday) + timedelta(add_day + adding)
      return sub_date


def OneWay(route='OneWay'): 
    lst = []
    for departure in range(len(start)):
        for destination in range(len(end)):
            for counter in range(loop):
                dates = index_counting(destination, destination)
                try:
                    trip_date = date_returns(route, counter, dates[0])
                    url = urls(route, start[departure], destination, trip_date)
                    lst.append(url)
                except:
                    pass
    return lst


def RoundTrip(lst =[], route='RoundTrip'):
    datesq = [index_counting(departure, destination) + [counter, run, departure, destination] for 
    departure in range(len(start)) for destination in range(len(end)) for run in range(run_loop) for counter in range(loop)]
    for dates in datesq:           
      try:
          #  trip_date = date_returns(route, counter, dates[0], dates[1], run)
#                     url = urls(route, start[departure], destination, trip_date[0], trip_date[1])
          trip_date = date_returns(route, dates[2], dates[0], dates[1], dates[3])
          print(trip_date)
          url = urls(route, start[dates[4]], dates[5], trip_date[0], trip_date[1])
          lst.append(url)
      except:
          pass
    return lst


# def RoundTrip(lst =[], route='RoundTrip'):
#     for departure in range(len(start)):
#         for destination in range(len(end)):
#           for run in range(run_loop):
#             for counter in range(loop):
#                 dates = index_counting(departure, destination)
#                 try:
#                     trip_date = date_returns(route, counter, dates[0], dates[1], run)
#                     url = urls(route, start[departure], destination, trip_date[0], trip_date[1])
#                     lst.append(url)
#                 except:
#                     pass
#     return lst


def MultiCity(route='MultiCity'):
    lst = []
    counter_days = 0
    stay = [0] + stay_in
    for stay_long in range(len(stay)):
        for adding in range(loop):
            trip_date = date_returns(route, counter_days, adding)
            url = urls(route, stay_long, trip_date)
            lst.append(url)
        try:
            counter_days += stay[stay_long + 1]
        except:
            pass
    return lst



def Everywhere(run=0, lst =[]):
    if len(stay_in) != 0:
      route = 'EverywhereRoundTrip'
    else:
      route = 'EverywhereOneWay'
    if route == 'EverywhereRoundTrip':
      for departure in range(len(start)):
        for run in range(run_loop):
            for counter in range(loop):
                dates = index_counting(departure, departure)
                try:
                    trip_date = date_returns(route, counter, dates[0], dates[1], run)
                    # print(start[departure], trip_date[0], trip_date[1])
                    url = urls(route, start[departure], trip_date[0], trip_date[1])
                    lst.append(url)
                except:
                    pass
      return lst
    else:
      for departure in range(len(start)):
        for counter in range(loop):
            dates = index_counting(departure, departure)
            try:
              trip_date = date_returns(route, counter, dates[0])
              url = urls(route, start[departure], trip_date)
              lst.append(url)
            except:
                pass
      return lst



for u in RoundTrip():
    print(u)
