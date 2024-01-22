import requests
from bs4 import BeautifulSoup as BS
import json


def GetCurrentWeek() -> int:
    webPage = requests.get("https://ssau.ru/rasp?groupId=531030143")
    html = BS(webPage.content, 'html.parser')
    info = html.select(".week-nav-current > .week-nav-current_week")
    return int(''.join(c for c in info[0].text if c.isdigit()))


def ParseGroups() -> None:
    groupsInfo = {}
    for course in range(1, 6):
        webPage = requests.get(f"https://ssau.ru/rasp/faculty/492430598?course={course}")
        html = BS(webPage.content, 'html.parser')

        for group in html.select(".group-catalog__groups > a"):
            groupsInfo[group.text[1:-1]] = group['href']
    
    with open("GroupsInfo.json", "w") as file:
        json.dump(groupsInfo, file, indent=4)


def ParseTeachers() -> None:
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
        json.dump(teachersInfo, file, indent=4, ensure_ascii=False)


def ParseLesson(scheduleLesson: BS) -> dict:
    # Тип занятия описывается css-классом "lesson-border-type-N", где N означает тип занятия:
    lessonsTypes = {
        1: 'Лекция',
        2: 'Лабораторная',
        3: 'Практика',
        4: 'Другое',
        5: 'Экзамен',
        6: 'Консультация',
        8: 'Зачет',
    }
    lessonInfo = {}
    lessonInfo["discipline"] = scheduleLesson.find("div", "schedule__discipline").text
    lessonInfo["type"] = lessonsTypes[int(scheduleLesson['class'][2][-1])]
    lessonInfo["place"] = scheduleLesson.find("div", "schedule__place").text
    lessonInfo["teacher"] = scheduleLesson.find("div", "schedule__teacher").text
    lessonInfo["groups"] = scheduleLesson.find("div", "schedule__groups").text
    return lessonInfo


def GroupURL(groupNumber: str) -> str:
    with open("GroupsInfo.json", "r") as file:
        groupsInfo = json.load(file)
    url = f"https://ssau.ru{groupsInfo[groupNumber]}"
    return url


def TeachersURL(name: str) -> str:
    with open("TeachersInfo.json", "r") as file:
        teachersInfo = json.load(file)
    url = teachersInfo[name]
    return url


# Возможно убрать дефолтные значения отсюда
def GetScheduleByURL(url: str = "https://ssau.ru/rasp?groupId=531030143", week: int = GetCurrentWeek()) -> None:
    schedule = {
        1: [], # Mon
        2: [], # Tue
        3: [], # Wed
        4: [], # Thu
        5: [], # Fri
        0: [], # Sat
    }
    timeStamps = []

    webPage = requests.get(url + f"&selectedWeek={week}")
    html = BS(webPage.content, 'html.parser')

    timeItems = html.select(".schedule__items > .schedule__time")
    for time in timeItems:
        timeStamps.append(time.text)

    scheduleItems = html.select(".schedule__items > .schedule__item")
    for i in range(7, len(scheduleItems)):
        if len(scheduleItems[i].contents) != 0:
            lessons = scheduleItems[i].select(".schedule__lesson")
            for lesson in lessons:
                lessonInfo = ParseLesson(lesson)
                lessonInfo["time"] = timeStamps[i // 6 - 1]
                schedule[i % 6].append(lessonInfo)
    
    with open("Schedule.json", "w") as file:
        json.dump(schedule, file, indent=4, ensure_ascii=False)
