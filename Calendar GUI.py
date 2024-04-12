import flet as ft
from flet import *
import calendar
import datetime

# константы
CELL_SIZE = (28, 28)
CELL_BG_COLOR = 'white10'
TODAY_BG_COLOR = 'teal600'


class SetCalendar(UserControl):
    def __init__(self, start_year=datetime.date.today().year):
        self.current_year = start_year
        self.m1 = datetime.date.today().month
        self.m2 = self.m1 + 1
        self.click_count: list = []
        self.long_press_count: list = []
        self.current_color = "blue"
        self.selected_date = any

        self.calendar_grid = Column(
            wrap=True,
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )
        super().__init__()

    def _change_month(self, delta):
        self.m1 = min(max(1, self.m1 + delta), 12)
        self.m2 = min(max(2, self.m2 + delta), 13)

        new_calendar = self.create_month_calendar(self.current_year)
        self.calendar_grid = new_calendar
        self.update()

    def one_click_date(self, e):
        self.selected_date = e.control.data
        e.control.bgcolor = 'green600'
        e.control.update()
        self.update()

    def create_month_calendar(self, year):
        self.current_year = year
        self.calendar_grid.controls: list = []

        for month in range(self.m1, self.m2):
            month_label = Text(
                f"{calendar.month_name[month]} {self.current_year}",
                size=14,
                weight='bold'
            )

            month_matrix = calendar.monthcalendar(self.current_year, month)
            month_grid = Column(alignment=MainAxisAlignment.CENTER)
            month_grid.controls.append(
                Row(
                    alignment=MainAxisAlignment.START,
                    controls=[month_label],
                )
            )

            weekday_labels = [
                Container(
                    width=28,
                    height=28,
                    alignment=alignment.center,
                    content=Text(
                        weekday,
                        size=12,
                        color='white',
                    ),
                )
                for weekday in ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
            ]

            weekday_row = Row(controls=weekday_labels)
            month_grid.controls.append(weekday_row)

            for week in month_matrix:
                week_container = Row()
                for day in week:
                    if day == 0:
                        day_container = Container(
                            width=28,
                            height=28,
                        )
                    else:
                        day_container = Container(
                            width=28,
                            height=28,
                            border=border.all(0.5, 'white24'),
                            alignment=alignment.center,
                            data=datetime.date(
                                year=self.current_year,
                                month=month,
                                day=day
                            ),
                            on_click=lambda e: self.one_click_date(e),
                            # on_long_press=lambda e: self.long_click_date(e),
                            animate=400
                        )
                    day_label = Text(str(day), size=12)

                    if day == 0:
                        day_label = None
                    if (
                            day == datetime.date.today().day
                            and month == datetime.date.today().month
                            and self.current_year == datetime.date.today().year
                    ):
                        day_container.bgcolor = 'teal700'
                    day_container.content = day_label
                    week_container.controls.append(day_container)
                month_grid.controls.append(week_container)

        self.calendar_grid.controls.append(month_grid)

        return self.calendar_grid

    def build(self):
        return self.create_month_calendar(self.current_year)


class DateSetUp(UserControl):
    def __init__(self, cal_grid):
        self.cal_grid = cal_grid

        self.prev_btn = BTNNumeration('Назад', lambda e: cal_grid._change_month(-1))
        self.next_btn = BTNNumeration('Вперёд', lambda e: cal_grid._change_month(1))

        self.today = Text(
            datetime.date.today().strftime("%B %d, %Y"),
            width=260,
            size=13,
            color='white54',
            weight='w400'
        )

        self.btn_container = Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                self.prev_btn,
                self.next_btn
            ],
        )

        self.calendar = Container(
            width=320,
            height=45,
            bgcolor="#313131",
            border_radius=8,
            animate=300,
            clip_behavior=ClipBehavior.HARD_EDGE,
            alignment=alignment.center,
            content=Column(
                alignment=MainAxisAlignment.START,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Divider(height=60, color='transparent'),
                    self.cal_grid,
                    Divider(height=10, color='transparent'),
                    self.btn_container,
                ],
            ),
        )

        super().__init__()

    def _get_calendar(self, e: None):
        if self.calendar.height == 45:
            self.calendar.height = 450
            self.calendar.update()
        else:
            self.calendar.height = 45
            self.calendar.update()

    def build(self):
        return Stack(
            width=320,
            controls=[
                self.calendar,
                Container(
                    on_click=lambda e: self._get_calendar(e),
                    width=320,
                    height=45,
                    border_radius=8,
                    bgcolor='#313131',
                    padding=padding.only(left=15, right=5),
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            self.today,
                            Container(
                                width=32,
                                height=32,
                                border=border.only(
                                    left=BorderSide(0.9, 'white24'),
                                ),
                                alignment=alignment.center,
                                content=Icon(
                                    name=icons.CALENDAR_MONTH_SHARP,
                                    size=15,
                                    opacity=0.65,
                                ),
                            ),
                        ],
                    ),
                ),
            ],
        )


class BTNNumeration(UserControl):
    def __init__(self, txt_name, function):
        self.txt_name = txt_name
        self.function = function
        super().__init__()

    def build(self):
        return IconButton(
            content=Text(self.txt_name, size=8, weight='bold'),
            width=56,
            height=28,
            on_click=self.function,
            style=ButtonStyle(
                shape={"": RoundedRectangleBorder(radius=6)},
                bgcolor={"": 'teal600'}
            ),
        )


def main(page: Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.padding = 80
    page.title = "Календарь"

    dlg = ft.AlertDialog(
        title=ft.Text("""
        7 Фев- Президентские выборы
        8 Мар- Международный женский день
        11 Мар- Рамадан старт
        20 Мар- Новруз праздник
        """),
        on_dismiss=lambda e: print("Dialog dismissed!"),
    )

    def open_dlg(e):
        page.dialog = dlg
        dlg.open = True
        page.update()


    cal = SetCalendar()
    date = DateSetUp(cal)

    page.add(
        Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[date]
        ),
        ft.ElevatedButton("События", on_click=open_dlg),

    )
    page.update()


if __name__ == '__main__':
    ft.app(target=main)
    # flet.app(target=main, view=flet.AppView.WEB_BROWSER)
