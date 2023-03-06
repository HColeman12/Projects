
'''

This Python program scrapes unemployment data from the Bureau of Labor Statitics and writes SQL code to
update the database for my Open Curator website.

'''

from bs4 import BeautifulSoup
import requests
from datetime import datetime

currentMonth = datetime.now().month
currentYear = datetime.now().year


source = requests.get('https://data.bls.gov/timeseries/LNS14000000').text

soup = BeautifulSoup(source, 'lxml')

the_table = soup.find('table', id='table0')

rows = the_table.findChildren(['tr'])


for row in rows:
    cells = row.findChildren('th')
    for cell in cells:
        if (cell.string == str(currentYear)):
            tds = row.findChildren('td')
            cur_month = tds[currentMonth -1].text
            if currentMonth != 1:
                prev_month = tds[currentMonth - 2].text
                

if currentMonth == 1:
    lastYear = currentYear - 1
    for row in rows:
        cells = row.findChildren('th')
        for cell in cells:
            if cell.string == str(lastYear):
                tds = row.findChildren('td')
                prev_month = tds[11].text


if currentMonth == 1:
    last_Month = 12
else:
    last_Month = currentMonth - 1
    
table_date_1 = str(currentMonth) + str(currentYear)
if currentMonth == 1:
    table_date_2 = str(last_Month) + str(currentYear - 1)
else:
    table_date_2 = str(last_Month) + str(currentYear)

with open("update_project.txt", "w") as f:
    if cur_month and cur_month.strip():
        f.write(f"UPDATE OC1B SET {table_date_1} = {cur_month} where table_id = 6 and geo = \"united states\";\n")
    f.write(f"UPDATE OC1B SET {table_date_2} = {prev_month} where table_id = 6 and geo = \"united states\";")

    
                    

            
            


