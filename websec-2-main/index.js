fetch('/rasp?groupId=531030143')
    .then((data) => data.json())
    .then((res) => {
        console.log(res);
        renderSchedule(res);
        currentWeek = parseInt(res.currentWeek);
        document.querySelector("#currentWeek").innerHTML = `${currentWeek} неделя`;
        if (currentWeek == 1) {
            document.querySelector("#previousButton").style.visibility = "hidden";
        } else {
            document.querySelector("#previousButton").style.visibility = "visible";
        }
    })

fetch('/groups')
    .then((data) => data.json())
    .then((res) => {
        console.log(res);
        let selectElement = document.querySelector("#select");
        for (group in res) {
            let groupElement = document.createElement("option");
            groupElement.innerHTML = group;
            groupElement.setAttribute("value", res[group]);
            selectElement.appendChild(groupElement);
        }
        selectElement.addEventListener("change", () => {
            updateSchedule(selectElement.value);
            console.log("LOOK:", selectElement.value)
        })
    })

fetch('/teachers')
    .then((data) => data.json())
    .then((res) => {
        console.log(res);
        let selectElement = document.querySelector("#selectTeacher");
        for (teacher in res) {
            let teacherElement = document.createElement("option");
            teacherElement.innerHTML = teacher;
            teacherElement.setAttribute("value", res[teacher]);
            selectElement.appendChild(teacherElement);
        }
        selectElement.addEventListener("change", () => {
            updateSchedule(selectElement.value);
        })
    })

let currentUrl = '/rasp?groupId=531030143';
let currentWeek;
let currentDay = new Date().getDay();
let styles = "";
let styleSheet = document.createElement("style");
styleSheet.classList.add("schedule-style");


function updateSchedule(url) {
    currentUrl = url;
    fetch(url)
        .then((data) => data.json())
        .then((res) => {
            renderSchedule(res);
            console.log(res);
            currentWeek = parseInt(res.currentWeek);
            document.querySelector("#currentWeek").innerHTML = `${currentWeek} неделя`;
            if (currentWeek == 1) {
                document.querySelector("#previousButton").style.visibility = "hidden";
            } else {
                document.querySelector("#previousButton").style.visibility = "visible";
            }
        })
}

function renderSchedule(data) {
    let table = document.querySelector("#schedule");
    table.innerHTML = "";
    console.log(table);
    let headers = table.insertRow();
    headers.classList.add("first-row"); // класс верхней строчки
    headers.insertCell().appendChild(document.createTextNode("Время"));

    let ind = 0;
    for (let date of data.dates) {
        let cell = headers.insertCell();
        cell.appendChild(document.createTextNode(date));
        cell.classList.add(`column-${ind}`);
        ind++;
    }

    ind = 0;
    let days = data.daysOfSchedule;

    for (let time of data.times) {
        let row = table.insertRow();
        row.classList.add("one-row"); // класс <tr>
        row.insertCell().appendChild(document.createTextNode(time));

        for (let day of days) {
            if (ind > 5) {
                break;
            }
            if (day.subject !== null) {
                let infoToInsert = document.createElement("div");
                let correctTeacher = JSON.parse(day.teacher);
                infoToInsert.innerHTML = `${day.subject}<br>${day.place}<br>`;
                let teacherElement;
                if (correctTeacher.link !== null) {
                    teacherElement = document.createElement("a");
                    teacherElement.href = "#";
                    teacherElement.innerHTML = correctTeacher.name;
                    teacherElement.addEventListener('click', () => updateSchedule(correctTeacher.link));
                } else {
                    teacherElement = document.createElement("div");
                    teacherElement.innerHTML = correctTeacher.name;
                }
                infoToInsert.classList.add("text-style1"); // класс <div>'а внутри ячейки <td>
                infoToInsert.appendChild(teacherElement);
                infoToInsert.appendChild(document.createElement("br"));
                console.log(correctTeacher);
                for (let group of day.groups) {
                    let correctGroup = JSON.parse(group);
                    let aNode;
                    if (correctGroup.link !== null) {
                        aNode = document.createElement("a");
                        aNode.href = "#";
                        aNode.innerHTML = correctGroup.name;
                        aNode.addEventListener('click', () => updateSchedule(correctGroup.link));
                    } else {
                        aNode = document.createElement("div");
                        aNode.innerHTML = correctGroup.name;
                    }
                    infoToInsert.appendChild(aNode);
                    infoToInsert.appendChild(document.createElement("br"));
                }
                let cell = row.insertCell();
                cell.classList.add(`column-${ind}`);
                cell.appendChild(infoToInsert);
                cell.classList.add("one-cell"); // класс <td> в таблице
            } else {
                let cell = row.insertCell();
                cell.classList.add("one-cell"); // класс <td> в таблице
                cell.classList.add(`column-${ind}`);
            }
            ind++;
        }
        days = days.slice(ind);
        ind = 0;
    }
}

function changePage(goNextPage) {
    let ind = 0;
    while (currentUrl[ind] !== "&" && ind <= 100) ind++;
    if (currentUrl[ind] !== "&") {
        currentUrl += `&selectedWeek=${goNextPage ? currentWeek + 1 + "" : currentWeek - 1 + ""}`;
    } else {
        currentUrl = currentUrl.slice(0, currentUrl.length - (currentWeek > 9 ? 2 : 1));
        currentUrl += goNextPage ? currentWeek + 1 + "" : currentWeek - 1 + "";
    }
    console.log(currentWeek);
    console.log(currentUrl);
    updateSchedule(currentUrl);
}