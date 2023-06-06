from aiogram import Router
import datetime
import calendar
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
router: Router = Router()
year=[str(datetime.datetime.now().year),str(datetime.datetime.now().year+1)]
months = ["Январь", 'Февраль', "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь",
           "Октябрь", "Ноябрь", "Декабрь"]
months_number = {"Январь":"01", 'Февраль': "02", "Март": "03", "Апрель" : "04", "Май" : "05", "Июнь" : "06", "Июль" : "07",
                  "Август" : "08", "Сентябрь" : "09","Октябрь" : "10", "Ноябрь" : "11", "Декабрь" : "12"}
days_week=["  Пн  ", "  Вр  ", "  Ср  ", "  Чт  ", "  Пт  ", "  Сб  ", "  Вс  "]
list_day=[]
# button_go: KeyboardButton = KeyboardButton(text='Поехали!!!')    удалить


#Клавиатура начала
def go_kb():
    go_kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    go_bt= InlineKeyboardButton(text='Поехали!!!', callback_data='Поехали!!!')
    go_kb.row(go_bt, width=1)
    return go_kb.as_markup(one_time_keyboard=True,resize_keyboard=True)

# Клавиатура выбора месяца
def month_kb(Year_answer):
    month_kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons=[]
    if Year_answer==str(datetime.datetime.now().year):
        for index, button in enumerate(months):
            if index < datetime.datetime.now().month-1:
                pass
            else:
                buttons.append(InlineKeyboardButton(text=button,
                        callback_data=button))
    else:
        for button in months:
            buttons.append(InlineKeyboardButton(text=button,
                    callback_data=button))
    month_kb.row(*buttons, width=4)
    return month_kb.as_markup()

#Клавиатура выбора года
def year_kb():
    year_kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons=[]
    for button in year:
        buttons.append(InlineKeyboardButton(text=button,
                callback_data=button))
    year_kb.row(*buttons, width=2)
    return year_kb.as_markup()



#Клавиатура выбора дня
def day_kb(year,month):
    day_kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    month_calendar = calendar.monthcalendar(year, month)
    week=[]
    days_month=[]
    for days in days_week:
        week.append(InlineKeyboardButton(text=days,
                callback_data=days))
    for day_numbers in month_calendar:
        for numbers in day_numbers:
            if numbers==0:
                days_month.append(InlineKeyboardButton(text=" ",
                        callback_data=" "))
            else:
                list_day.append(str(numbers))
                days_month.append(InlineKeyboardButton(text=numbers,
                callback_data=str(numbers)))
    day_kb.row(*week,width=7)
    day_kb.row(*days_month,width=7)
    return day_kb.as_markup()




def way_kb():
    way_kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    one_way_bt= InlineKeyboardButton(text='→', callback_data = "one_way")
    two_way_bt= InlineKeyboardButton(text='⇆', callback_data = "two_way")
    way_kb.row(one_way_bt,two_way_bt, width=2)
    return way_kb.as_markup()

def url_kb(url):
    url_kb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    url_kb_bt= InlineKeyboardButton(text='Купить', url=f"https://www.aviasales.ru{url}")
    url_kb.row(url_kb_bt)
    return url_kb.as_markup()