#Получаем библеотеки
import asyncio
import sqlite3
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async
online_users = set()
con = sqlite3.connect("chat.db")
cur = con.cursor()
cur.execute("select * from msg")
chat_msgs = cur.fetchall()


async def main():
    global chat_msgs

    put_markdown("Демо Чат от ТБ")

    msg_box = output()
    put_scrollable(msg_box, height=400, keep_bottom=True)

    nickname = await input("Войти в чат", required=True, placeholder="Ваше имя",
                           validate=lambda n: "Такой ник уже используется!" if n in online_users or n == '📢' else None)
    online_users.add(nickname)

    refresh_task = run_async(refresh_msg(nickname, msg_box))

    while True:
        data = await input_group("", [
            input(placeholder="Текст сообщения ...", name="msg"),
            actions(name="cmd", buttons=["Отправить"])
        ], validate=lambda m: ('msg', "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m['msg'] else None)

        if data is None:
            break

        msg_box.append(put_markdown(f"`{nickname}`: {data['msg']}"))
        new_msg(nickname, data['msg'])

    refresh_task.close()


def new_msg(n, m):
    global chat_msgs
    cur.execute("insert into msg (username, message) values (?,?)", (n, m))
    con.commit()
    chat_msgs.append((n, m))


async def refresh_msg(nickname, msg_box):
    global chat_msgs
    last_idx = 0

    while True:
        await asyncio.sleep(1)

        for m in chat_msgs[last_idx:]:
            last_idx += 1
            if m[0] != nickname:  # if not a message from current user
                msg_box.append(put_markdown(f"`{m[0]}`: {m[1]}"))

        # remove expired


if __name__ == "__main__":
    start_server(main, debug=True, port=8080, cdn=True,remote_access=True)
