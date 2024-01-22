fetch("/groups")
    .then(response => response.json())
    .then(response => {
        datalist = document.querySelector("#groups_teachers");
        for (group in response) {
            let optionGroup = document.createElement("option");
            optionGroup.innerHTML = group;
            datalist.appendChild(optionGroup)
        }
    })

// TODO: исправить кодировки
fetch("/teachers")
.then(response => response.json())
.then(response => {
    datalist = document.querySelector("#groups_teachers");
    for (teacher in response) {
        let optionTeacher = document.createElement("option");
        optionTeacher.innerHTML = teacher;
        datalist.appendChild(optionTeacher)
    }
})