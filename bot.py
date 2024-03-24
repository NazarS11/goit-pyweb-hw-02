import pickle
from datetime import datetime as dtdt
from datetime import timedelta as td
from classes import AddressBook, Record, MessageBot

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
           return "Enter the argument for the command."
        except KeyError:
            return "No such contact in the list."
        except TypeError as e:
            return f"Error: {e}"
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(address_book, name, phone):
    try:
        record = address_book.find(name)
        if not record:
            record = Record(name)
            address_book.add_record(record)
            record.add_phone(phone)
            return record
        else:
            record.add_phone(phone)
            return record
    except ValueError as e:
        return f"Error: {e}"

@input_error
def change_phone(address_book, name, old_phone, new_phone):
    try:
        existing_contact = address_book.find(name)
        if existing_contact:
            existing_contact.edit_phone(old_phone, new_phone)
            return f"Successfully changed"
        else:
            return f"{name} contact is not in the address book"
    except ValueError as e:
        return f"Error: {e}"

@input_error
def add_birthday(address_book, name, birthday):
    try:
        existing_contact = address_book.find(name)
        if existing_contact:
            existing_contact.add_birthday(birthday)
            return f"Name: { existing_contact.name.value}, Birthday: {existing_contact.birthday}"
        else:
            return f"{name} contact is not in the address book"
    except ValueError as e:
        return f"Error: {e}"

@input_error
def delete_phone(address_book, name, phone):
    try:
        existing_contact = address_book.find(name)
        if existing_contact:
            if existing_contact.find_phone(phone):
                existing_contact.remove_phone(phone)
                return f"{phone} phone number is successfully deleted from {existing_contact.name.value} contact"
            else: 
                return f"{existing_contact.name.value} contact has no added {phone} phone number"
        else:
            return f"{name} contact is not in the address book"
    except ValueError as e:
        return f"Error: {e}"

@input_error
def show_birthday(address_book, name):
    existing_contact = address_book.find(name)
    if existing_contact:
        return f"Name: { existing_contact.name.value}, Birthday: {existing_contact.birthday}"
    else:
        return f"{name} contact is not in the address book"

@input_error
def show_phone(address_book, name):
    existing_contact = address_book.find(name)
    if existing_contact:
        width = max(len(existing_contact.name.value),4) + 2
        header = '{:<{w}}|{:<10}'.format('Name','Phone',w = width) + '\n' + '-' * width + '|' + '-' * 10
        result = header + '\n' + "\n".join(map(lambda phone: '{:<{w}}|{:<10}'.format(existing_contact.name.value,phone.value,w = width), existing_contact.phones))
        return result
    else:
        return f"{name} contact is not in the address book"

@input_error
def display_contacts(address_book):
    if address_book:
        return address_book
    else: 
        return f"Address book is empty"

@input_error
def show_birthdays(address_book):
    today = dtdt.now().date()
    congrat_list = []
    for name, record in address_book.data.items():
        if record.birthday:
            birthday = record.birthday.value
            latest_birth_date = dtdt(today.year, birthday.month, birthday.day).date()
            if today < latest_birth_date and (latest_birth_date - today).days < 8:
                if latest_birth_date.weekday() == 6:
                    congrat_list.append({'name':name,'congratulation_date':(latest_birth_date + td(days=1)).strftime("%Y.%m.%d")})
                elif latest_birth_date.weekday() == 5:
                    congrat_list.append({'name':name,'congratulation_date':(latest_birth_date + td(days=2)).strftime("%Y.%m.%d")})
                else:
                    congrat_list.append({'name':name,'congratulation_date':latest_birth_date.strftime("%Y.%m.%d")})
        else: continue
    result = ""
    result = "\n".join(map(lambda record: f"{record['name']} should be congratulated at {record['congratulation_date']}", congrat_list))
    return result

def delete_contact(address_book,name):
    existing_contact = address_book.find(name)
    if existing_contact:
        address_book.delete(name)
        return f"{name} contact is successfully deleted"
    else:
        return f"{name} contact is not in the address book"

    
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        return pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


@input_error
def main():
    book = load_data()
    bot = MessageBot()
    bot.message("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            bot.message("Good bye!")
            break
        elif command == "hello":
            bot.message("How can I help you?")
        elif command == "add":
            bot.message(add_contact(book, *args))
        elif command == "delete-phone":
            bot.message(delete_phone(book, *args)) 
        elif command == "change":
            bot.message(change_phone(book, *args))
        elif command == "add-birthday":
            bot.message(add_birthday(book, *args))
        elif command == "show-birthday":
            bot.message(show_birthday(book, *args))
        elif command == "phone":
            bot.message(show_phone(book, *args))
        elif command == "birthdays":
            bot.message(show_birthdays(book))        
        elif command == "all":
            bot.message(display_contacts(book))
        elif command == "delete-contact":
            bot.message(delete_contact(book, *args))
        elif command == "help":
            bot.message(bot.help())  
        else:
            bot.message("Invalid command.")


if __name__ == '__main__':
    main()