import psycopg2

class DataConnect:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        try:
            self.connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cursor = self.connection.cursor()
            # Создаём таблицу контактов, если её нет
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    phone VARCHAR(20) NOT NULL
                )
            """)
            self.connection.commit()
            print("Подключение к базе прошло успешно!")
        except Exception as e:
            print("Ошибка подключения к базе:", e)
            print("\nПроверьте, что PostgreSQL запущен и слушает порт 5432.")
            print("Если используете XAMPP/WAMP/PostgreSQL, откройте панель управления и включите сервер.\n")
            exit()  # Выходим из программы, если нет подключения

    def add_contact(self, name, phone):
        query = "INSERT INTO contacts (name, phone) VALUES (%s, %s)"
        self.cursor.execute(query, (name, phone))
        self.connection.commit()
        print(f"Контакт {name} добавлен!")

    def list_contacts(self):
        self.cursor.execute("SELECT id, name, phone FROM contacts")
        return self.cursor.fetchall()

    def delete_contact(self, contact_id):
        self.cursor.execute("DELETE FROM contacts WHERE id=%s", (contact_id,))
        self.connection.commit()
        print("Контакт удалён!")

    def close(self):
        self.cursor.close()
        self.connection.close()


# ====== Твои данные для подключения ======
db = DataConnect(
    dbname='n71_smss',  # имя базы данных
    user='n71_sms',     # логин
    password='123'      # пароль
)

# ====== Функция для отправки SMS ======
def send_sms():
    contacts = db.list_contacts()
    if not contacts:
        print("Список контактов пуст!")
        return

    print("Контакты:")
    for c in contacts:
        print(f"{c[0]}. {c[1]} ({c[2]})")

    try:
        contact_id = int(input("Выберите контакт для отправки SMS (ID): "))
    except ValueError:
        print("Неверный ввод!")
        return

    selected = [c for c in contacts if c[0] == contact_id]
    if not selected:
        print("Контакт не найден!")
        return

    message = input(f"Введите сообщение для {selected[0][1]}: ")
    print(f"SMS для {selected[0][1]} ({selected[0][2]}): {message}")


# ====== Главное меню ======
def main():
    while True:
        print("\nSMS Manager")
        print("1. Добавить контакт")
        print("2. Отправить SMS")
        print("3. Удалить контакт")
        print("4. Выйти")

        choice = input("Выберите действие: ")
        if choice == "1":
            name = input("Имя контакта: ")
            phone = input("Телефон контакта: ")
            db.add_contact(name, phone)
        elif choice == "2":
            send_sms()
        elif choice == "3":
            contacts = db.list_contacts()
            if not contacts:
                print("Список контактов пуст!")
                continue
            print("Контакты:")
            for c in contacts:
                print(f"{c[0]}. {c[1]} ({c[2]})")
            try:
                contact_id = int(input("Введите ID контакта для удаления: "))
            except ValueError:
                print("Неверный ввод!")
                continue
            db.delete_contact(contact_id)
        elif choice == "4":
            print("Выход...")
            db.close()
            break
        else:
            print("Неверный выбор!")

if __name__== "__main__":
    main()