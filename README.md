# U.S. National Parks Ultimate Rank

Web-scraping tool to clean and create the “Ultimate U.S. National Parks Rank” of all 63 national parks.

## What does this project do?

1.	Web-scrapes U.S. national park rankings from various travel-blogger websites.
2.	Cleans the data for accurate comparison of rankings between blogs.
3.	Merges the different rankings from each blog to create a complete rank for all 63 U.S. national parks.

## Why did I create this project?
My main goal for this project was simply to practice. As a newbie self-taught programmer, I wanted to challenge what I’ve been learning on Codecademy and apply it to something I am super passionate about. Through this project I practiced basic Python 3 syntax, web-scraping with BeautifulSoup, data cleaning, object-oriented programming, and file management.

I LOVE the outdoors. In 2021 I visited 10 National Parks, including some of the most popular and least popular in the U.S. I have a goal to visit all 63 parks in my lifetime, and I wanted a way to decide where to start to make sure I hit the best parks while I am still young and can do the difficult hikes. I noticed there are MANY bloggers who have created their own rank of best to worst national parks. This program combines those lists into one ultimate rank of U.S. National Parks.

## How do you use this project?
### Requirements
The following packages are needed to run this program:
- BeautifulSoup
- Requests
- Pandas

They are not included in the main python library.

**To install these packages,** run the command: ‘pip install -r requirements.txt’

### Running the Program
The program is found in [national_parks.py](https://github.com/jac-davis/national-parks/blob/main/national_parks.py)

The inputs for each function are in [np_blogs.csv](https://github.com/jac-davis/national-parks/blob/main/np_blogs.csv)

**Option 1 (easiest way):** The program automatically loops through [np_blogs.csv](https://github.com/jac-davis/national-parks/blob/main/np_blogs.csv) (lines 151-165) and completes the following: 
1. Prints a dictionary of a cleaned rank for each blog
2. Creates a CSV file of a cleaned rank for each blog
3. Prints a combined ultimate rank using each blog

To use this option: **add a blog to a new line [np_blogs.csv](https://github.com/jac-davis/national-parks/blob/main/np_blogs.csv).** Four examples have already been added to the file. To add a blog, you will need the following information:
- Column 1: Website/Blog Name
- Column 2: Url (in double quotes)
- Column 3: HTML tag from the blog that contains the list of national parks (in double quotes)
- Column 4: One-word nickname for the website (in double quotes). No spaces are allowed, so either delete the spaces or use underscores in place of them.

**Option 2 (manual way):** 
Manually create an instance of the Blog_Rank class for the blog you want to clean and save the instance to a new variable. From here, you can apply the Blog_Rank class methods.

The get_average_rank function takes a list of cleaned dictionaries as an input. To use this function in option 2, run the .get_dict() method on your blog instance from Blog_Rank. Then, .append() each instance you want to use in your ultimate rank to a new list. The new list will be the input for your function.

## Main Learning Take-aways:
1. ***Creating projects you are passionate about makes programming so much more enjoyable.*** Right after I came up with this project idea, I spent 5 hours straight on a Saturday working on this project. Time flew by and I knew programming was something I could continue learning for the long-haul.
2. ***You don’t have to know everything.*** I came up with this web-scraping project before I even knew how to web-scrape or even access the HTML tags on a webpage. I learned how web-scraping worked in an afternoon from Codecademy and lots of Google searches/Youtube videos. I learned more by tackling a project I wasn’t sure I could complete rather than sticking with something simple that didn’t challenge me.
3. ***Be proud of what you’ve created, even if it isn’t perfect.*** This program is simple and still flawed, but it is in the possibilities of what functionality can be added in the future where growth and learning will continue

![IMG_0147](https://user-images.githubusercontent.com/104480294/173732762-69a06290-c162-4626-b10e-e34a59fe3094.jpeg)

