from django.utils.translation import gettext as _


# --------------------------------- Price Filter ---------------------------------
# def price_maker():
#     price_list = []
#     for i in range(1, 10):
#         price_list.append((f'{i} - {i+1}', f'{i} تا {i+1} میلیارد'))
#
#     for i in range(10, 50, 5):
#         price_list.append((f'{i} - {i+5}', f'{i} تا {i+5} میلیارد'))
#
#     for i in range(50, 100, 10):
#         price_list.append((f'{i} - {i+10}', f'{i} تا {i+10} میلیارد'))
#
#     for i in range(100, 500, 50):
#         price_list.append((f'{i} - {i+50}', f'{i} تا {i+50} میلیارد'))
#
#     for i in range(500, 1000, 100):
#         price_list.append((f'{i} - {i+100}', f'{i} تا {i+100} میلیارد'))
#
#     return price_list
#
#
# price_filters = price_maker()
#
# # --------------------------------- Area Filter ---------------------------------
# def area_maker():
#     area_list = []
#     for i in range(20, 100, 10):
#         area_list.append((f'{i} - {i+10}', f'{i} تا {i+10} متر'))
#     for i in range(100, 500, 50):
#         area_list.append((f'{i} - {i+50}', f'{i} تا {i+50} متر'))
#     for i in range(500, 1000, 100):
#         area_list.append((f'{i} - {i+100}', f'{i} تا {i+100} متر'))
#     for i in range(1000, 5000, 1000):
#         area_list.append((f'{i} - {i+1000}', f'{i} تا {i+1000} متر'))
#     area_list.append(('5000 - 10000', '5000 تا 10000 متر'))
#     return area_list
#
#
# area_filters = area_maker()
#
#
# # --------------------------------- Age Filter ---------------------------------
# def age_maker():
#     age_list = [('نوساز', 'نوساز')]
#     for i in range(1, 30):
#         age_list.append((f'{i} - {i+1}', f'{i} تا {i+1} سال'))
#     age_list.append(('بیش از 30', 'بیش از 30'))
#     return age_list
#
#
# age_filters = age_maker()
#
#
# # --------------------------------- Level Filter ---------------------------------
# def level_maker():
#     level_list = [('زیر همکف', 'زیر همکف'), ('همکف', 'همکف')]
#     for i in range(1, 30):
#         level_list.append((f'{i} - {i+1}', f'{i} تا {i+1} سال'))
#     level_list.append(('بیش از 30', 'بیش از 30'))
#     return level_list
#
#
# level_filters = level_maker()
#
#
# # --------------------------------- Level Filter ---------------------------------
# def room_maker():
#     room_list = [('no-room', 'بدون اتاق')]
#     for i in range(1, 5):
#         room_list.append((f'{i} - {i+1}', f'{i} تا {i+1} سال'))
#     room_list.append(('more-5', 'بیش از 5'))
#     return room_list
#
#
# room_filters = room_maker()
