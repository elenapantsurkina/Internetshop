from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# Настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """ Специальный класс, который отвечает за обработку входящих запросов от клиентов """

    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """

        if self.path == "/":
            self.path = "/contacts.html"  # Перенаправление на страницу контактов

        if self.path.endswith(".html"):
            content_type = "text/html"
        elif self.path.endswith(".css"):
            content_type = "text/css"
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("<h1>404 - File Not Found</h1>", "utf-8"))
            return

        try:
            with open(self.path[1:], "r", encoding="utf-8") as file:  # Удаляем начальный '/'
                self.send_response(200)  # Отправка кода ответа
                self.send_header("Content-type", content_type)  # Отправка типа данных
                self.end_headers()  # Завершение формирования заголовков ответа
                self.wfile.write(bytes(file.read(), "utf-8"))  # Тело ответа с содержимым файла
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("<h1>404 - File Not Found</h1>", "utf-8"))  # Если файл не найден


if __name__ == "__main__":
    # Инициализация веб-сервера
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Старт веб-сервера в бесконечном цикле
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    # Остановка веб-сервера
    webServer.server_close()
    print("Server stopped.")
