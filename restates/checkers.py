min_file_price = 1000000000  # TOOMAN
max_file_price = 1000000000000  # TOOMAN
min_area = 20  # m2
max_area = 100000  # m2


def file_price_checker(price):
    if min_file_price <= price <= max_file_price:
        return True


def area_checker(area):
    if min_area <= area <= max_area:
        return True


def phone_checker(phone):
    try:
        if len(phone) == 11 and int(phone) and phone[0:2] == '09' and phone[2] in ['0', '1', '2', '3']:
            return True
    except ValueError:
        return False


def postal_code_checker(code):
    try:
        if len(code) == 10 and int(code):
            return True
    except ValueError:
        return False


def national_code_checker(code):
    try:
        if len(code) == 10 and int(code):
            number = 0
            for i in range(1, len(code)):
                number += (i + 1) * int(code[-(i + 1)])

            if number % 11 >= 2:
                control = 11 - number % 11
            else:
                control = number % 11

            if control == int(code[9]):
                print('ass')
                return True
            else:
                print('pussy')
                return False

    except ValueError:
        print('cock')
        return False


