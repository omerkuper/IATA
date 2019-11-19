from bs4 import BeautifulSoup
import requests
import json


def findMeDestination(letter):

    lst = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'}
    web = requests.get(f"https://en.wikipedia.org/wiki/List_of_airports_by_IATA_code:_{letter.upper()}")
    url = web.content
    soup = BeautifulSoup(url, "html.parser")
    everywhere_i = soup.find_all("td")  # destinations
    short_iata_code = [place.text.strip('\n') for place in everywhere_i]
    if letter.upper() not in lst:
        short_iata_list = list(zip(short_iata_code[:-5:4], short_iata_code[3:-5:4]))
    else:
        short_iata_list = list(zip(short_iata_code[:-5:6], short_iata_code[3:-5:6]))
    return short_iata_list




def create_dict_of_iata_code(letter):
    iata_code_dict = {}
    for tuple_codes in findMeDestination(letter):
        country_name = tuple_codes[1].split(",")
        iata_code_dict[tuple_codes[0][: 3]] = country_name
    with open("IATA CODE.txt", "a") as write_file:
        json.dump(iata_code_dict, write_file)
    return iata_code_dict





# let = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
#
# for l in let:
#     print(create_dict_of_iata_code(l))
#
#
#
#
#
