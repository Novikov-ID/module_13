from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

api = ''
bot = Bot(token=api)
ds = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Расчитать')
kb.row(button1, button2)


class UserState(StateGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text=['Информация'])
async def start_message(message):
    await message.answer('Рассчёт суточной нормы калорий по упрощённой формулу Миффлина - Сан Жеора.')


@dp.message_handler(text='Расчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


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
