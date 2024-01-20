import requests
from bs4 import BeautifulSoup as BS
import json

def ParseFaculties():
    page = requests.get("https://ssau.ru/rasp")
    html = BS(page.content, 'html.parser')

    for element in html.select(".faculties > .faculties__item"):
        faculty = element.select('a')
        print(faculty[0].text)

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
        items = html.select(".list-group > li")
        print(items)
        # for item in items:
            

        if(len(items) == 0):
            break

        print("____________END OF PAGE________________________________________________")
        page += 1




# ParseFaculties()
ParseGroups()
# ParseTeachers()