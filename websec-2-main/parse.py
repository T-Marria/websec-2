import requests
from bs4 import BeautifulSoup as BS
import json

def ParseGroups():
    groupsInfo = {}
    for course in range(1, 6):
        webPage = requests.get(f"https://ssau.ru/rasp/faculty/492430598?course={course}")
        html = BS(webPage.content, 'html.parser')

        for group in html.select(".group-catalog__groups > a"):
            groupsInfo[group.text[1:-1]] = group['href']
    
    with open("GroupsInfo.json", "w") as file:
        json.dump(groupsInfo, file, separators=(',\n', ': '))

def ParseTeachers():
    teachersInfo = {}
    page = 1
    while True:
        webPage = requests.get(f"https://www.ssau.ru/staff?page={page}")
        html = BS(webPage.content, 'html.parser')
        items = html.select(".list-group > li > a")
        for item in items:
            staffId = ''.join(c for c in item['href'] if c.isdigit())
            # print(f"{item.text[:-1]}: {staffId}")
            teachersInfo[item.text[1:-1]] = f"https://ssau.ru/rasp?staffId={staffId}"

        if(len(items) == 0):
            break
        page += 1
        print(f"{page} страниц из 118 обработано", end="\r")

    with open("TeachersInfo.json", "w") as file:
        json.dump(teachersInfo, file, separators=(',\n', ': '), ensure_ascii=False)




# ParseGroups()
ParseTeachers()