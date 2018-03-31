from bs4 import BeautifulSoup
import json, csv, os, requests
import sys, re


def scrapData(soup, htmlFile, outputFile): 

    fileType = outputFile.split('.')
    keys = ['name', 'date', 'rating type', 'long term', 'short term','outlook', 'action', 'press release', 'history', 'rating report']
    homepageURL = 'http://jcrvis.com.pk/'
    
    f = open("cleanData2", "w")
    for i in (soup.find_all('tbody', {'class':'row'})): 
        
        # 1st extract basic data
        for  j in i.find_all('tr', {'class':'data'} ):
            for k in j.find_all('td'):
                
                if k.get_text() == '\n': # introduce deliminator for every empty attribute
                    f.write('--1--') 
                else: 
                    f.write(k.get_text())
                f.write('\n')

        # now extract URLs of history, press release & rating report. 
        for j in i.find_all('tr', {'class':'files'}):
            for l in j.find_all('td'):
                
                for k in l.find_all('a', href =True):
            
                    if k != None: 
                        f.write(homepageURL +  k['href'])

                    f.write('\n') # remove null characters from each line. 

    f.close()

    # remove emplty spaces from file. 
    f2 = open('cleanData3', 'a+')
    count = 1 
    with open('cleanData2', 'r+') as f:
        for line in f:
           if line.strip():
            f2.write(line)

    f2.close() 
    f2 = open('cleanData3', 'r')

    with open('cleanData2', 'w') as f:
        for i in range(2):
            for line in f2:
                if len(line)>=52 and len(line)<=62:
                    f.write(line[0: len(line) - 4]) 
                else:
                    f.write(line)
        
    

    if fileType[1] == 'json':
        dumpJSON('cleanData2', keys, outputFile)
    elif fileType[1] == 'csv':
        dumpCSV('cleanData2', keys, outputFile)
    else:
        print('invalid file type! use json/csv file format.\n')

def dumpCSV(cleanData, keys, outputFile):

    f1 = open(cleanData, 'r')
    temp = f1.read().split('\n')
    count = 0 
    with open(outputFile, 'w') as f: 
        for i in keys:
            f.write(i)
            f.write(', ')
        f.write('\n')
        for line in temp:
            if count == 10:
                count = 0 
                f.write('\n')
            if line ==  '--1--':
                line = ' ' 
            else: 
                f.write(line)
                f.write(', ')
                count += 1
                


def dumpJSON(cleanData, keys, outputFile): 

    finallList = []
    dictionary = {}
    index = 0

    with open(cleanData, 'r') as f2: 
        for line in f2: 
            line = line.rstrip('\n')
            if index > 9: # after every 10th attribute, close the dict object & dump it in the list.  
                index = 0 
                finallList.append(dictionary)
                dictionary = {}

            if line ==  '--1--':
                line = ' ' 
                
            dictionary[keys[index]] = line
            index += 1

    # write the results in json file
    f = open(outputFile, 'w')
    f.write('[\n\t')
    for i in range(0, len(finallList)): 
        f.write( json.dumps(finallList[i],indent=4, sort_keys=True))
        if i != len(finallList) - 1:
            f.write(',\t')
        else: 
            break
    f.write('\n]')      

    


if __name__ == "__main__":

    URL = "http://jcrvis.com.pk/ratingSect.aspx"
    pageContent = requests.get(URL)
    soup = BeautifulSoup(pageContent.content, "html.parser")
    
    #extract the html content and dump in a file. 
    f = open('beautifiedPage.html', 'w+')
    f.write(soup.prettify())
    f.close()

    outputFileName = sys.argv[2:][0] # extract output file name.
    scrapData(soup, pageContent, outputFileName)
    

