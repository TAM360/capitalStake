from bs4 import BeautifulSoup
import requests
import json, csv, sys, os
  
def scrapData(soup, pageContent, outputFileName): 
    homepage = 'http://www.pacra.com.pk'
    keys  = [
        "id", "name", "sector", "ratingtype","date", "lt_rating", "st_rating",
        "action", "outlook", "press_link", "report_link", "histor_link"
        ]

    f = open('cleanData1', 'w')
    # dump the cleaned data in cleanData1 text file.
    for i in (soup.find_all('tr', {"align": "left", "style":"font-size:12px"})):
        for j in (i.find_all("td")):
            
            k = j.find('a', href=True)
            if k != None:
                x = k.get("href") # extract reports, summaries & press release links. 
                f.write(homepage + x[3:]) # strip off "/.." from the link and concatenate homepage's link. 
            else: 
                f.write(j.get_text()),    
            f.write('\n')

    f.close()
    fileName = sys.argv[2:]
    fileName = fileName[0].split(".")

    if fileName[1] == 'json': 
        dumpJSON('cleanData1', keys, sys.argv[2])

    elif fileName[1] == 'csv':
        dumpCSV('cleanData1', keys, sys.argv[2])



def dumpJSON(cleanData, keys, outputFile): 
    # for writing in json file. 
    array = []
    count = 0
    with open(cleanData, "r") as f:
        dictionary = {}
        for line in f: 
                line = line.rstrip('\n') # remove 'n\' from each line of text file. 
                if count== 12: # after every 12th iteration , 1 dictionary object gets finished completely.
                    count = 0
                    # 2 attributes aren't required for the assignment. 
                    dictionary.pop("id", None) 
                    dictionary.pop("ratingtype", None)
                    
                    array.append(dictionary)
                    dictionary = {} # reuse the dictionary object. 
                
                dictionary[keys[count]] = line
                count +=1 

    f2 = open(sys.argv[2:][0], "w")
    f2.write('[\n\t')
    for i in range(0, len(array)):
        f2.write(json.dumps(array[i], indent=4))
        if i != len(array) -1:
            f2.write(',\t')

    f2.write("\n\t]")
    f2.close() 
    
def dumpCSV(cleanData, keys, outputFile): 
     
    f1 = open(cleanData, 'r')
    temp = f1.read().split('\n')
    count = 0 
    
    with open(outputFile, 'w') as f: 
        
        for i in keys:
            if i != 'id' and i != 'ratingType': 
                f.write(i)
                f.write(', ')
        f.write('\n')
        
        for line in temp:
            if count == 12:
                count = 0 
                f.write('\n')
           
            else: 
                if count != 0 and count != 3: # no need for id & ratingType attributes. 
                    line = line.rstrip('\n')
                    f.write(line)
                    f.write(', ')
                count += 1

# main program. 
if __name__ == '__main__':
    
    URL = 'http://www.pacra.com.pk/reports.php'
    page1 = requests.get(URL)
    soup = BeautifulSoup(page1.content, 'html.parser')
    
    f = open("beautifiedPage.html", "w+")
    f.write(soup.prettify())
    f.close()

    outputFileName = sys.argv[2:][0] 
    scrapData(soup, page1, outputFileName)
   