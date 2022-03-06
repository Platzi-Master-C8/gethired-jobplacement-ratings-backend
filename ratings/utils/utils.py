import random
import functools
import operator
import smtplib
import os

# Dotenv
from dotenv import load_dotenv

load_dotenv()

SMTP_PORT = os.getenv("SMTP_PORT")
USER_EMAIL = os.getenv("USER_EMAIL")
USER_EMAIL_PASSWORD = os.getenv("USER_EMAIL_PASSWORD")


from typing import List


class Util:
    def create_tracking_code() -> str:
        MAYUS = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "X",
            "Y",
            "Z",
        ]

        NUMS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

        characters = MAYUS + NUMS

        tracking_code: List = []

        for i in range(8):
            random_character = random.choice(characters)
            tracking_code.append(random_character)

        tracking_code = "".join(tracking_code)

        return tracking_code

    def assign_weight(companion_evaluation_criteria: str) -> int:
        """Return the convertion of a string company evaluation in it's equivalent to a weight

        Args:
            companion_evaluation_criteria (str): Criteria of of the company evaluation to be evaluated

        Returns:
            int: Weight assigned
        """
        weight_assigned = 0

        if companion_evaluation_criteria == "Good":
            weight_assigned = 5
        elif companion_evaluation_criteria == "Regular":
            weight_assigned = 3
        elif companion_evaluation_criteria == "Bad":
            weight_assigned = 1

        return weight_assigned

    def round_values(amount, number_of_decimals=1):
        result = round(amount, number_of_decimals)
        return result

    def tranform_tuple_in_string(tuple: tuple) -> str:
        """Tansforma  tuple in a string

        Args:
            tuple (tuple): A tuple

        Returns:
            str: the tuple converted into string
        """
        return functools.reduce(operator.add, (tuple))

    def send_offer_tracking_email(user_email:str,tracking_code:str, paternal_last_name:str):
        """Send the tracking code per applicantion realized by user

        Args:
            user_email (str): Email of the applicant
            tracking_code (str): Tracking code of the application of the vacancy
            paternal_last_name (str): Applicant's paternal last name

        Returns:
            str: Status of the sending message
        """
        
        subject = 'Employment application at get-hired.work'
        user_email = user_email
        tracking_code = tracking_code
        last_name = paternal_last_name
        get_hired_page = 'https://get-hired.work/'
        preference_message = 'The get-hired team thanks you for your preference.' 
        instructions = f'To follow up on your application we invite you to go to our home page {get_hired_page} and click on the "status of my offer" button by entering your application tracking number and your last name attached to this message:'
        
        
        message ='Subject: {}\n\n{}\n\n{}\n\n Tracking Code: {}\n Last name: {}'.format(subject,preference_message,instructions,tracking_code,last_name)
        
        server = smtplib.SMTP("smtp.gmail.com", port=SMTP_PORT)
        server.starttls()
        server.login(USER_EMAIL,USER_EMAIL_PASSWORD)
        
        server.sendmail(USER_EMAIL, f'{user_email}', message)
        server.quit()
        
        return 'Message Sended'