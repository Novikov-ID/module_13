from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton( text='Информация')
button2 = KeyboardButton( text='Расчитать')
kb.row(button1, button2)

kb_in = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text='Расчитать норму калорий',callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта',callback_data='formulas')
kb_in.add(button1,button2)


class UserState(StateGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text=['Информация'])
async def info_message(message):
    await message.answer('Рассчёт суточной нормы калорий по упрощённой формулу Миффлина - Сан Жеора.')

@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:',reply_markup=kb_in)

@dp.callback_query_handler(text=['formulas'])
async def get_formulas(call):
    await call.message.answer(f'Для мужчин:\n\t'
                                 f'10*вес + 6.25*рост - 5*возраст + 5\n'
                                 f'Для женщин:\n\t'
                                 f'10*вес + 6.25*рост - 5*возраст -161')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_gender(message, state):
    await state.update_data(age=message.text)
    await message.answer(f'Введите свой пол жен/муж:')
    await UserState.gender.set()


@dp.message_handler(state=UserState.gender)
async def set_growth(message, state):
    await state.update_data(gender=message.text)
    await message.answer(f'Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer(f'Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data_quest = await state.get_data()

    if data_quest['gender'] == 'муж':
        result = 10 * int(data_quest['weight']) + \
                 6.25 * int(data_quest['growth']) - \
                 5 * int(data_quest['age']) + 5

    elif data_quest['gender'] == 'жен':
        result = 10 * int(data_quest['weight']) + \
                 6.25 * int(data_quest['growth']) - \
                 5 * int(data_quest['age']) + 5
        10 * int(data_quest['weight']) + \
        6.25 * int(data_quest['growth']) - \
        5 * int(data_quest['age']) - 161

    await message.answer(f'Ваша норма калорий: {result} ккал в сутки.')
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
