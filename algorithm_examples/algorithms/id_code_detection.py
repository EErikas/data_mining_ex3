from datetime import datetime
import requests
from bs4 import BeautifulSoup


# Corporate IDs:
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


# ---------------------------------------------------------------------------------------------------
# Personal IDs:

def get_int_list(personal_id_string):
    return [int(foo) for foo in personal_id_string]


def get_int_from_int_list(numbers):
    return numbers[0] * 10 + numbers[1]


def get_sum_mod(id_code, values):
    return sum([foo * bar for foo, bar in zip(id_code[:10], values)]) % 11


def get_checksum_number(id_code):
    value_set_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    value_set_2 = [3, 4, 5, 6, 7, 8, 9, 1, 2, 3]

    check_number = get_sum_mod(id_code, value_set_1)
    if check_number != 10:
        return check_number
    else:
        check_number = get_sum_mod(id_code, value_set_2)
        if check_number != 10:
            return check_number
        else:
            return 0


def check_personal_id(id_number, block_exceptions=False):
    month_code = get_int_from_int_list(id_number[3:5])
    day_code = get_int_from_int_list(id_number[5:7])
    # First digit can be from 1 to 6:
    is_first_digit_correct = int(id_number[0]) in range(1, 7)
    # Date digits must be in a right range
    # Note: there is an exception when a person cannot remember their month or day of birth
    # in such cases the corresponding digits are replaced by 0s
    # By default these exceptions are allowed, but can be disabled, therefore variable block_exceptions is used
    # Since it is a bool value it can be interpreted as 0 or 1 so it is used in range accordingly:
    # False means range starts from 0, True means it starts from 1
    is_date_format_correct = month_code in range(block_exceptions, 13) and day_code in range(block_exceptions, 32)

    is_date_correct = get_birthday(id_number[:7]) is not None
    is_check_number_correct = id_number[-1] == get_checksum_number(id_number)

    # Method returns True if all requirements are met:
    return is_first_digit_correct and is_date_format_correct and is_date_correct and is_check_number_correct


def get_birthday(id_date_data):
    century_code = id_date_data[0]
    year_code = get_int_from_int_list(id_date_data[1:3])
    month_code = get_int_from_int_list(id_date_data[3:5])
    day_code = get_int_from_int_list(id_date_data[5:7])

    century = 1800 if century_code <= 2 else 1900 if century_code <= 4 else 2000
    year = century + year_code
    if month_code == 0 or day_code == 0:
        return '{0}-{1}-{2}'.format(year,
                                    'N/A' if month_code == 0 else month_code,
                                    'N/A' if day_code == 0 else day_code)
    else:
        # Convert values to a date in order to check if date exists
        # this is especially helpful when working with leap years
        try:
            return datetime(year, month_code, day_code).strftime('%Y-%m-%d')
        except ValueError:
            return None


def get_personal_description(id_code):
    id_code_as_int_list = get_int_list(id_code)
    if check_personal_id(id_code_as_int_list):
        gender = 'Male' if int(id_code[0]) % 2 == 1 else 'Female'
        return '{0} born on {1}'.format(gender, get_birthday(id_code_as_int_list))
    else:
        return 'Invalid code!'


# ---------------------------------------------------------------------------------------------------
# Detect IDs from given text:
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
            id_code = get_int_list(temp)
            if check_personal_id(id_code):
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
