from datetime import datetime
import requests
from bs4 import BeautifulSoup


def get_company_data(company_code):
    # Check if corporate ID exists in records
    url = 'http://www.registrucentras.lt/jar/p/index.php?pav=&kod={}&p=1'.format(company_code)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find specific table w/ information about corporate ID holder
    tables = soup.find_all('table', attrs={'bgcolor': '#CCCCCC'})
    if len(tables) > 0:
        # ... if there are tables, return the first one
        return str(tables[0])
    else:
        return None


def get_personal_id(personal_id_string):
    return [int(foo) for foo in personal_id_string]


def get_number(numbers):
    return int(''.join([str(foo) for foo in numbers]))


def get_sum_mod(id_code, values):
    sum = 0
    for i in range(10):
        sum += id_code[i] * values[i]
    return sum % 11


def get_checksum_number(id_code):
    value_set_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    value_set_2 = [3, 4, 5, 6, 7, 8, 9, 1, 2, 3]

    len(value_set_1)

    check_number = get_sum_mod(id_code, value_set_1)
    if check_number != 10:
        return check_number
    else:
        check_number = get_sum_mod(id_code, value_set_2)
        if check_number != 10:
            return check_number
        else:
            return 0


def check_personal_id(id_number):
    year_code = get_number(id_number[1:3])
    month_code = get_number(id_number[3:5])
    day_code = get_number(id_number[5:7])

    # If first digit is between 1 and 6
    if int(id_number[0]) in range(1, 7):
        # If date is in correct format:
        if year_code in range(0, 100) \
                and month_code in range(0, 13) \
                and day_code in range(0, 32):
            # If date is correct:
            if get_birthday(id_number[:7]) is not None:
                # If checksum is correct:
                if id_number[-1] == get_checksum_number(id_number):
                    return True  # ID is correct
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


def get_birthday(id_date_data):
    century_code = id_date_data[0]
    year_code = get_number(id_date_data[1:3])
    month_code = get_number(id_date_data[3:5])
    day_code = get_number(id_date_data[5:7])

    century = 1800 if century_code <= 2 else 1900 if century_code <= 4 else 2000
    year = century + year_code
    if month_code == 0 or day_code == 0:
        return '{0}-{1}-{2}'.format(year,
                                    'N/A' if month_code == 0 else month_code,
                                    'N/A' if day_code == 0 else day_code)
    else:
        # Convert values to a date in order to check if date exists
        # this is especially helpful with dates that are around leap years
        try:
            return datetime(year, month_code, day_code).strftime('%Y-%m-%d')
        except ValueError:
            return None


def get_personal_description(id_code):
    if id_checker(id_code):
        gender = 'Male' if int(id_code[0]) % 2 == 1 else 'Female'
        return '{0} born on {1}'.format(gender, get_birthday(get_personal_id(id_code)))
    else:
        return 'Invalid code!'


def id_checker(personal_id):
    id = get_personal_id(personal_id)
    return check_personal_id(id)


def get_unique_values(all_values):
    return list(dict.fromkeys(all_values))


def get_digits_only(string):
    return ''.join(filter(lambda x: x.isdigit(), string))


def text_sanitizer(text):
    words = text.replace('\n', ' ').split(' ')

    valid_ak = []
    invalid_ak = []
    valid_jak = []
    invalid_jak = []

    for word in words:
        temp = get_digits_only(word)
        if len(temp) == 11:
            if id_checker(temp):
                valid_ak.append(temp)
            else:
                invalid_ak.append(temp)
        elif len(temp) == 7 or len(temp) == 9:
            if get_company_data(temp) is not None:
                valid_jak.append(temp)
            else:
                invalid_jak.append(temp)
    return {
        'valid_ak': get_unique_values(valid_ak),
        'invalid_ak': get_unique_values(invalid_ak),
        'valid_jak': get_unique_values(valid_jak),
        'invalid_jak': get_unique_values(invalid_jak)
    }
