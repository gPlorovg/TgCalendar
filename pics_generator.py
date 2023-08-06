from PIL import Image, ImageDraw, ImageColor, ImageFont
import calculate as calc
from math import ceil


class Calendar:
    def __init__(self, head_date, tail_date, text):
        self.basic = ImageColor.getrgb("#D9D9D9")
        self.black = ImageColor.getrgb("#1E1E1E")
        self.red = ImageColor.getrgb("#DF2727")
        self.colors = [ImageColor.getrgb(i) for i in ["#e60049", "#0bb4ff", "#50e991", "#e6d800", "#9b19f5", "#ffa300",
                                                      "#dc0ab4", "#27aeef", "#00bfa0"]]
        self.transparent = (255, 0, 0, 0)
        self.font24 = ImageFont.truetype("RobotoMono-Medium.ttf", 24)
        self.font28 = ImageFont.truetype("RobotoMono-Medium.ttf", 28)
        self.font40 = ImageFont.truetype("RobotoMono-Medium.ttf", 40)
        self.font44 = ImageFont.truetype("RobotoMono-Medium.ttf", 44)

        self.head = head_date
        self.tail = tail_date
        # (name, color, [dates])
        self.users = list()
        self.text = text
        self.main_w = 1650 + 180
        self.positions = calc.get_positions(self.head, self.tail)
        self.weeks = ceil(len(self.positions) / 7)
        # self.main_h = 60 + 58 * text_lines + 52 + 160 + 170 * weeks + 20
        self.main_h = 350 + 170 * self.weeks
        self.image = Image.new("RGBA", (self.main_w, self.main_h), self.transparent)
        self.draw = ImageDraw.Draw(self.image)

        self.draw_main()
        self.draw_title()
        self.draw_header()
        self.draw_grid()

    def draw_main(self):
        self.draw.rounded_rectangle((0, 0, self.main_w, self.main_h), fill=self.basic, outline=self.transparent,
                                    width=1, radius=28)

    def draw_title(self):
        self.draw.text((self.main_w // 2 - len(self.text) * 14, 60), self.text, font=self.font44, fill=self.black)

    def draw_header(self):
        x = 20 + 180
        y = 170
        for i in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            color = self.red if i == "Saturday" or i == "Sunday" else self.black
            self.draw.rounded_rectangle((x, y, x + 160, y + 160), fill=color, outline=color,
                                        width=4, radius=28)
            self.draw.text((x + 4 + (9 - len(i)) * 8, y + 58), i, font=self.font28, fill="white")
            x += 170

    def draw_day(self, x, y, date, is_weekend):
        color = self.red if is_weekend else self.black

        self.draw.rounded_rectangle((x, y, x + 160, y + 160), fill=self.basic, outline=color,
                                    width=4, radius=28)
        self.draw.rounded_rectangle((x + 14, y + 12, x + 14 + 36, y + 12 + 32), fill=self.basic, outline=color,
                                    width=2, radius=6)
        self.draw.text((x + 14 + 5, y + 12 - 2), date, font=self.font24, fill=color)

    def draw_grid(self):
        x = 20 + 180
        y = 170
        f = True
        for i, v in enumerate(self.positions):
            if f and v != "" or v.split(".")[0] == "01":
                self.draw.text((20, y + 10), calc.determine_month(v.split(".")[1]), font=self.font28, fill=self.black)
                self.draw.line((20, y + 10 + 36, 20 + len(calc.determine_month(v.split(".")[1]) * 17), y + 10 + 36),
                               fill=self.black, width=3)
                f = False
            if v != "":
                self.draw_day(x, y, v.split(".")[0], (i + 1) % 7 == 0 or i % 7 == 0)
            if i % 7 == 0:
                x = 20 + 180
                y += 170
            else:
                x += 170

    def add_user(self, name, dates):
        if self.colors:
            self.users.append((name, self.colors.pop(), dates))
        self.draw_names()
        self.draw_marks()

    def draw_names(self):
        y = self.main_h // 2
        for user in self.users:
            self.draw.text((1340 + 180, y), user[0], font=self.font40, fill=user[1])
            y += 60

    def draw_marks(self):
        for i_user, user in enumerate(self.users):
            for date in user[2]:
                try:
                    i = self.positions.index(date)
                except ValueError:
                    print(date + "not in calendar!")
                else:
                    y = 340 + (i // 7) * 170 + 12 + i_user * 20
                    if i_user < 2:
                        x = 20 + 180 + (i % 7 - 1) * 170 + 48 + 6
                        self.draw.rounded_rectangle((x, y, x + 96, y + 16), fill=user[1], outline=user[1],
                                                    width=1, radius=8)
                    else:
                        x = 20 + 180 + (i % 7 - 1) * 170 + 6
                        self.draw.rounded_rectangle((x, y, x + 144, y + 16), fill=user[1], outline=user[1],
                                                    width=1, radius=8)

    def save(self, path="test.png"):
        print("save")
        self.image.save(path)


if __name__ == "__main__":
    test = Calendar("29.07.2023", "04.08.2023", "День рождения Ромы")
    test.add_user("@plorov", ["29.07.2023", "30.07.2023", "02.08.2023"])
    test.add_user("Денис", ["29.07.2023", "30.07.2023"])
    test.add_user("Катя К", ["29.07.2023", "30.07.2023"])
    test.add_user("Влад", ["29.07.2023", "30.07.2023"])
    test.add_user("@spqrty", ["29.07.2023", "30.07.2023"])
    test.draw_marks()
    test.save()
