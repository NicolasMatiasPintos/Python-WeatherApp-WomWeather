#Main File
#Using PyQt5 and requests/El programa usa PyQt5 y requests.
#Se me escapa mucho el spanglish ojo eh

import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, 
                            QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QIcon

class WomWeatherTitleBar(QWidget):
    def __init__(self, mainWindow):
        super().__init__(mainWindow)
        self.lbl_title = QLabel("WomWeather", self)
        self.btn_close = QPushButton(self)
        self.mainWindow = mainWindow
        self.IconTB = QLabel()
        self.Icon = QPixmap("cloud.svg")
        self.initUI()

    def initUI(self):
        self._startPos = None
        self.setFixedHeight(40)
        self.btn_close.setFixedSize(40, 30)
        self.btn_close.setIcon(QIcon("x.svg"))
        self.IconTB.setPixmap(self.Icon)

        HLayoutManager = QHBoxLayout()
        HLayoutManager.addWidget(self.IconTB)
        HLayoutManager.addWidget(self.lbl_title)
        HLayoutManager.addStretch()
        HLayoutManager.addWidget(self.btn_close)
        HLayoutManager.setContentsMargins(0, 0, 0, 0)

        self.setLayout(HLayoutManager)
        #Por si quisiera que el titlebar fuera diferente al mainwidget
        #self.setAttribute(Qt.WA_StyledBackground, True)

        self.setObjectName("TitleBar")
        self.btn_close.setObjectName("btn_close")
        self.lbl_title.setObjectName("lbl_title")
        self.setStyleSheet("""
            QWidget#TitleBar{
                background-color: #1034ad;
                border-bottom: 2px solid #0d2a8c;
            }
            QLabel#lbl_title{
                color: black;
                font-size: 15px;
                font-weight: 450;
                font-family: calibri;
                font-style: italic;
            }
            QPushButton#btn_close{
                color: white;
                background: transparent;
                border: none;
                font-size: 16px;
            }
            QPushButton#btn_close:hover {
                background-color: #ff5555;
            }
        """)

        self.btn_close.clicked.connect(self.mainWindow.close)

    #Definimos el evento de "mousePressEvent" para reflejar lo que pasa cuando mantenemos click en un title bar
    #Esto es un evento propio del PyQt5, el nombre tiene que ser si o si este. Esto va para los 3 eventos.
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._startPos = event.globalPos() - self.mainWindow.frameGeometry().topLeft()

    #Definimos el evento de "mouseMoveEvent" para simular el "drag" de la ventana.
    def mouseMoveEvent(self, event):
        if self._startPos and event.buttons() == Qt.LeftButton:
            self.mainWindow.move(event.globalPos() - self._startPos)

    #Definimos el evento de "mouseReleaseEvent" para simular el hecho de soltar el titlebar.
    def mouseReleaseEvent(self, event):
        self._startPos = None



class WomWeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.lbl_city = QLabel("Enter a city name: ", self)
        self.txt_city = QLineEdit(self)
        self.btn_Weather = QPushButton("Show Weather", self)
        self.lbl_temp = QLabel(self)
        self.lbl_emoji = QLabel(self)
        self.lbl_description = QLabel(self)
        self.bar_title = QWidget(self)
        self.titleBar = WomWeatherTitleBar(self)
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(400, 500)
        #Nota, QPixmap no aguanta formato "SVG" y hay que pasarlo a png.
        self.background_image("stacked-waves-haikei.png")

        VLayoutManager = QVBoxLayout()
        VLayoutManager.addWidget(self.titleBar)
        VLayoutManager.addWidget(self.lbl_city)
        VLayoutManager.addWidget(self.txt_city)
        VLayoutManager.addWidget(self.btn_Weather)
        VLayoutManager.addWidget(self.lbl_temp)
        VLayoutManager.addWidget(self.lbl_emoji)
        VLayoutManager.addWidget(self.lbl_description)

        self.setLayout(VLayoutManager)

        self.lbl_city.setAlignment(Qt.AlignCenter)
        self.txt_city.setAlignment(Qt.AlignCenter)
        self.lbl_temp.setAlignment(Qt.AlignCenter)
        self.lbl_emoji.setAlignment(Qt.AlignCenter)
        self.lbl_description.setAlignment(Qt.AlignCenter)

        self.lbl_city.setObjectName("lbl_city")
        self.txt_city.setObjectName("txt_city")
        self.lbl_temp.setObjectName("lbl_temp")
        self.lbl_emoji.setObjectName("lbl_emoji")
        self.lbl_description.setObjectName("lbl_description")
        self.btn_Weather.setObjectName("btn_Weather")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#lbl_city{
                font-size: 35px;
                font-weight: 600;
                font-style: italic;
                color: #1e202b;
            }
            QLineEdit#txt_city{
                font-size: 35px;
                padding: 12px 16px;
                border-radius: 12px;
                border: 1.5px solid #d0d0e1;
                background-color: #ffffff;
                color: #333;
            }
            QPushButton#btn_Weather{
                font-size: 35px;
                font-weight: bold;
                padding: 12px 20px;
                background-color: #7269ef;
                border-radius: 14px;
                color: #232130;
            }
            QPushButton#btn_Weather:hover{
                background-color: #5b54d6;
            }
            QLabel#lbl_temp{
                font-size: 65px;
                color: #3c3f4a;
            }
            QLabel#lbl_emoji{
                font-size: 90px;
                font-family: Segoe UI emoji;
            }
            QLabel#lbl_description{
                font-size: 50px;
                color: #3c3f4a;
            }
            """)
        
        self.btn_Weather.clicked.connect(self.get_weather)
    
    def get_weather(self):
        #You should get your own api key and use it down here, I won't post mine that's for sure. You have the URL down here:
        #URL: https://openweathermap.org/
        api_key = "Your Own API Key"
        city = self.txt_city.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
        
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized\nInvalid API Key")
                case 403:
                    self.display_error("Forbidden\nAcces denied")
                case 404:
                    self.display_error("Not found\nCity Not Found")
                case 500:
                    self.display_error("Internal Server Error\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway\nInvalid Response from the server")
                case 503:
                    self.display_error("Service Unavailable\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout\nNo response from the server")
                case _:
                    self.display_error(f"HTTP Error occured\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your Internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def display_error(self, message):
        self.lbl_temp.setStyleSheet("font-size: 30px")
        self.lbl_temp.setText(message)
        self.lbl_emoji.clear()
        self.lbl_description.clear()

    def display_weather(self, data):
        self.lbl_temp.setStyleSheet("font-size: 65px")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) - 459.67
        weather_id = data["weather"][0]["id"]
        weather_desc = data["weather"][0]["description"]

        self.lbl_temp.setText(f"{temperature_c:.0f}°C")
        self.lbl_emoji.setText(self.display_weather_emoji(weather_id))
        self.lbl_description.setText(weather_desc.title())
    
    @staticmethod
    def display_weather_emoji(weather_id):
        match weather_id:
            case _ if 200 <= weather_id <= 232:
                return "⛈️"
            case _ if 300 <= weather_id <= 321:
                return "🌦️"
            case _ if 500 <= weather_id <= 531:
                return "🌧️"
            case _ if 600 <= weather_id <= 622:
                return "🌨️"
            case _ if 701 <= weather_id <= 741:
                return "🌫️"
            case 762:
                return "🌋"
            case 771:
                return "🌬️"
            case 781: 
                return "💨"
            case 800:
                return "🌞"
            case _ if 801 <= weather_id <= 804:
                return "☁️"
            case _:
                return ""
    
    def background_image(self, image_path):
        palette = QPalette()
        pixmap = QPixmap(image_path)
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    WeatherApp = WomWeatherApp()
    WeatherApp.show()
    sys.exit(app.exec_())