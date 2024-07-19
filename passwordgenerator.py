import random
import string
import argparse
import sqlite3
from prettytable import PrettyTable


numbers = string.digits
letters = string.ascii_lowercase + string.ascii_uppercase
specialcharacters = "[$&+=?@#<>^*()%!]"
symbols = list(numbers + letters + specialcharacters)
# список, содержащий всевозможные символы для создания пароля

def generator(length):
    password = ''.join(random.choices(symbols, k=length))
    return password
# функция генерации паролей

def save_password(password, service):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, password TEXT, service TEXT)''')
    cursor.execute('''INSERT INTO passwords (password, service) VALUES (?, ?)''', (password, service))
    conn.commit()
    conn.close()
# с помощью базы данных мы сохраняем наши сгенерированные пароли, создав таблицу с паролями и сервисами

def display_passwords():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM passwords''')
    rows = cursor.fetchall()
    conn.close()

    table = PrettyTable(["ID", "Password", "Service"])
    for row in rows:
        table.add_row(row)
    print(table)

# отображаем наши сохраненные пароли с помощью PrettyTable

def remove_password(row_id):
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM passwords WHERE id = ?''', (row_id,))
    conn.commit()
    conn.close()

# удаление паролей с заданным id

def main():
    parser = argparse.ArgumentParser(prog='Password generator', description='Программа для генерации пароля')
    parser.add_argument('-l', '--length', type=int, help='Длина желаемого пароля', required=False)
    parser.add_argument('-s', '--service', type=str, help='Название сервиса для пароля', required=False)
    parser.add_argument('-d', '--display', action='store_true', help="Отобразить сохраненные пароли")
    parser.add_argument('-r', '--remove', type=int, help='Удалить пароль с указанным id', required=False)
    args = parser.parse_args()

    if args.display:
        display_passwords()
    elif args.remove:
        remove_password(args.remove)
        print(f'Пароль с ID {args.remove} успешно удален')
    else:
        password = generator(args.length)
        save_password(password, args.service)
        print(f'Сгенерированный пароль для {args.service}: {password}')

if __name__ == '__main__':
    main()
