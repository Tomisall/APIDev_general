import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = 'https://www.oxfordbus.co.uk/stops/3400030036'
fetch_time = datetime.now()
page = requests.get(URL)
update_time = fetch_time.strftime("%H:%M:%S")

print('\n' + '  ' + 'Updated:  ' + update_time, end="\n"*2) 
#print(page.text)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id='departure-board-wrapper')

#print(results.prettify())

job_elements = results.find_all("li", class_="departure-board__item")
#update_time = results.find_all("div", class_="single-stop__countdown__status")


topFive = job_elements[:4]

for job_element in topFive:
    #print(job_element.text.strip(), end="\n")
    name_element = job_element.find("p", class_="single-visit__name")
    time_element = job_element.find("div", class_="single-visit__time")


    print('\n' + '  ' + name_element.text.strip() + '    ' + time_element.text.strip(), end="\n"*2)


print('\n', end="\n")
