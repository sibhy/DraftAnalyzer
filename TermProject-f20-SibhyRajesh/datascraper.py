## Sibhy Rajesh
## Term Project 15-112
## This file web scrapes the data to be used in later parts of the project.

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pandas as pd
import numpy as np

# labeled lines are from:
# https://towardsdatascience.com/scraping-nfl-stats-to-compare-quarterback-efficiencies-4989642e02fe
# they have the comment 'from source' next to them

# all data scraped from: 
# https://www.pro-football-reference.com/


# does the actual web scraping and custom parsing
# can save to csv if requested(if save is True)
def initializeMetrics(year, metric, save):
    
    if invalidMetric(metric):
        return None
    
    if invalidMetricYear(year):
        return None

    currUrl = f'https://www.pro-football-reference.com/years/{year}/{metric}.htm'

    html = urlopen(currUrl)  # from source
    statPageHtml = bs(html, 'lxml')  # from source

    statRows = statPageHtml.findAll('tr')[1:] # from source

    currStats = []
    for i in range(len(statRows)): # from source
        currStats.append([col.getText() for col in statRows[i].findAll('td')]) # from source
    
    headers = statPageHtml.findAll('tr')[0] # from source

    headersText = doubleHeadersCheck(headers, currStats, statPageHtml) # my fn

    headersText = renameHeaders(headersText) # my function to rename headers
 
    removeEmptys(currStats) # my function to remove empty rows

    data = pd.DataFrame(currStats, columns = headersText[1:]) # from source 

    newData = cleanUpNames(data)  # my function to remove asterisks and plus signs

    if save:
        newData.to_csv(f"{year}-{metric}-Data.csv")

    ######################
    # TECH DEMO EXAMPLES #
    ######################
    
     # print(testarray.shape) # numpy tech demo tests
    # print(testarray[0])
    # print(testarray.sum(1))
    # print(testarray[testarray["TD"] > 10])

    # print(data.head()) # prints first 5 rows

    # print(data.iloc[3]) # print the third row of our dataframe

    # print(data.loc[(data["Tm"] == "ATL")]) # locate players for Tampa Bay

    # print(data.groupby(["Int"]).first()) # grouping options for diff cats.
        
    # fpts = data["TD"].astype(np.float) # need to convert numpy values into np.float

    # print(fpts.apply(np.sum)) # here we can sum 

    # numpyData = np.array(data)
    # print(numpyData.shape)
    # print(numpyData.size)
    # print(numpyData.dtype)
    # print(numpyData[1, :])


# helper functions primarily for parsing 

def removeEmptys(currStats):
    for row in currStats:
        if row == []:
            currStats.remove(row)

def initializeHeaders(headers):
    headersText = [i.getText() for i in headers.findAll('th')] # from source
    return headersText

def doubleHeadersCheck(headers, currStats, statPageHtml):
    i = 0
    headersText = initializeHeaders(headers)

    while len(headersText) - 1 != len(currStats[1]):
            headers = statPageHtml.findAll('tr')[i]
            headersText = initializeHeaders(headers)
            i += 1

    return headersText
            
def cleanUpNames(data):
    for i in range(len(data)):
        oldName = data.iloc[i, 0]
        newName = oldName
        asteriskIndex = oldName.find('*')
        plusIndex = oldName.find('+')

        if plusIndex != -1:
            newName = oldName[:plusIndex]

        if asteriskIndex != -1:
            newName = oldName[:asteriskIndex]

        if newName != oldName:   
            data['Player'] = data['Player'].replace([oldName], newName)
            # this line using '.replace' is from:
            # https://datatofish.com/replace-values-pandas-dataframe
    
    newData = data.set_index("Player", drop = True)
    return newData

# built to rename headers of data scraped from fantasy 2019, as this is our main
# data used. yds and tds are used in multiple instances, so need to rename them.
def renameHeaders(headersText): 
    rAttIndex = 12
    rYdsIndex = 13
    rTdsIndex = 15
    recYdsIndex = 18
    recTdsIndex = 20
    allTdsIndex = 23
    headersText[rAttIndex] = "rushAtt" # rushing attempts
    headersText[rYdsIndex] = "rushYds" # rush yds
    headersText[rTdsIndex] = "rushTds" # rush tds
    headersText[recYdsIndex] = "recYds" # receiving yards
    headersText[recTdsIndex] = "recTds" # receiving tds
    headersText[allTdsIndex] = "allTds" # all tds

    return headersText


# checks if the entered metric is valid
def invalidMetric(metric): 
    return (metric not in ["passing" , "rushing", "receiving", "defense", "kicking",
 "returns", "scoring", "fantasy"])

# checks if the entered year is valid
def invalidMetricYear(year):
    return (not isinstance(year, int) or year < 1920 or year > 2020)


