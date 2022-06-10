# import 1_get_rank
import seaborn
from bs4 import BeautifulSoup
import requests
from string import digits
import csv
import pandas as pd
from collections import OrderedDict
from operator import itemgetter

# make the info from each file into a dictionary


def get_dict(csv_title):
    with open(csv_title, "r") as csv:
        clean_csv = pd.read_csv(csv)
        # creates dictionary with 'National Park' and 'Rank' as keys
        csv_dict = clean_csv.to_dict('record')
        # print(csv_dict)
        # creates dict with park: rank
        clean_dict = {}
        for park in csv_dict:
            for key, val in park.items():
                clean_dict[park['National Park']] = park['Rank']
        return clean_dict


combined_dict = {}

farandwide = get_dict("farandwide.csv")
lee = get_dict("lee.csv")
outdoor_command = get_dict("outdoor_command.csv")
discoverer = get_dict("discoverer.csv")

list_of_dicts = [lee, outdoor_command, discoverer]
# uses farandwide to create the base to compare to
for key, val in farandwide.items():
    combined_dict[key] = val
# compares values in each csv file and takes the average
for blog in list_of_dicts:
    for key, val in blog.items():
        if combined_dict.get(key) == None:
            continue
        combined_dict[key] = (val + combined_dict[key])

ranked_dict = OrderedDict(sorted(combined_dict.items(), key=itemgetter(1)))
# print(ranked_dict)

complete_rank = "National Parks Complete Rank: "

count = 1
for park in ranked_dict:
    complete_rank += "\n" + str(count) + ". "
    complete_rank += park + " National Park "
    count += 1

print(complete_rank)


# Things to do:
# 1. Make the second half of this page into a function so that it isn't just floating in the program
# 2. make it so that I don't need a base rank to add to?
# 3. integrate it so that it prints in the same code file
# 4. see if there is a way to implement object oriented programming with it
