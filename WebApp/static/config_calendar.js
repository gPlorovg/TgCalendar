const calendar = document.querySelector("table");
const event_label = document.createElement("label");
// const create_btn = document.createElement("button");
let dates;
const tg = window.Telegram.WebApp;

tg.MainButton.text = "create";
tg.MainButton.setParams({"color": "#DF2727", "textColor": "#FFFFFF"});
tg.MainButton.onClick(create_calendar);

// create_btn.innerText = "create calendar";
// create_btn.addEventListener("click", create_calendar);
event_label.textContent = localStorage.getItem("event_name");
event_label.setAttribute("id", "event_name");
calendar.insertAdjacentElement("beforebegin", event_label);
// calendar.insertAdjacentElement("afterend", create_btn);


const clicked_days = new Array(35).fill(false);
// const day = document.createElement("td");
// day.classList.add("day");
// day.setAttribute("id", "5");
// day.innerText = "5";

function create_calendar() {
    // console.log(JSON.stringify(dates));
    const data_set = {
        "action" : "config",
        "event_name" : localStorage.getItem("event_name"),
        "dates": dates.filter((item, i) => clicked_days[i])
    };
    tg.sendData(JSON.stringify(data_set));
    // const resp = JSON.stringify({"data": dates.filter((item, i) => clicked_days[i]),
    //     "action" : "config"});
    // console.log(resp);
    // const parse_resp = JSON.parse(resp);
    // console.log(parse_resp["action"]);
    // console.log(parse_resp["data"]);
    // window.Telegram.WebApp.close();
    // fetch(window.location.origin + "/create_calendar", {
    //             method: "POST",
    //             headers: {
    //                 "Content-Type": "application/json"
    //             },
    //             body: JSON.stringify(dates.filter((item, i) => clicked_days[i]))
    // })
    //     .then((resp) => resp.json())
    //     .then((resp) => feedback(resp));
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

function feedback (resp) {
    console.log(resp);
}

// day.addEventListener("click", day_click);
//
// const dates_row = document.createElement("tr");
// dates_row.append(day);
// calendar.insertAdjacentElement("beforeend", dates_row);



function draw_grid(positions, months_positions) {
    tg.ready();
    // tg.expand();
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

// draw_grid(['', '', '16.08.2023', '17.08.2023', '18.08.2023', '19.08.2023', '20.08.2023', '21.08.2023', '22.08.2023', '23.08.2023', '24.08.2023', '25.08.2023', '26.08.2023', '27.08.2023', '28.08.2023', '29.08.2023', '30.08.2023', '31.08.2023', '', '', '', '', '', '', '', '01.09.2023', '02.09.2023', '03.09.2023', '04.09.2023', '05.09.2023', '06.09.2023', '07.09.2023', '08.09.2023', '09.09.2023', '10.09.2023'],['August', '', '', 'September', '']);

fetch(window.location.origin + "/tg_calendar/calendar_grid?start_date=" + localStorage.getItem("start_date"))
    .then((json_data) => json_data.json())
    .then((resolved_data) => draw_grid(resolved_data.positions, resolved_data.months_positions));