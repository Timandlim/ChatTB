import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('chat.db')
cursor = connection.cursor()

# Отчищаем таблицу
cursor.execute('''
DELETE FROM msg
''')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()
print("Таблица чата отчищена")