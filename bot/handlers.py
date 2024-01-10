import api
import bot.text
import emoji

from aiogram import types, F
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
from .keyboards import kb, func_about_city_kb
from .text import weather_1h, about_of_city
from aiogram import Router

router = Router()

@router.message(Command("help"))
async def help_command(message: types.Message):
    photo: FSInputFile = FSInputFile("bot/img/free-icon-weather-831268.png")
    await message.answer_photo(photo=photo, caption=bot.text[0], parse_mode="HTML")


@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Выберите ваш <b>город</b>", reply_markup=kb.start_kb, parse_mode="HTML")


@router.message(Command("name_city"))
async def about_city_command(message: types.Message):
    message_text: str = "Выберите <b>город</b>"
    keyboard = func_about_city_kb()
    await message.answer(message_text, reply_markup=keyboard.as_markup(), parse_mode="HTML")


@router.callback_query(F.data.endswith("_btn"))
async def callback_response(callback: types.CallbackQuery):
    data_city: tuple | None = api.City(callback.message.text).api_get_info_of_city()
    message_to_user: str = ""

    if data_city:

        for line in range(len(about_of_city)):
            message_to_user += (emoji.emojize(about_of_city[line], language="fr") + data_city[line]) + "\n\n"
        await callback.message.answer(message_to_user)

    else:
        await callback.message.answer("Вы исчерпали все попытки за сегодня.")


@router.message()
async def proccess_callback_button(message: types.Message):
    all_cities: dict = api.Weather().get_all_cities()
    if message.text in all_cities:
        city: str = all_cities.get(message.text)[-1]
        response_to_user: str = f"Вы выбрали город: {message.text}"
        photo = FSInputFile(city)
        await message.answer_photo(photo=photo, caption=response_to_user)

        result_data: str = await weather_data(message.text)
        await message.answer(result_data)

async def weather_data(name_city: str) -> str:
    """
    Обрабатывает данные о погоде, вывод
    :return:
    """
    forecast_weather: api.Weather = api.Weather()
    city_weather_data: tuple = forecast_weather.get_city(name_city)

    if city_weather_data:
        data_weather_for_user: str = ""
        all_text_from_1h: list = weather_1h.weather_data
        for line in range(len(all_text_from_1h)):
            data_weather_for_user += emoji.emojize(all_text_from_1h[line]) + " " + str(city_weather_data[line]) + "\n\n"
        return data_weather_for_user
    else:
        return "К сожалению ваш запрос не удался"