from bs4 import BeautifulSoup
import requests
import json, csv
  
keys  = [
    "id", "name", "sector", "ratingtype","date", "lt_rating", "st_rating",
    "action", "outlook", "press_link", "report_link", "histor_link"
    ]
list1 = []
count = 0

URL = 'http://www.pacra.com.pk/reports.php'
homepage = 'http://www.pacra.com.pk'
page1 = requests.get(URL)
soup = BeautifulSoup(page1.content, 'html.parser')
f = open("beautifiedPage.html", "w+")
f.write(soup.prettify())
f.close()

# dump the cleaned data in cleanData1 text file.
for i in (soup.find_all('tr', {"align": "left", "style":"font-size:12px"})):
    for j in (i.find_all("td")):
        
        k = j.find('a', href=True)
        if k != None:
            x = k.get("href") # extract reports, summaries & press release links. 
            print(homepage + x[3:]) # strip off "/.." from the link and concatenate homepage's link. 
        else: 
            print(j.get_text()),    

f2 = open('out.json', "w+")
f2.write("[\n\t")

# for writing in json file. 
with open("cleanData1", "r") as f:
    dictionary = {}
    for line in f: 
        line = line.rstrip('\n') # remove 'n\' from each line of text file. 
        if count== 12: # after every 12th iteration , 1 dictionary object gets finished completely.
            count = 0
            # 2 attributes aren't required for the assignment. 
            dictionary.pop("id", None) 
            dictionary.pop("ratingtype", None)
            
            f2.write(json.dumps(dictionary, indent=4))
            if line !=None:
                f2.write(',\n')
            dictionary = {} # reuse the dictionary object. 
         
        dictionary[keys[count]] = line
        count +=1 

f2.write("\n\t]")
f2.close() 

# for writing in csv file
f3 = open('out.csv', 'a')       
