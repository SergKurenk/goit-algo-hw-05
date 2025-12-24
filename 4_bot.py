import re

def input_error_decorator(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Контакт не знайдено. Будь ласка, перевірте правильність введеного імені."
        except IndexError:
            return "Недостатньо параметрів для виконання команди. Будь ласка, додайте необхідні аргументи."
        except ValueError:
            return "Недостатньо значень для виконання команди. Додайте будь ласка Ім'я та номер телефону."
    return inner

def parse_input(user_input: str):
    if user_input.strip() == "":
        return "", []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def show_contacts(contacts:dict[str, str]):
    if len(contacts) == 0:
        return "Список контактів порожній."
    result = "Контакти:\n"
    for name, phone in contacts.items():
        result += f"{name}: {phone}\n"
    return(result.strip())

def check_phone(phone: str) -> bool:
    match = re.match(r'^\+?\d{7,15}$', phone)
    return match is not None

@input_error_decorator 
def change_contact(contacts:dict[str, str], *param) -> str:
    name = param[0]
    phone = param[1]
    if name in contacts:
        if check_phone(phone):
            contacts[name] = phone
            return("Контакт оновлено.")
        else:
            return("Невірний формат номера телефону.")
    else:
        return("Контакт не знайдено.")

@input_error_decorator
def add_contact(contacts:dict[str, str], *param) -> str:
    name, phone = param
    contacts[name] = phone
    return("Контакт додано.")

@input_error_decorator
def del_contact(contacts:dict[str, str], *param) -> str:
    name = param[0]
    if name in contacts:
        del contacts[name]
        return("Контакт видалено.")
    else:
        return("Контакт не знайдено.") 

@input_error_decorator
def show_phone(contacts:dict[str, str], *param) -> str:
    name = param[0]
    return contacts.get(name, "Контакт не знайдено.")

def main():
    cmd = ""
    contacts = {}
    print('Welcome to the assistant bot!')
    while True:
        cmd, *param = parse_input(input("Ведіть команду: "))

        match cmd:
            case "exit":
                print("Бувай!")
                break
            case "add":
                print(add_contact(contacts, *param))
            case "change":
                print(change_contact(contacts, *param))
            case "phone":
                print(show_phone(contacts), *param)
            case 'all':
                print(show_contacts(contacts))
            case 'del':
                print(del_contact(contacts, *param))
            case "hello":
                print("Чим я можу вам допомогти?")
            case "help":
                print("Список всіх команд:")
                print("hello - привітання")
                print("add <ім'я> <номер телефону> - додати новий контакт")
                print("change <ім'я> <номер телефону> - змінити існуючий контакт")
                print("phone <ім'я> - показати номер телефону контакта")
                print("all - показати всі контакти")
                print("del <ім'я> - видалити контакт")
                print("exit - закрити чат")
            case "":
                print("Будь ласка, введіть команду. Для списку команд введіть 'help'.")
            case _:
                print("Вибачте, я не знаю таку команду.")

if __name__ == "__main__":
    main()

