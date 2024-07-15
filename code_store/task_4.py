"""
Description: This module contains functions for a simple contact list application.
"""

import re
import json
from functools import wraps


def input_error(handler):
    """
    This decorator handles user input errors and exceptions.
    """
    @wraps(handler)
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except KeyError:
            print("The contact does not exist. Try again.")
        except ValueError:
            print("The name or phone number is missing.")
        except (IndexError, TypeError):
            print("Invalid input. Please check your command format.")
    return wrapper


def hello(arg: tuple = None) -> None:
    """
    This function prints a greeting message.
    """
    print("How can I help you?")

def load_contacts(filename: str = 'contacts.json') -> dict:
    """
    This function loads contacts from a file.
    :param filename: str
    :return: dict
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_contacts(contacts_dict: dict, filename: str = 'contacts.json') -> None:
    """
    This function saves contacts to a file.
    :param contacts_dict: dict
    :param filename: str
    :return: None
    """
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(contacts_dict, file, ensure_ascii=False, indent=4)


def validate_phone(phone: str) -> str:
    """
    Normalize a phone number to the format +38XXXXXXXXXX.
    Args:
        phone_number (str): The phone number to normalize.
    Returns:
        str: The normalized phone number.
    """
    
    cleaned_number = re.sub(r'\D', '', phone)
    if len(cleaned_number) < 10:
        raise TypeError("Phone number must consist of digits and be at least 10 digits long.")
    
    civil_number = cleaned_number[-10:]
    country_code = "+38"
    result = country_code + civil_number
    
    return result

@input_error
def add_contact(args: tuple, filename: str = 'contacts.json') -> None:
    """
    This function adds a contact to the contacts list.
    :param args: tuple
    :param filename: str
    :return: None
    """
    if len(args) == 2:
        name, phone = args
        phone = validate_phone(phone)
        contacts = load_contacts(filename)
        contacts[name] = phone
        save_contacts(contacts, filename)
        print("Contact added.")
    else:
        raise ValueError


@input_error
def change_contact(args: tuple, filename: str = 'contacts.json') -> None:
    """
    This function changes a contact's phone number.
    :param args: tuple
    :param filename: str
    :return: None
    """
    if len(args) == 2:
        name, phone = args
        phone = validate_phone(phone)
        contacts = load_contacts(filename)
        if name in contacts:
            contacts[name] = phone
            save_contacts(contacts, filename)
            print("Contact updated.")
        else:
            raise KeyError
    else:
        raise ValueError


@input_error
def show_phone(args: tuple, filename: str = 'contacts.json') -> None:
    """
    This function shows a contact's phone number.
    :param args: tuple
    :param filename: str
    :return: None
    """
    if len(args) == 1:
        name = args[0]
        contacts = load_contacts(filename)
        if name in contacts:
            print(f"{name}'s phone number is {contacts[name]}")
        else:
            raise KeyError
    else:
        raise ValueError


def show_all_contacts(filename: str = 'contacts.json') -> None:
    """
    This function shows all contacts.
    :param filename: str
    :return: None
    """
    contacts = load_contacts(filename)
    if contacts:
        for name, phone in contacts.items():
            print(f"{name}: {phone}")
    else:
        print("No contacts found.")

@input_error
def parse_input(user_input: str) -> tuple:
    """
    This function parses user input.
    :param user_input: str
    :return: tuple
    """
    parts = user_input.strip().split()
    command = parts[0].lower()
    args = parts[1:]
    
    return command, args


def main_contact_bot(filename: str = 'contacts.json'):
    """
    Main function to run the assistant bot.
    :param filename: str, path to the file with contacts
    """
    print("Welcome to the assistant bot!")

    command_dict = {
        'hello': hello,
        'add': lambda args: add_contact(args, filename),
        'change': lambda args: change_contact(args, filename),
        'phone': lambda args: show_phone(args, filename),
        'all': lambda args: show_all_contacts(filename),
    }

    while True:
        user_input = input("Enter a command: ")
        if user_input.strip() == "":
            print("Invalid command. Try again.")
            continue
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        else:
            if command in command_dict:
                command_dict[command](args)
            else:
                print("Invalid command. Try again.")
