from faker import Faker
from random import choice
import pandas as pd
import json
from log import logger


faker = Faker()


# create fake usernames

def generate_random_mobile_phone():
    """
    :param
    :return: random Egypt mobile number
    """
    operator = choice(['010', '012', '011', '015'])
    reset_of_number = ''
    for i in range(8):  # 8 digits reset of number (unless operator)
        digit = choice('0123456789')
        reset_of_number += digit
    return '+2' + operator + reset_of_number


def seed():
    """
        :param
        :return: list of random users profiles
    """
    logger.info('Starting generating fake data for testing')
    users = []
    for i in range(5):
        user = {}
        title = choice(['mr.', 'mrs.'])
        fullname = faker.name().split()
        fname = fullname[0]
        lname = fullname[-1]
        email = faker.email()
        password = faker.password()
        # dob = faker.date_of_birth().strftime('%Y-%B-%d')
        dob = faker.date_of_birth().strftime('%Y-%m-%d')
        company = faker.company()
        address = faker.address().replace('\n', ' ')
        city = faker.city()
        postalcode = faker.postcode()
        phone = generate_random_mobile_phone()
        user['title'] = title
        user['fname'] = fname
        user['lname'] = lname
        user['email'] = email
        user['password'] = password
        user['dob'] = dob
        user['company'] = company
        user['address'] = address
        user['city'] = city
        user['postalcode'] = postalcode
        user['phone'] = phone
        users.append(user)
    logger.info(f'Ending generating fake data for testing with "{len(users)}" users')

    return users


def export_to_json(usrs):
    """
    :param usrs: list of users , [{}, {}, {}]
    :return:
    """
    logger.info('Starting exporting to json')
    json.dump(usrs, open('users.json', 'w'), indent=4, sort_keys=True)
    logger.info('Ending exporting to json')


def export_to_excel(usrs):
    """
    :param usrs: list of users , [{}, {}, {}]
    :return: random dataframe for user
    """
    logger.info('Starting exporting to excel')
    users_df = pd.DataFrame(usrs)
    users_df.index += 1             # start counter from 1
    users_df.index.names = ['No.']  # rename index to 'No.'
    users_df.to_excel('users.xlsx')
    logger.info('Ending exporting to json')
    return users_df


users = seed()
export_to_json(users)
export_to_excel(users)