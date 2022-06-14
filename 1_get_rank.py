from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
from collections import OrderedDict
from operator import itemgetter

list_nps_simplified = ['Yosemite', 'Canyonlands', 'Arches', 'Wrangell', 'Crater Lake', 'Grand Canyon', 'Zion', 'Gates of the Arctic',
                       'Dry Tortugas', 'Denali', 'Glacier', 'Yellowstone', 'Bryce Canyon', 'Katmai', 'Big Bend', 'Death Valley', 'Olympic',
                       'Grand Teton', 'Carlsbad Caverns', 'Mount Rainier', 'Rocky Mountain', 'Kobuk Valley', 'Capitol Reef', 'Acadia',
                       'Theodore Roosevelt', 'North Cascades', 'Badlands', 'Glacier Bay', 'Channel Islands', 'Black Canyon of the Gunnison',
                       'Lake Clark', 'Haleakal', 'Lassen Volcanic', 'Great Sand Dunes', 'Great Basin', 'Joshua Tree', 'Kings Canyon', 'Redwood',
                       'Volcanoes', 'Great Smoky Mountains', 'Kenai Fjords', 'White Sands', 'Mesa Verde', 'Everglades', 'Isle Royale', 'Virgin Islands',
                       'Saguaro', 'New River Gorge', 'Petrified Forest', 'Sequoia', 'Shenandoah', 'American Samoa', 'Guadalupe Mountains', 'Wind Cave',
                       'Voyageurs', 'Biscayne', 'Mammoth Cave', 'Gateway Arch', 'Congaree', 'Cuyahoga Valley', 'Pinnacles', 'Indiana Dunes', 'Hot Springs']

list_nps_standard = ['Yosemite', 'Canyonlands', 'Arches', 'Wrangell-St. Elias', 'Crater Lake', 'Grand Canyon', 'Zion', 'Gates of the Arctic',
                     'Dry Tortugas', 'Denali', 'Glacier', 'Yellowstone', 'Bryce Canyon', 'Katmai', 'Big Bend', 'Death Valley', 'Olympic',
                     'Grand Teton', 'Carlsbad Caverns', 'Mount Rainier', 'Rocky Mountain', 'Kobuk Valley', 'Capitol Reef', 'Acadia',
                     'Theodore Roosevelt', 'North Cascades', 'Badlands', 'Glacier Bay', 'Channel Islands', 'Black Canyon of the Gunnison',
                     'Lake Clark', 'Haleakala', 'Lassen Volcanic', 'Great Sand Dunes', 'Great Basin', 'Joshua Tree', 'Kings Canyon', 'Redwood',
                     'Hawaii Volcanoes', 'Great Smoky Mountains', 'Kenai Fjords', 'White Sands', 'Mesa Verde', 'Everglades', 'Isle Royale', 'Virgin Islands',
                     'Saguaro', 'New River Gorge', 'Petrified Forest', 'Sequoia', 'Shenandoah', 'American Samoa', 'Guadalupe Mountains', 'Wind Cave',
                     'Voyageurs', 'Biscayne', 'Mammoth Cave', 'Gateway Arch', 'Congaree', 'Cuyahoga Valley', 'Pinnacles', 'Indiana Dunes', 'Hot Springs']


class Blog_Rank:
    def __init__(self, url, tag_ref, csv_title):
        self.url = url
        self.tag_ref = tag_ref
        self.csv_title = csv_title

    def clean(self):
        """Webscrapes a blog and cleans the data to be uniform"""
        website = requests.get(self.url)
        soup = BeautifulSoup(website.content, "html.parser")
        heading_tags = soup.find_all(self.tag_ref)

        national_parks = [tag.get_text() for tag in heading_tags]
        # print(national_parks)

        """Removes any extra headings that aren't a national park"""
        # condition 1: the line has to begin with a number (rank)
        for park in national_parks:
            if park[0].isdigit() == False:
                national_parks.remove(park)
        # condition 2: sorts the parks in order from best to worst
        if national_parks[0][0] != "1":
            national_parks.reverse()

        """standardizes the list of national parks and resolves spelling variations"""
        # Compares the scraped lines with list_nps_simplified(line 8) to standardize format of the text
        cleaned_parks = []
        for park in national_parks:
            for item in list_nps_simplified:
                if item in park:
                    cleaned_parks.append(item)
        # solves issue of "Glacier" also being in "Glacier Bay"
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
        return cleaned_parks

    def get_dict(self):
        cleaned_dict = self.clean()
        """Creates a dictionary with rank: park name"""
        # creates a list numbered 1 through len(cleaned_parks)
        ranks = [i for i in range(1, (len(cleaned_dict) + 1))]
        # creates a dictionary with rank: park
        rank = 1
        dict_parks = {}
        for park in cleaned_dict:
            dict_parks[rank] = park
            rank += 1
        return dict_parks

    def create_csv(self):
        """creates a csv file with the clean rank"""
        cleaned_dict = self.clean()
        ranks = [i for i in range(1, (len(cleaned_dict) + 1))]
        # creates a dictionary to be turned into csv
        dict_parks = []
        for park in cleaned_dict:
            dict_parks.append({"National Park": park, "Rank": []})
        for rank in ranks:
            dict_parks[rank-1]["Rank"] = rank

        # creates a csv
        fields = ["National Park", "Rank"]
        with open(self.csv_title, 'w') as rank_csv:
            rank_writer = csv.DictWriter(rank_csv, fieldnames=fields)
            rank_writer.writeheader()
            for item in dict_parks:
                rank_writer.writerow(item)
            return f"Creating {self.csv_title}."


def get_average_rank(list_of_ranks):
    """takes as many ranks as you want and averages them out to get a clearer rank"""
    average = {}
    # creates the base for our comparison. average[park][0] = rank_total. average[park][1] = num of ranks that list that park
    for park in list_nps_standard:
        average[park] = [0, 0]
    # loops through blogs and adds the rank value to average
    for blog in list_of_ranks:
        for key, val in blog.items():
            if average.get(val) == None:
                continue
            average[val][0] = (key + average[val][0])
            # this step is so we can take the average later depending on how many ranks include the park
            average[val][1] += 1
    # takes the average
    for key, val in average.items():
        if val[1] == 0:
            average[key] = val[0]
        else:
            average[key] = val[0]/val[1]
    # sorts average by rank and prints it out in separate lines
    sorted_average = OrderedDict(sorted(average.items(), key=itemgetter(1)))
    complete_rank = "National Parks Complete Rank: "
    count = 1
    for park in sorted_average:
        complete_rank += "\n" + str(count) + ". "
        complete_rank += park + " National Park "
        count += 1
    return complete_rank

# Testing!!


# loops through list of blogs in np_blogs and creates an instance for each blog
with open("np_blogs.csv", "r") as np_blogs_csv:
    np_df = pd.read_csv(np_blogs_csv)
    np_dict = np_df.to_dict('records')

    ranks = []
    for row in np_dict:
        url = row["Url"]
        tag = row["Tag"]
        csv_title = row["CSV Name"] + ".csv"
        blog_instance = Blog_Rank(url, tag, csv_title)
        ranks.append(blog_instance.get_dict())
        print(blog_instance.get_dict())
        print(blog_instance.create_csv())
    print(get_average_rank(ranks))
