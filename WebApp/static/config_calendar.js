const calendar = document.querySelector("table");
const event_label = document.createElement("label");
const create_btn = document.createElement("button");
create_btn.innerText = "create calendar";
event_label.textContent = localStorage.getItem("event_name");
event_label.setAttribute("id", "event_name");
calendar.insertAdjacentElement("beforebegin", event_label);
calendar.insertAdjacentElement("afterend", create_btn);


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

draw_grid(['', '', '16.08.2023', '17.08.2023', '18.08.2023', '19.08.2023', '20.08.2023', '21.08.2023', '22.08.2023', '23.08.2023', '24.08.2023', '25.08.2023', '26.08.2023', '27.08.2023', '28.08.2023', '29.08.2023', '30.08.2023', '31.08.2023', '', '', '', '', '', '', '', '01.09.2023', '02.09.2023', '03.09.2023', '04.09.2023', '05.09.2023', '06.09.2023', '07.09.2023', '08.09.2023', '09.09.2023', '10.09.2023'],['August', '', '', 'September', '']);

// fetch(window.location.origin + "/calendar_grid?start_date=" + localStorage.getItem("start_date"))
//     .then((json_data) => json_data.json())
//     .then((resolved_data) => draw_grid(resolved_data.positions, resolved_data.months_positions));