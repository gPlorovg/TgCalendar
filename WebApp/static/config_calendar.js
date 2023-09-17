const calendar = document.querySelector("table");
const event_label = document.createElement("label");
let dates;
const tg = window.Telegram.WebApp;

tg.MainButton.text = "create";
tg.MainButton.setParams({"color": "#DF2727", "textColor": "#FFFFFF"});
tg.MainButton.onClick(create_calendar);

event_label.textContent = localStorage.getItem("event_name");
event_label.setAttribute("id", "event_name");
calendar.insertAdjacentElement("beforebegin", event_label);

const clicked_days = new Array(35).fill(false);

function create_calendar() {
    const data_set = {
        "action" : "config",
        "event_name" : localStorage.getItem("event_name"),
        "dates": dates.filter((item, i) => clicked_days[i])
    };
    tg.sendData(JSON.stringify(data_set));
}

function day_click(el) {
    el.preventDefault();
    const id = parseInt(el.target.id);
    if (clicked_days[id]) {
        clicked_days[id] = false;
        if ((id + 1) % 7 === 0 || (id + 2) % 7 === 0) {
            el.target.style.background = "#D9D9D9";
            el.target.style.color = "#DF2727";
        } else {
            el.target.style.background = "#D9D9D9";
            el.target.style.color = "#1E1E1E";
        }
    } else {
        clicked_days[id] = true;
        if ((id + 1) % 7 === 0 || (id + 2) % 7 === 0) {
            el.target.style.background = "#DF2727";
            el.target.style.color = "white";

        } else {
            el.target.style.background = "#1E1E1E";
            el.target.style.color = "#D9D9D9";
        }
    }
}

function draw_grid(positions, months_positions) {
    tg.ready();
    tg.MainButton.show();

    dates = positions;
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
            day.addEventListener("touchstart", day_click);
        } else {
            day.classList.add("empty");
        }
        weekdays.push(day)
    }
}

fetch(window.location.origin + "/tg_calendar/calendar_grid?start_date=" + localStorage.getItem("start_date"))
    .then((json_data) => json_data.json())
    .then((resolved_data) => draw_grid(resolved_data.positions, resolved_data.months_positions));