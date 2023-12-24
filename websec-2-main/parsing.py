import json
import codecs
import requests
from bs4 import BeautifulSoup

def ParseTeachers():
    teachers = []
    teachersList = []
    
    for page in range(1, 122):
        url = f"https://ssau.ru/staff?page={page}"
        response = requests.get(url)
        teachers.append(response.text)

        for teacher in teachers:
            soup = BeautifulSoup(teacher, 'html.parser')
            teachersListItems = soup.select(".list-group-item > a")
            for t in teachersListItems:
                staffId = ''.join(filter(str.isdigit, t.get("href")))
                teachersList.append({"name": t.text, "link": f"/rasp?staffId={staffId}"})
    with codecs.open("TeachersList.json", "w", "utf-8") as f:
        f.write(json.dumps(teachersList, ensure_ascii=False))
    f.close()
    return teachersList

def ParseGroups():
    groups = []
    for course in range(1, 6):
        url = f"https://ssau.ru/rasp/faculty/492430598?course={course}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            

            for group in soup.select(".group-catalog__groups > a"):
                groups.append({"name": group.text, "link": "/rasp" + group['href'][group['href'].find('?'):]})
                
    with codecs.open("GroupsList.json", "w", "utf-8") as f:
        f.write(json.dumps(groups, ensure_ascii=False))
    f.close()


# def parser():
#     result = {"teachersList": []}
#     groups = []
#     teachersList = []
#     for i in range(1, 122):
#         url = "https://ssau.ru/staff?page=" + str(i)
#         response = requests.get(url)
#         teachersList.append(response.text)
#         if i == 121:
#             for teacher in teachersList:
#                 soup = BeautifulSoup(teacher, 'html.parser')
#                 teachersList_list = soup.select(".list-group-item > a")
#                 for t in teachersList_list:
#                     staffId = ''.join(filter(str.isdigit, t.get("href")))
#                     result["teachersList"].append({"name": t.text, "link": f"/rasp?staffId={staffId}"})
    
#     for i in range(1, 6):
#         url = "https://ssau.ru/rasp/faculty/492430598?course=" + str(i)
#         response = requests.get(url)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
#             group_list = soup.select(".group-catalog__groups > a")

#             for group in group_list:
#                 group_name = group.text
#                 group_link = "/rasp" + group['href'][group['href'].find('?'):]

#                 groups.append({"name": group_name, "link": group_link})
#                 result["groups"] = groups
#     with codecs.open("groupAndteachersList.json", "w", "utf-8") as stream:
#         stream.write(json.dumps(result, ensure_ascii=False))
#     stream.close()


# parser()
ParseTeachers()
print("teachers parsed")

ParseGroups()
print("groups parsed")