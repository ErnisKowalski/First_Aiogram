from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Sqlite import create_profile, edit_profile, db_start, delete_profile, check_info


API_Token = '6593176333:AAG0-x3uRy3bbieWzNAtIymEHujK1V_bFpE'
bot = Bot(token=API_Token)
dp = Dispatcher(bot, storage=MemoryStorage())


#@dp.message_handler()
#async def location(massage: types.Message):
    #latitude = massage.location.latitude
    #longitude = massage.location.longitude
    #await bot.send_message(text=str(latitude), chat_id=massage.from_user.id)


async def on_startup(x):
    print('Hellow world!')
    await db_start()



class ProfileStateGroup(StatesGroup):
    name = State()
    photo = State()
    hobbies = State()
    leisure = State()


admin_kb = ReplyKeyboardMarkup()
admin_kb.add(['/Удалить профиль']).add(['/Изменить анкету'])

kb1 = ReplyKeyboardMarkup()
kb1.add(KeyboardButton('/Старт'))
kb1.add(KeyboardButton('/Зарегистрироваться'))
kb1.add(KeyboardButton('/Показать тех,кто рядом', ))
kb1.add(KeyboardButton('/Профиль'))
kb1.add(KeyboardButton('/Стоп'))




@dp.message_handler(commands=['Старт'])
async def start(message: types.Message):
    await message.answer(text='Необходимо пройти регистрацию, нажмите кнопку зарегистрироваться', reply_markup=kb1)


@dp.message_handler(commands=['Зарегистрироваться'])
async def register(message: types.Message):
    await bot.send_message(text='Как тебя зовут?', chat_id=message.from_user.id)
    await create_profile(user_id=message.from_user.id)
    await ProfileStateGroup.name.set()


@dp.message_handler(state=ProfileStateGroup.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await bot.send_message(text='Отправь мне своё фото', chat_id=message.from_user.id)
    await ProfileStateGroup.next()


@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=ProfileStateGroup.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo"] = message.photo[0].file_id
    await bot.send_message(chat_id=message.from_user.id,
                           text='Чем ты занимаешься?')
    await ProfileStateGroup.next()


@dp.message_handler(state=ProfileStateGroup.hobbies)
async def load_hobbies(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['hobbies'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                           text='Чем ты увлекаешься?')
    await ProfileStateGroup.next()


@dp.message_handler(state=ProfileStateGroup.leisure)
async def load_leisure(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['leisure'] = message.text
    await bot.send_message(chat_id=message.from_user.id,
                        text='Спасибо за пройденную регистрацию!!')
    proxy_data = await dp.storage.proxy().get_data(chat=message.from_user.id)
    await bot.send_message(text=f'Данные: {proxy_data}')
    await edit_profile(state, user_id=message.from_user.id)
    await state.finish()



@dp.message_handler(commands=['Профиль'])
async def check_profile(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.send_photo(photo=data["photo"],
                             chat_id=message.from_user.id,
                             caption=f'Имя: {data["name"]}\n'
                             f'Увлечение: {data["hobbies"]}\n'
                                 f'Занятие: {data["leisure"]}')
    await edit_profile(state,user_id=message.from_user.id)
    await state.finish()

@dp.message_handler(commands=['admin'])
async def get_admin(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(text='Добрый день', reply_markup=admin_kb,
                           chat_id=message.from_user.id)


@dp.message_handler(commands=['Список пользователей'])
async def get_list(message: types.Message):
    #await delete_profile(user_id=message.from_user.id)
    await bot.send_message(text='Ваш профиль успешно удалён',
                           chat_id=ID)


@dp.message_handler(commands=['Список поисковых запросов'])
async def get_find(message: types.Message):
#    await check_info(user_id=message.from_user.id)
    await bot.send_message(text='')


@dp.message_handler(commands=['Стоп'])
async def delete_info(message: types.Message):
    await delete_profile(user_id=message.from_user.id)
    await bot.send_message(text='Ваш профиль успешно удалён')



if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
