import seaborn
from bs4 import BeautifulSoup
import requests
from string import digits
import csv
import pandas as pd

list_nps = ['Yosemite', 'Canyonlands', 'Arches', 'Wrangell', 'Crater Lake', 'Grand Canyon', 'Zion', 'Gates of the Arctic', 'Dry Tortugas', 'Denali', 'Glacier', 'Yellowstone', 'Bryce Canyon', 'Katmai', 'Big Bend', 'Death Valley', 'Olympic', 'Grand Teton', 'Carlsbad Caverns', 'Mount Rainier', 'Rocky Mountain', 'Kobuk Valley', 'Capitol Reef', 'Acadia', 'Theodore Roosevelt', 'North Cascades', 'Badlands', 'Glacier Bay', 'Channel Islands', 'Black Canyon of the Gunnison', 'Lake Clark', 'Haleakal',
            'Lassen Volcanic', 'Great Sand Dunes', 'Great Basin', 'Joshua Tree', 'Kings Canyon', 'Redwood', 'Volcanoes', 'Great Smoky Mountains', 'Kenai Fjords', 'White Sands', 'Mesa Verde', 'Everglades', 'Isle Royale', 'Virgin Islands', 'Saguaro', 'New River Gorge', 'Petrified Forest', 'Sequoia', 'Shenandoah', 'American Samoa', 'Guadalupe Mountains', 'Wind Cave', 'Voyageurs', 'Biscayne', 'Mammoth Cave', 'Gateway Arch', 'Congaree', 'Cuyahoga Valley', 'Pinnacles', 'Indiana Dunes', 'Hot Springs']

# converts 1np_blogs.csv to a dictionary
with open("np_blogs.csv") as np_blogs_csv:
    np_df = pd.read_csv(np_blogs_csv)
    np_dict = np_df.to_dict('record')
    # print(np_dict)

# rewrite of get_np_list


def get_np_list_2(url, tag_ref, csv_title):
    """Takes the URL and HTML Tag of the list being pulled from. Adds just the list of National Parks to a list."""
    website = requests.get(url)
    soup = BeautifulSoup(website.content, "html.parser")
    heading_tags = soup.find_all(tag_ref)
    # print(heading_tags)
    national_parks = []
    for tag in heading_tags:
        national_parks.append(tag.get_text())
    # print(national_parks)
    # removes headings that aren't a ranked park
    for park in national_parks:
        if park[0].isdigit() == False:
            national_parks.remove(park)
    # print(national_parks)
    # sorts the parks in order from best to worst
    if national_parks[0][0] != "1":
        national_parks.reverse()
    # print(national_parks)
    cleaned_parks = []
    for park in national_parks:
        for item in list_nps:
            if item in park:
                cleaned_parks.append(item)
    # remove extra "Glacier" entry that happens because "Glacier" is also in "Glacier Bay"
    if "Glacier Bay" in cleaned_parks:
        index_glacierbay = cleaned_parks.index("Glacier Bay")
        index_glacier1 = [i for i, n in enumerate(
            cleaned_parks) if n == 'Glacier'][0]
        index_glacier2 = [i for i, n in enumerate(
            cleaned_parks) if n == 'Glacier'][1]
        if index_glacier1 == index_glacierbay - 1:
            del cleaned_parks[index_glacier1]
        if index_glacier2 == index_glacierbay - 1:
            del cleaned_parks[index_glacier2]
    # print(cleaned_parks)
    # next 3 loops account for common misspellings/punctuation differences
    for item, park in enumerate(cleaned_parks):
        if park == 'Wrangell':
            cleaned_parks[item] = 'Wrangell-St. Elias'
    for item, park in enumerate(cleaned_parks):
        if park == 'Volcanoes':
            cleaned_parks[item] = 'Hawaii Volcanoes'
    for item, park in enumerate(cleaned_parks):
        if park == 'Haleakal':
            cleaned_parks[item] = 'Haleakala'
    # print(cleaned_parks)
    # creates a list numbered 1 through len(cleaned_parks)
    ranks = []
    for i in range(1, (len(cleaned_parks) + 1)):
        ranks.append(i)
    # print(ranks)
    # creates a dictionary with national park, rank
    dict_parks = []
    for park in cleaned_parks:
        dict_parks.append({"National Park": park, "Rank": []})
    for rank in ranks:
        dict_parks[rank-1]["Rank"] = rank
    # print(dict_parks)
    # creates csv file
    fields = ["National Park", "Rank"]
    with open(csv_title, 'w') as rank_csv:
        rank_writer = csv.DictWriter(rank_csv, fieldnames=fields)
        rank_writer.writeheader()
        for item in dict_parks:
            rank_writer.writerow(item)
    print("The file " + csv_title + " has been created.")


# loops through rows in np_dict
for row in np_dict:
    url = row["Url"]
    tag = row["Tag"]
    csv_title = row["CSV Name"]
    get_np_list_2(url, tag, csv_title)
