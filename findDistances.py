from bs4 import BeautifulSoup
import requests
import os
import json

letters = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12,
           'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24,
           'Z': 25}
look = {}

class FindMeHub:
    def __init__(self):
        self.lst_set = set()

    def saveDataToTxt(self, data_list):
        directory = "/home/omer/Skyscanner/skyscanner/savingFiles/DistancesHub"
        myFile = open(os.path.join(directory, 'Distances Between 2 Points.txt'), 'a', newline='')
        with myFile as output:
            output.write(f"{str(data_list)}\n")

    def findMeDestination(self, airport_name):  # into TLV
        lst_of_points = []
        dict_destination_out = {}
        for index in range(len(airport_name)):
            dict_destination_in = {}
            web = requests.get(f"https://www.flightsfrom.com/{airport_name[index].upper()}/destinations")
            url = web.content
            soup = BeautifulSoup(url, "html.parser")
            everywhere_i = soup.find_all("span",
                                         class_="airport-font-midheader destination-search-item")  # destinations
            for place in everywhere_i:
                dict_destination_in[place.text[-3:]] = place.text[: -5]
            dict_destination_out[airport_name[index].upper()] = dict_destination_in
        lst_of_points.append(dict_destination_out)
        print(lst_of_points)
        self.saveDataToTxt(lst_of_points)
        return dict_destination_out

    def find_hubs(self, first, arrive, keys, values, start_second):
        for end_point, mid_point in arrive.items():
            if keys in mid_point and start_second not in self.lst_set and first != '':
                self.distances([first, start_second, keys, end_point])

                self.lst_set.add(start_second)
            elif keys == end_point and start_second not in self.lst_set:
                self.distances([start_second, keys])

                self.lst_set.add(start_second)
            elif keys in mid_point and first == '':
                self.distances([start_second, keys, end_point])

    def lets_start_find_hubs(self, start, departures, arrive):
        for start_point, value in departures.items():
            for keys, values in value.items():
                self.find_hubs(start, arrive, keys, values, start_point)

    def lets_start_find(self, starting_point):
        first_hub = []
        for start_point, value in starting_point.items():
            for keys, values in value.items():
                first_hub.append(keys)
        return first_hub

    def find_country(self, iata_code):
        country_dict = {}
        for iata in iata_code:
            with open("IATA CODE.json", "r") as read_file:
                data = json.load(read_file)
                country = data[letters[iata[0]]][iata][-1].strip()
                if country[0] not in letters.keys():
                    country_dict[iata] = country[1:].strip()
                else:
                    country_dict[iata] = country
        return country_dict

    def send_iata_code(self, iata_code):
        lst = [key for code in iata_code for key in code]
        return self.find_country(lst)

    def fast_route(self, starting_point, end_point):
        departures = self.findMeDestination(starting_point)
        arrive = self.findMeDestination(end_point)
        self.lets_start_find_hubs('', departures, arrive)

    def look_for_iata_code(self, dicts):
        # lst_iata = {k: v for k, v in dicts.items() if v in look}
        lst_iata = {k: v for k, v in dicts.items()}
        return lst_iata

    def slower_route(self, starting_point, end_point):
        self.key_point = ''
        self.lst_set.clear()
        lets_go = {}
        starting_point = self.findMeDestination(starting_point)
        for key in starting_point:
            self.key_point = key
            lets_go[key] = self.look_for_iata_code(self.send_iata_code(starting_point.values()))
        departures = self.findMeDestination(self.lets_start_find(lets_go))
        arrive = self.findMeDestination(end_point)
        self.lets_start_find_hubs(self.key_point, departures, arrive)

    def distances(self, airport_name):  # into TLV
        airportA = airport_name[0].upper()
        airportB = airport_name[1].upper()

        if len(airport_name) == 2:
            web = requests.get(
                f"https://www.greatcirclemapper.net/en/great-circle-mapper.html?route={airportA}-{airportB}&aircraft=&speed=")

        elif len(airport_name) == 3:
            airportC = airport_name[2].upper()
            web = requests.get(
                f"https://www.greatcirclemapper.net/en/great-circle-mapper.html?route={airportA}-{airportB}-{airportC}&aircraft=&speed=")

        elif len(airport_name) == 4:
            airportC = airport_name[2].upper()
            airportD = airport_name[3].upper()
            web = requests.get(
                f"https://www.greatcirclemapper.net/en/great-circle-mapper.html?route={airportA}-{airportB}-{airportC}-{airportD}&aircraft=&speed=")

        url = web.content
        soup = BeautifulSoup(url, "html.parser")
        everywhere_i = soup.find_all("div", class_="item total clearfix")  # destinations
        distances = everywhere_i[0].td.text
        clean_distances = distances.split(",")
        final_distances = clean_distances[1].strip()

        if len(airport_name) == 2:
            print(f"Distances from {airportA} to {airportB} is : {final_distances} *")

        elif len(airport_name) == 3:
            airportC = airport_name[2].upper()
            print(f"Distances from {airportA} through {airportB} to {airportC} is : {final_distances}")

        elif len(airport_name) == 4:
            airportC = airport_name[2].upper()
            airportD = airport_name[3].upper()
            print(
                f"Distances from {airportA} through {airportB} through {airportC} to {airportD} is : {final_distances}")


run = FindMeHub()

start = ["tlv"]
end = ["mel", 'syd']

for i in start:
    run.fast_route([i], end)
    print(f"\n{'*' * 150}")


