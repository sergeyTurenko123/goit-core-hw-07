from collections import UserDict, UserList
import datetime  as dt
from datetime import datetime  as dtdt

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
class Name(Field):
    def __init__(self, value):
        if value[0].isupper():
            self.value = value
        else:
            raise ValueError("Incorect Name")
class Phone(Field):
    def __init__(self, value):
        if len(value) == 10:
            self.value = value
        else:
            raise ValueError ("Incorect Phone")

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = dtdt.strptime(value, "%Y-%m-%d").date()  # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
 
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
            
    def remove_phone(self, phone):
        p = self.find_phone(phone)
        self.phones.remove(p)
            
    def edit_phone(self, old_phone, new_phone):
        number = self.find_phone(old_phone)
        if number:
            self.add_phone(new_phone)
            self.remove_phone(old_phone)
        else:
            raise ValueError

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"    

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        for names, record in self.data.items():
            if name in names:
                return self.data[name]
            
    def delete(self, name):
        user = self.find(name)
        del user
    
    def get_upcoming_birthdays(self):
        now = dtdt.today().date() #поточний час
        birthday = []
        for user in self.data:
            date_user = user[2] 
            date_user = str(now.year) + date_user[4: ]
            date_user = dtdt.strptime(date_user, "%Y-%m-%d").date() #парсинг дати
            week_day = date_user.isoweekday()
            difference_day = (date_user - now).days
            if 1 < difference_day < 7 :
                if difference_day < 6 :
                    birthday.append({"name": user["name"], "birthday":date_user.strftime("%Y-%m-%d")})
                else:
                    if difference_day == 7:
                        birthday.append({"name": user["name"], "birthday":(date_user + dt.timedelta(days = 1)).strftime("%Y-%m-%d")})
                    elif difference_day == 6:
                        birthday.append({"name": user["name"], "birthday":(date_user + dt.timedelta(days = 2)).strftime("%Y-%m-%d")})
        return birthday

def parse_input(user_input):
    name, *args = user_input.split()
    name = name.strip().lower()
    return name, *args


def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    name_phone = book.find(name)
    name_phone.edit_phone(old_phone, new_phone)
    message = "Number changed."
    return message

def show_phone(args, book: AddressBook):
    name, *_ = args
    return book.find(name)

def show_all(book: AddressBook):
    for name, record in book.data.items():
        print(record)
    pass

def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    message = "Date of birth updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Date of birth added."
    record.add_birthday(birthday)
    return message

def show_birthday(args, book: AddressBook):
    name, *_ = args
    return book.find(name)

def birthdays(book: AddressBook):
    return book.get_upcoming_birthdays()

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add_birthday":
            print(add_birthday(args, book))
        elif command == "show":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book)) 
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
    
# # Створення запису для John
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")
     
# # Створення нової адресної книги
# book = AddressBook()

# # Додавання запису John до адресної книги               
# book.add_record(john_record)
    
#     # Створення та додавання нового запису для Jane
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# book.add_record(jane_record)

#     # Виведення всіх записів у книзі
# # for name, record in book.data.items():
# #     print(record)


# #     # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")   

# print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

#      # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

#    # Видалення запису Jane
# book.delete("Jane")


