localStorage.setItem("event_name", "Roma's birthday party");
localStorage.setItem("start_date", "2023-08-15");

const event_label = document.createElement("label");
event_label.textContent = localStorage.getItem("event_name");
event_label.setAttribute("id", "event_name");

const calendar = document.querySelector("table");
calendar.insertAdjacentElement("beforebegin", event_label);
console.log(localStorage.getItem("start_date"));

const dates_row = document.createElement("tr");
const month_cell = document.createElement("td");
month_cell.classList.add("month_name");
month_cell.innerText = "July";
dates_row.append(month_cell);
for (let i = 0; i < 7; i++) {
    const td = document.createElement("td");
    td.classList.add("day");
    if ((i + 1) % 7 === 0 || (i + 2) % 7 === 0) {
        td.classList.add("holiday");
    }
    td.setAttribute("id", i.toString());
    td.innerText = i.toString();
    dates_row.append(td);
}

calendar.insertAdjacentElement("beforeend", dates_row);



