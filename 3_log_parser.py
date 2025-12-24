import sys

def parse_log_line(line: str) -> dict: #для парсингу рядків логу
#приймає рядок з логу як вхідний параметр і повертає словник з розібраними компонентами: дата, час, рівень, повідомлення. Використовуйте методи рядків, такі як split(), для розділення рядка на частини.
    dictionary = {}
    splitted = line.split(" ")
    if len(splitted) < 4:
        return {}
    dictionary["date"] = splitted[0]
    dictionary["time"] = splitted[1]
    dictionary["level"] = splitted[2]
    dictionary["message"] = " ".join(splitted[3:])
    #print(dictionary)
    return dictionary

def load_logs(file_path: str) -> list: #для завантаження логів з файлу
    #відкриває файл, читає кожен рядок і застосовує до нього функцію parse_log_line, зберігаючи результати в список
    try:
        fh = open(file_path, "r")
        parsed_list = [parse_log_line(el.strip()) for el in fh.readlines()]
    except FileNotFoundError:
        print(f"Файл за шляхом {file_path} не знайдено.")
        return []
    except IOError:
        print(f"Помилка при читанні файлу {file_path}.")
        return []
    finally:
        fh.close()
    return parsed_list

def filter_logs_by_level(logs: list, level: str) -> list: #для фільтрації логів за рівнем.
    #Вона дозволить вам отримати всі записи логу для певного рівня логування
    return [log for log in logs if log["level"] == level]

def count_logs_by_level(logs: list) -> dict: #для підрахунку записів за рівнем логування.
    #проходить по всім записам і підраховує кількість записів для кожного рівня логування.
    counts = {}
    for log in logs:
        level = log["level"]
        counts[level] = counts.get(level, 0) + 1
    return counts

def display_log_counts(counts: dict): #яка форматує та виводить результати. Результати мають бути представлені у вигляді таблиці з кількістю записів для кожного рівня
#Вона приймає результати виконання функції count_logs_by_level
    print("Рівень логування | Кількість")
    print("-----------------|----------")
    for level, count in counts.items():
        print(f"{level:<16} | {count}")

#Ваш скрипт повинен вміти обробляти різні види помилок, такі як відсутність файлу або помилки при його читанні. Використовуйте блоки try/except для обробки виняткових ситуацій.

def main():
    path = ""
    if len(sys.argv) > 1:
        path = sys.argv[1]  #command line
    else:
        path = "./log.txt"   #debug only
    
    loaded_logs = load_logs(path)
    if not loaded_logs:
        return
    count_logs_by_level(loaded_logs)
    display_log_counts(count_logs_by_level(loaded_logs))

    if len(sys.argv) == 3:
        level = sys.argv[2].upper()
        if level not in ["INFO", "DEBUG", "ERROR", "WARNING"]:
            print(f"Невідомий рівень логування: {level}")
            return
        filtered_logs = filter_logs_by_level(loaded_logs, level)
        print(f"\nДеталі логів для рівня '{level}':")
        for log in filtered_logs:
            print(f"{log['date']} {log['time']} - {log['message']}")

if __name__ == "__main__":
    main()

# Простий запуск з одним параметром - шляхом до файлу логу.
# Рівень логування | Кількість
# -----------------|----------
# INFO             | 4
# DEBUG            | 3
# ERROR            | 2
# WARNING          | 1

#Запуск з двома параметрами - шляхом до файлу логу та рівнем логування (наприклад, ERROR), виводить всі записи логу з цим рівнем.
# Рівень логування | Кількість
# -----------------|----------
# INFO             | 4
# DEBUG            | 3
# ERROR            | 2
# WARNING          | 1

# Деталі логів для рівня 'ERROR':
# 2024-01-22 09:00:45 - Database connection failed.
# 2024-01-22 11:30:15 - Backup process failed.
