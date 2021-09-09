# web scraping

from bs4 import BeautifulSoup # virtual environment
import time
import csv
import requests # allows to request acces to info from website

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
get_link = requests.get(START_URL)
time.sleep(10)

headers = ["name", "distance", "mass", "radius"]
planet_data = []
new_planet_data = []

def scrape(): #planet_data contains planet NUMBER data (ex: weight of planet)
    for i in range(0, 100): 
        soup = BeautifulSoup(get_link.text, "html.parser") #creating virtual environment 
        temp_list = []
        for tr_tag in soup.find_all("tr"): #soup finds all "tr" as tr_tags
            td_tags = tr_tag.find_all("td") #tr_tag finds all "td" as td_tags 
            for td_tag in td_tags: #tr is table row, td is table data
                try:
                    temp_list.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0]) #appends all td_tags with "value" class (only first address)
                except: #exception for try
                    temp_list.append("")
        planet_data.append(temp_list)
    with open("scrapper_2.csv", "w") as f: #writing info into scraper_2.csv
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(planet_data)
def scrape_more_data(hyperlink): #data[5] #... #new_planet_data contains the planet names
    try: #used to make sure code runs no matter what the condition is
        page = requests.get(hyperlink) #gets hyperlink
        soup = BeautifulSoup(page.content,"html.passer") #creates virtual environment
        temp_list = []
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}): #finds all tr_tags and attributes with "fact_row" class
            td_tags = tr_tag.find_all("td") #tr_tag finds all "td" as td_tags 
            for td_tag in td_tags: #tr is table row, td is table data
                try:
                    temp_list.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0]) #appends all td_tags with "value" class (only first address)
                except: #exception for try
                    temp_list.append("")
        new_planet_data.append(temp_list) #appending entire temp_list to new_planet_data, so it contains the names
    except: #if try doesn't work, allows program to sleep
        time.sleep(1)
        scrape_more_data(hyperlink)

scrape()

for index,data in enumerate(planet_data): #takes numbers in planet_data and checks the index and data #enumerating is assigning the index value to the actual values
    scrape_more_data(data[5]) #the hyper_link in data, address 6 --> "scrape_more_data" function hyperlink #...
    print(f"{index+1} page done 2")
final_planet_data = [] 
for index,data in enumerate(planet_data): 
    new_planet_data_element = new_planet_data[index] #new_planet_data_element will hold the index value of new_planet_data
    new_planet_data_element = [elem.replace("\n","")for elem in new_planet_data_element] #new_planet_data_element will remove the "newline"(\n) and space
    new_planet_data_element = new_planet_data_element[:7] #seven values will show up on one page
    final_planet_data.append(data+new_planet_data_element) #appending data(index values) and new_planet_data_element(planet names) to final_planet_data
with open("final.csv", "w") as f: #writing all the info in final_planet_data 
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_planet_data)


