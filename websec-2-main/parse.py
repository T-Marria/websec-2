import requests
from bs4 import BeautifulSoup as BS
import json


def GetCurrentWeek():
    webPage = requests.get("https://ssau.ru/rasp?groupId=531030143")
    html = BS(webPage.content, 'html.parser')
    info = html.select(".week-nav-current > .week-nav-current_week")
    return int(''.join(c for c in info[0].text if c.isdigit()))


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
        teachers = html.select(".list-group > li > a")
        for teacher in teachers:
            staffId = ''.join(c for c in teacher['href'] if c.isdigit())
            teachersInfo[teacher.text[1:-1]] = f"https://ssau.ru/rasp?staffId={staffId}"

        if(len(teachers) == 0):
            break
        page += 1
        print(f"{page} страниц из 118 обработано", end="\r")

    with open("TeachersInfo.json", "w") as file:
        json.dump(teachersInfo, file, separators=(',\n', ': '), ensure_ascii=False)


def GetGroupSchedule(groupNumber: str = "6411-100503D", week: int = GetCurrentWeek()):
    schedule = {
        "Mon": [],
        "Tue": [],
        "Wed": [],
        "Thu": [],
        "Fri": [],
        "Sat": [],
        "Sun": []
    }

    with open("GroupsInfo.json", "r") as file:
        groupsInfo = json.load(file)

    webPage = requests.get(f"https://ssau.ru{groupsInfo[groupNumber]}&selectedWeek={week}")
    html = BS(webPage.content, 'html.parser')
    sch_items = html.select(".schedule__items > .schedule__item")
    for item in sch_items:
        print(item)
        print()

GetGroupSchedule("6411-100503D")






# ParseGroups()
# ParseTeachers()