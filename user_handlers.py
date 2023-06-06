import keyboards
import Api
from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.types import Message, CallbackQuery
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

user_answer={}
bot_answer=[]
# user_answer={"departure":[],"arrival":[],"date_departure":{"year":[],"month":[],"day":[]},"price":[],"return_departure_date":[]}
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    fill_departure = State()        # Состояние ожидания ввода места отправления
    fill_arrival = State()         # Состояние ожидания ввода места прибытия
    fill_date_departure = State()   # Состояние ожидания выбора даты отправления
    fill_date_departure_kb = State()
    fill_way = State() 
    fill_way_one_two = State()   
    fill_date_return= State()
    fill_way_two_ticket= State()

router: Router = Router()

#Хендлер начало
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await state.clear()
    answer_start=await message.answer(text='Ну что, начнем?', reply_markup=keyboards.go_kb())
    bot_answer.append(answer_start)

    

@router.message(Command(commands='begin'))
async def process_start_command(message: Message, state: FSMContext):
    await state.clear()
    ansewr_begin=await message.answer(text='Ну что, начнем?', reply_markup=keyboards.go_kb())
    bot_answer.append(ansewr_begin)
    
    

#Хендлер город вылета
@router.callback_query(Text(text='Поехали!!!'))
async def process_departure(callback: CallbackQuery, state: FSMContext):
    answer_takeoff=await callback.message.answer(text='Откуда планируете вылет?🛫')
    await state.set_state(FSMFillForm.fill_departure)
    bot_answer.append(answer_takeoff)

#Хендлер город прилета
@router.message(StateFilter(FSMFillForm.fill_departure))
async def process_arrival(message: Message, state: FSMContext):
    asnwer_landing=await message.answer(text='Где надо преземлиться?🛬')
    user_answer[message.chat.id]={}
    user_answer[message.chat.id]["departure"] = message.text
    await state.set_state(FSMFillForm.fill_date_departure) 
    bot_answer.append(asnwer_landing)


#Хендлер календарь прилета.год
@router.message(StateFilter(FSMFillForm.fill_date_departure))
async def process_year(message: Message,state: FSMContext):
    user_answer[message.chat.id]["date_departure"]={}
    user_answer[message.chat.id]["return_departure_date"]={}
    user_answer[message.chat.id]["date_departure"].update({"year":0,"month":0,"day":0})
    user_answer[message.chat.id]["return_departure_date"].update({"year":0,"month":0,"day":0})
    user_answer[message.chat.id]["arrival"]= message.text
    answer_message_year=await message.answer("Выберете год:", reply_markup=keyboards.year_kb())
    bot_answer.append(answer_message_year)
    await state.set_state(FSMFillForm.fill_date_departure_kb)
    
#Хендлер календарь прилета.месяц 
@router.callback_query(Text(text=keyboards.year),StateFilter(FSMFillForm.fill_date_departure_kb))
async def process_month(callback: CallbackQuery):
    global answer_message_month
    if user_answer[callback.from_user.id]["date_departure"]["year"]:
        user_answer[callback.from_user.id]["date_departure"]["year"]= callback.data
        await answer_message_month.edit_text(text="Выберете месяц:",
                                         reply_markup=keyboards.month_kb(user_answer[callback.from_user.id]["date_departure"]["year"]))
        if user_answer[callback.from_user.id]["date_departure"]["day"]:
            await answer_message_day.edit_text("Выберете день:", reply_markup=keyboards.day_kb(int(user_answer[callback.from_user.id]["date_departure"]["year"]),
                                                                                    int(1+keyboards.months.index(user_answer[callback.from_user.id]["date_departure"]["month"]))))
    else:
        user_answer[callback.from_user.id]["date_departure"]["year"]= callback.data
        answer_message_month = await callback.message.answer("Выберете месяц:", reply_markup=keyboards.month_kb(user_answer[callback.from_user.id]["date_departure"]["year"]))
    bot_answer.append(answer_message_month)

#Хендлер календарь прилета.день
@router.callback_query(Text(text=keyboards.months),StateFilter(FSMFillForm.fill_date_departure_kb))
async def process_day(callback: CallbackQuery,state: FSMContext):
    global answer_message_day
    if user_answer[callback.from_user.id]["date_departure"]["month"]:
        user_answer[callback.from_user.id]["date_departure"]["month"] = callback.data
        await answer_message_day.edit_text("Выберете день:", reply_markup=keyboards.day_kb(int(user_answer[callback.from_user.id]["date_departure"]["year"]),
                                                                                    int(1+keyboards.months.index(user_answer[callback.from_user.id]["date_departure"]["month"]))))
    else:
        user_answer[callback.from_user.id]["date_departure"]["month"] = callback.data
        answer_message_day = await callback.message.answer("Выберете день:", reply_markup=keyboards.day_kb(int(user_answer[callback.from_user.id]["date_departure"]["year"]),
                                                                                    int(1+keyboards.months.index(user_answer[callback.from_user.id]["date_departure"]["month"]))))
    bot_answer.append(answer_message_day)
    await state.set_state(FSMFillForm.fill_way_one_two)


#Клавиатура выбора туда обратно      
@router.callback_query(Text(text=keyboards.list_day),StateFilter(FSMFillForm.fill_way_one_two)) 
async def process_one_way(callback: CallbackQuery):
    user_answer[callback.from_user.id]["date_departure"]["day"]= callback.data
    answer_way=await callback.message.answer("Выберете в одну сторону или в обе:", reply_markup=keyboards.way_kb())
    bot_answer.append(answer_way)

#Выдача билетов в один конец
@router.callback_query(StateFilter(FSMFillForm.fill_date_departure_kb),Text(text="one_way"))
async def process_ticket_one_way(callback: CallbackQuery):
    print(user_answer)
    for i in bot_answer:
        await i.delete()
    await callback.message.answer(text="Ваши билеты:")
    ticket=Api.api_response_1way(user_answer[callback.from_user.id]["departure"],user_answer[callback.from_user.id]["arrival"],
                                        f'{user_answer[callback.from_user.id]["date_departure"]["year"]}-{keyboards.months_number[user_answer[callback.from_user.id]["date_departure"]["month"]]}-{user_answer[callback.from_user.id]["date_departure"]["day"]}')
    if ticket:
        for i in ticket:
            await callback.message.answer(text=i[0], reply_markup=keyboards.url_kb(i[1]))
    else:
        await callback.message.answer(text="На данное число билеты не найдены")
    

#Хендлер календарь вылета год 
@router.callback_query(Text(text="two_way"))
async def process_year_return(callback: CallbackQuery, state: FSMContext):
    answer_message_year = await callback.message.answer("Выберете год:", reply_markup=keyboards.year_kb())
    bot_answer.append(answer_message_year)
    await state.set_state(FSMFillForm.fill_date_return)
    
#Хендлер календарь вылета месяц 
@router.callback_query(StateFilter(FSMFillForm.fill_date_return),Text(text=keyboards.year))
async def process_month_return(callback: CallbackQuery):
    if user_answer[callback.from_user.id]["return_departure_date"]["year"]:
        user_answer[callback.from_user.id]["return_departure_date"]["year"]= callback.data
        await answer_message_month.edit_text(text="Выберете месяц:",
                                         reply_markup=keyboards.month_kb(user_answer[callback.from_user.id]["return_departure_date"]["year"]))
        if user_answer[callback.from_user.id]["return_departure_date"]["day"]:
            await answer_message_day_return.edit_text("Выберете день:", reply_markup=keyboards.day_kb(int(user_answer[callback.from_user.id]["return_departure_date"]["year"]),
                                                                                    int(1+keyboards.months.index(user_answer[callback.from_user.id]["return_departure_date"]["month"]))))
    else:
        user_answer[callback.from_user.id]["return_departure_date"]["year"]= callback.data
        answer_message_month = await callback.message.answer("Выберете месяц:", reply_markup=keyboards.month_kb(user_answer[callback.from_user.id]["return_departure_date"]["year"]))
    bot_answer.append(answer_message_month)  

#Хендлер вылета прилета.день
@router.callback_query(StateFilter(FSMFillForm.fill_date_return),Text(text=keyboards.months))
async def process_day_return(callback: CallbackQuery, state: FSMContext):
    global answer_message_day_return
    if user_answer[callback.from_user.id]["return_departure_date"]["month"]:
        user_answer[callback.from_user.id]["return_departure_date"]["month"] = callback.data
        await answer_message_day_return.edit_text("Выберете день:", reply_markup=keyboards.day_kb(int(user_answer[callback.from_user.id]["return_departure_date"]["year"]),
                                                                                    int(1+keyboards.months.index(user_answer[callback.from_user.id]["return_departure_date"]["month"]))))
        
    else:
        user_answer[callback.from_user.id]["return_departure_date"]["month"] = callback.data
        answer_message_day_return = await callback.message.answer("Выберете день:", reply_markup=keyboards.day_kb(int(user_answer[callback.from_user.id]["return_departure_date"]["year"]),
                                                                                    int(1+keyboards.months.index(user_answer[callback.from_user.id]["return_departure_date"]["month"]))))
    bot_answer.append(answer_message_day_return)
    await state.set_state(FSMFillForm.fill_way_two_ticket)


# Выдача билетов в два направления
@router.callback_query(StateFilter(FSMFillForm.fill_way_two_ticket))
async def process_ticket_one_way(callback: CallbackQuery):
    user_answer[callback.from_user.id]["return_departure_date"]["day"]= callback.data
    for i in bot_answer:
        try:
            await i.delete()
        except:
            pass
    await callback.message.answer(text="Ваши билеты:")
    print(user_answer)
    ticket=Api.api_response_2way(user_answer[callback.from_user.id]["departure"],user_answer[callback.from_user.id]["arrival"],
                                        f'{user_answer[callback.from_user.id]["date_departure"]["year"]}-{keyboards.months_number[user_answer[callback.from_user.id]["date_departure"]["month"]]}-{user_answer[callback.from_user.id]["date_departure"]["day"]}',
                                        f'{user_answer[callback.from_user.id]["return_departure_date"]["year"]}-{keyboards.months_number[user_answer[callback.from_user.id]["return_departure_date"]["month"]]}-{user_answer[callback.from_user.id]["return_departure_date"]["day"]}')
    if ticket:
        for i in ticket:
            await callback.message.answer(text=i[0], reply_markup=keyboards.url_kb(i[1]))
    else:
        await callback.message.answer(text="На данное число билеты не найдены")

