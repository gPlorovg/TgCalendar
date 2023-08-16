localStorage.setItem("event_name", "Roma's birthday party");
localStorage.setItem("start_date", "2023-08-15");

const event_label = document.createElement("label");
const calendar = document.querySelector("table");
event_label.textContent = localStorage.getItem("event_name");
event_label.setAttribute("id", "event_name");
calendar.insertAdjacentElement("beforebegin", event_label);

function draw_grid(positions, months_positions) {
    let dates_row;
    let month_cell;
    let weekdays = [];
    let day;

    for (const [i, date] of positions.entries()) {
        if (i !== 0 && i % 7 === 0) {
            dates_row = document.createElement("tr");
            month_cell = document.createElement("td");
            month_cell.classList.add("month_name");
            month_cell.innerText = months_positions[Math.floor((i - 1) / 7)];
            dates_row.append(month_cell);
            if (weekdays) {
                for (let td of weekdays) {
                    dates_row.append(td);
                }
                calendar.insertAdjacentElement("beforeend", dates_row);
            }
            weekdays = [];
        }
        day = document.createElement("td");
        if (date !== "") {
            day.classList.add("day");
            if ((i + 1) % 7 === 0 || (i + 2) % 7 === 0) {
                day.classList.add("holiday");
            }
            day.setAttribute("id", i.toString());
            day.innerText = date.split(".")[0];
        } else {
            day.classList.add("empty");
        }
        weekdays.push(day)
    }
}

fetch(window.location.origin + "/calendar_grid?start_date=" + localStorage.getItem("start_date"))
    .then((json_data) => json_data.json())
    .then((resolved_data) => draw_grid(resolved_data.positions, resolved_data.months_positions));