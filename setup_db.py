import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('chat.db')
cursor = connection.cursor()

# Создаем таблицу msg
cursor.execute('''
CREATE TABLE IF NOT EXISTS msg (
username TEXT NOT NULL,
message TEXT NOT NULL
)
''')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()
print("Таблица чата создана")