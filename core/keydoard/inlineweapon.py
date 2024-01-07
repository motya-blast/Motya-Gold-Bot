from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from core.utils.callbackdata import WeapInfo


def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="ST TEC-9 \"Tropick\"",
                            callback_data=WeapInfo(stattrack='S/T',
                                                   types='weapon',
                                                   name='TEC-9',
                                                   skin='Tropick'))
    keyboard_builder.button(text="ST Berettas \"Soul Devourer\"", 
                            callback_data=WeapInfo(
                                stattrack='S/T',
                                types='weapon',
                                name='Berettas',
                                skin='Soul Devourer'))
    keyboard_builder.button(text="ST Mac10 \"Noxious\"",
                            callback_data=WeapInfo(
                                stattrack='S/T',
                                types='weapon',
                                name='MAC-10',
                                skin='Noxious'))
    keyboard_builder.button(text="ST M40 \"Grip\"", 
                            callback_data=WeapInfo(
                                stattrack='S/T',
                                types='weapon',
                                name='M40',
                                skin='Grip'))
    keyboard_builder.button(text="Graffiti \"Molotov\"", 
                            callback_data=WeapInfo(
                                name='Graffiti',
                                skin='Molotov'))
    keyboard_builder.button(text='Graffiti "Done"', 
                            callback_data=WeapInfo(
                                
                                name='Graffiti',
                                skin='Done'))#'Graffiti_done')
    keyboard_builder.button(text='Graffiti "Headshot"', 
                            callback_data=WeapInfo(
                                
                                name='Graffiti',
                                skin='Headshot'))#'Graffiti_headshot')
    keyboard_builder.button(text='Graffiti "Blue Fire"', 
                            callback_data=WeapInfo(
                                
                                name='Graffiti',
                                skin='Blue Fire'))#'Graffiti_blue_fire')
    keyboard_builder.button(text='Graffiti "Vibes"', 
                            callback_data=WeapInfo(
                                
                                name='Graffiti',
                                skin='Vibes'))#'Graffiti_vibes')
    keyboard_builder.button(text='Graffiti "Sorry"', 
                            callback_data=WeapInfo(
                                
                                name='Graffiti',
                                skin='sorry'))#'Graffiti_sorry')
    keyboard_builder.button(text='Graffiti "Ban"', 
                            callback_data=WeapInfo(
                                
                                name='Graffiti',
                                skin='Ban'))#'Graffiti_ban')
    keyboard_builder.button(text='UMP45 "Geometric"', 
                            callback_data=WeapInfo(
                                
                                types='weapon',
                                name='UMP45',
                                skin='Geometric'))#'ump45_geometric')
    keyboard_builder.button(text='M110 "Themis"', 
                            callback_data=WeapInfo(
                                
                                types='weapon',
                                name='M110',
                                skin='Themis'))#'m110_themis')
    keyboard_builder.button(text='Отмена', callback_data='cancel')
    keyboard_builder.adjust(3,3,3,3,1,1)
    return keyboard_builder.as_markup()