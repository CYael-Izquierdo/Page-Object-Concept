from faker import Factory
from faker import Faker
from faker.providers import automotive
from faker.providers import address
from faker.providers import BaseProvider
from pygeocoder import Geocoder
# from uszipcode import ZipcodeSearchEngine
import arrow
import random
from retry import retry
from pygeolib import GeocoderError

fake = Factory.create('en_US')
black_list = ["United States", "Unnamed"]

# COMMONWEALTH/TERRITORIES AR NOT SUPPORTED
us_states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    # 'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    # 'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    # 'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    # 'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    # 'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}


class Person(object):
    def __init__(self, sex='MALE', zip_code=None):
        # Set zip_code for AK as default
        if zip_code is None:
            zip_code = "99540"

        location = Address.generate_location_by_zipcode(zip_code)
        self.address = Address.get_address_by_location(location)
        self.zipcode = location.Zipcode
        self.city = location.City
        self.state_code = location.State
        self.state = us_states[self.state_code]
        self.state_code = self.state_code

        if sex.upper() == 'MALE':
            self.name = fake.name_male()
            self.sex = "M"
        elif sex.upper() == 'FEMALE':
            self.name = fake.name_female()
            self.sex = "F"
        else:
            self.name = fake.first_name()
            self.sex = ""

        self.last_name = fake.last_name()
        self.dob = arrow.utcnow().replace(years=-30).format('MM/DD/YYYY')
        self.phone = fake.phone_number()
        self.ssn = fake.ssn().replace("-", "")
        self.email = str("%s@test.com" % (self.name.replace(" ", ""))).lower()

    def __str__(self):
        return "Name: " + self.name + "\n" + \
               "Last name: " + self.last_name + "\n" + \
               "Sex: " + self.sex + "\n" + \
               "DOB: " + self.dob + "\n" + \
               "Address: " + self.address + "\n" + \
               "Zip: " + self.zipcode + "\n" + \
               "City: " + self.city + "\n" + \
               "State Code: " + self.state_code + "\n" + \
               "State: " + self.state + "\n" + \
               "Phone: " + self.phone + "\n" + \
               "Ssn: " + self.ssn + "00" + "\n" + \
               "Email: " + self.email

    def __as_dict(self):
        return {"effective_date": arrow.utcnow().replace(days=+15).format('MM/DD/YYYY'),
                "first_name": self.name,
                "last_name": self.last_name,
                "sex": self.sex,
                "dob": self.dob,
                "primary_address": self.address,
                "city": self.city,
                "state": self.state_code,
                "zip": self.zipcode,
                "ssn": self.ssn,
                "email": self.email}

    @staticmethod
    def __get_state_by_code(code):
        return us_states.get(code)


class Address():
    @staticmethod
    def generate_location_by_zipcode(zip_code: str):
        with ZipcodeSearchEngine() as search:
            location = search.by_zipcode(zip_code)
        return location

    @staticmethod
    def generate_location_by_state_code(state_code):
        with ZipcodeSearchEngine() as search:
            # By State Code
            locations = search.by_state(state_code)
        return locations

    @staticmethod
    @retry(tries=10, delay=5, max_delay=30, jitter=2)
    # TODO: Check performance
    def get_address_by_location(location: object):

        try:
            location = str(Geocoder.reverse_geocode(location.NEBoundLatitude, location.NEBoundLongitude)).split(",")[0]
        except GeocoderError as e:
            raise Exception(4 * "<" + "[ERROR]" + 4 * ">"
                            + "An error occurred when trying to create a location."
                            + "\nERROR: "
                            + format(e)
                            + "\n")
        return location

    def get_address_by_city_name(self):
        pass

    def get_address_by_zip_code(self):
        pass

    def get_address_by_state(self):
        pass


class Bank:
    def __init__(self):
        self.__bban = fake.bban()
        self.__country = fake.bank_country()
        self.__iban = fake.iban()

    def __str__(self):
        return "Basic Bank Account Number: " + self.__bban + "\n" + \
               "Bank Country: " + self.__country + "\n" + \
               "International Bank Account Number: " + self.__iban + "\n"

    def as_dict(self):
        return {"bban": self.__bban,
                "bank_country": self.__country,
                "iban": self.__iban,
                }

    @staticmethod
    def get_bban():
        return fake.bban()

    @staticmethod
    def get_country():
        return fake.bank_country()

    @staticmethod
    def get_iban():
        return fake.iban()


class Company:
    def __init__(self):
        self.__company_suffix = fake.company_suffix()
        self.__catch_phrase = fake.catch_phrase()
        self.__business = fake.bs()
        self.__company_name = fake.company()

    def __str__(self):
        return "Company Suffix: " + self.__company_suffix + "\n" + \
               "Company Name: " + self.__company_name + "\n" + \
               "Catch Phrase: " + self.__catch_phrase + "\n" + \
               "Business: " + self.__business + "\n"

    def as_dict(self):
        return {"suffix": self.__company_suffix,
                "company_name": self.__company_name,
                "catch_phrase": self.__catch_phrase,
                "business": self.__business
                }

    @staticmethod
    def get_suffix():
        return fake.company_suffix()

    @staticmethod
    def get_catch_phrase():
        return fake.catch_phrase()

    @staticmethod
    def get_business():
        return fake.bs()

    @staticmethod
    def get_name():
        return fake.company()


class CreditCard:
    def __init__(self):
        self.__number = fake.credit_card_number()
        self.__credit_card_full = fake.credit_card_full()
        self.__expire_date = fake.credit_card_expire()
        self.__security_code = fake.credit_card_security_code()

    def __str__(self):
        return "Credit Card Number: " + self.__number + "\n" + \
               "Credit Card Full: " + self.__credit_card_full + "\n" + \
               "Expire Date: " + self.__expire_date + "\n" + \
               "Security Code: " + self.__security_code + "\n"

    def as_dict(self):
        return {"credit_card_number": self.__number,
                "credit_card_full": self.__credit_card_full,
                "expire_date": self.__expire_date,
                "security_code": self.__security_code
                }

    @staticmethod
    def get_card_number(card_type=None):
        return fake.credit_card_number(card_type)

    @staticmethod
    def get_credit_card_full(card_type=None):
        return fake.credit_card_full(card_type)

    @staticmethod
    def get_expire_date(start="now", end="+10y", date_format="%m/%y"):
        """
            Returns a string date in month/year format.
        :param start_date Defaults to "now". Accepts dates like '-10y' or '+10y'
        :param end_date Defaults to 10 years in the future. Accepts dates like '-10y' or '+10y'
        :date_format date_format Defaults to month/year
        :return month/year string
        """
        return fake.credit_card_expire(start=start, end=end, date_format=date_format)

    @staticmethod
    def get_security_code(card_type=None):
        return fake.credit_card_security_code(card_type)


class Generator:
    @staticmethod
    @retry(tries=3)
    def get_person():
        return Person()

    @staticmethod
    @retry(tries=5)
    def get_person_by_zip_code(zip_code):
        return Person(zip_code)

    @staticmethod
    @retry(tries=3)
    def get_person_by_state(state: str):
        """
        Generates a Person object with address based on state_code
        :param state:  State code like "AL" for Alabama
        :return: Person object with address from state_code
        """

        def is_valid_address(word):
            for c in black_list:
                if c in word:
                    return False
            return True

        def is_valid_state_name(state_name):
            for k, v in us_states.items():
                if state_name.capitalize() == v:
                    return k
            return False

        if len(state) == 2:
            locations = Address.generate_location_by_state_code(us_states[state.upper()])
        # By State Name. Fuzzy name search is supported.
        else:
            state_code = is_valid_state_name(state)
            if not state_code:
                raise Exception("[ERROR] INVALID STATE: " + state)

            try:
                locations = Address.generate_location_by_state_code(state)
            except Exception as e:
                print("Exception in get_person_by_state"
                      + "\nERROR: "
                      + format(e))
        while True:
            city = random.choice(locations)
            person = Generator.get_person_by_zip_code(city.Zipcode)
            if is_valid_address(person.address):
                return person
            else:
                raise Exception("Not valid Address: " + person.address)

    @staticmethod
    @retry(tries=3)
    def get_person_by_city_name(city_name: str):
        """
        Get Person instance with address generated according to city name provided
        :param city_name: City name
        :return: Person Object
        """
        with ZipcodeSearchEngine() as search:
            cities = search.by_city(city_name)

        city_name = random.choice(cities)
        person = Generator.get_person_by_zip_code(city_name.Zipcode)

        return person

    @staticmethod
    def generate_text(max_nb_chars=200, ext_word_list=None):
        """
        Generates random text
        :param max_nb_chars: Max number of characters
        :param ext_word_list: External word list can be provided
        :return: Random text with length max_nb_chars
        """
        return fake.text(max_nb_chars, ext_word_list)

    @staticmethod
    def generate_sentence(nb_words=6, ext_word_list=None):
        """
        Generates random sentence
        :param nb_words: Number of words
        :param ext_word_list: External word list can be provided
        :return:
        """
        return fake.sentence(nb_words=nb_words, variable_nb_words=False, ext_word_list=ext_word_list)

    @staticmethod
    def generate_name(localization=None):
        """
        Generates name based in location. For example, it_IT for Italian names. Default: en_US
        :param localization:
        :return: Random name string
        """
        if localization is not None:
            f = Faker(localization)
        else:
            f = Faker()

        return f.name()

    @staticmethod
    def generate_address():
        """
        Generates random address
        :return: Random address string
        """
        return fake.address()

    @staticmethod
    # TODO: Check if plante numbers are valid
    def generate_license_plate_number():
        """
        Generates random license plate number.
        :return: Random plate number string
        """
        return fake.license_plate()

    @staticmethod
    def generate_job():
        return fake.job()

    @staticmethod
    def generate_phone_number():
        return fake.phone_number()

    @staticmethod
    def generate_simple_profile(sex='M'):
        if sex.capitalize() == "Male":
            sex = 'M'
        elif sex.capitalize() == "Female":
            sex = 'F'
        return fake.simple_profile(sex=sex)

    @staticmethod
    def generate_profile(sex='M'):
        if sex.capitalize() == "Male":
            sex = 'M'
        elif sex.capitalize() == "Female":
            sex = 'F'
        return fake.profile(sex=sex)
