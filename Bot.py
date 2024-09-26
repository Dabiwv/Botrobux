import socket
import threading

# Введи IP-адрес первого устройства, где запущен сервер
server_ip = input("Введите IP-адрес сервера: ")
port = 12345

# Создание сокета
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, port))

# Получение сообщений от сервера
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "USERNAME":
                client.send(username.encode("utf-8"))
            else:
                print(message)
        except:
            print("Ошибка подключения.")
            client.close()
            break

# Отправка сообщений на сервер
def send_message():
    while True:
        message = f"{username}: {input('')}"
        client.send(message.encode("utf-8"))

# Ввод имени пользователя и запуск потоков
username = input("Введите ваше имя: ")

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_message)
send_thread.start()
