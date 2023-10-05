'''Create random data for account creation for digital'''
import random

first_names = ['Harpreet', 'John', 'Jane', 'Corey', 'Travis', 'Dave', 'Kurt', 'Neil', 'Sam', 'Steve', 'Tom', 'James',
               'Robert', 'Michael', 'Charles', 'Joe', 'Mary', 'Maggie', 'Nicole', 'Patricia', 'Linda', 'Barbara',
               'Elizabeth', 'Laura', 'Jennifer', 'Maria']

last_names = ['Dhillon', 'Smith', 'Doe', 'Jenkins', 'Robinson', 'Davis', 'Stuart', 'Jefferson', 'Jacobs', 'Wright',
              'Patterson', 'Wilks', 'Arnold', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson',
              'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin']

street_names = ['Main', 'High', 'Pearl', 'Maple', 'Park', 'Oak', 'Pine', 'Cedar', 'Elm', 'Washington', 'Lake', 'Hill']

fake_cities = ['Metropolis', 'Eerie', "King's Landing", 'Sunnydale', 'South Park', 'Atlantis', 'Mordor', 'Olympus',
               'Balmora', 'Gotham', 'Springfield', 'Quahog', 'Smalltown', 'Pythonville', 'Faketown', 'Westworld',
               'Thundera', 'Vice City', 'Blackwater', 'Oldtown', 'Valyria', 'Winterfell', 'Braavos‎', 'Lakeview']

for num in range(1):
    first = random.choice(first_names)
    last = random.choice(last_names)

    phone = f'{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}'
    print(phone)

    street_num = random.randint(100, 999)
    street = random.choice(street_names)
    city = random.choice(fake_cities)

    zip_code = random.randint(10000, 99999)
    address = f'{street_num} {street} St., {city} CA'

    email = first.lower() + last.lower() + '@gmail.com'

    # print(f'{first} {last}\n{phone}\n{address}\n{email}\n')
