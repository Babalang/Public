import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from pync import *
#Application pour mettre en veille après un certain temps.
class Index(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TIMER")
        self.setGeometry(600, 400, 300, 350)
        label = QLabel("TIMER", self)
        label.setGeometry(50,10,100,30)
        self.hour_field = QSpinBox(self)
        self.hour_field.setGeometry(50, 50, 90, 20)
        self.hour_field.setRange(0, 23)
        self.hour_field.setSuffix(" heures")
        self.hour_field.setValue(0)

        self.minute_field = QSpinBox(self)
        self.minute_field.setGeometry(50, 100, 90, 20)
        self.minute_field.setRange(0, 59)
        self.minute_field.setSuffix(" minutes")
        self.minute_field.setValue(0)

        self.second_field = QSpinBox(self)
        self.second_field.setGeometry(50, 150, 90, 20)
        self.second_field.setRange(0, 59)
        self.second_field.setSuffix(" secondes")
        self.second_field.setValue(0)

        button = QPushButton("Annuler", self)
        button.setGeometry(50, 280, 200, 50)
        button.clicked.connect(self.Annuler)

        button = QPushButton("Valider", self)
        button.setGeometry(50, 220, 200, 50)
        button.clicked.connect(self.start_countdown)

        self.countdown_label = QLabel(self)
        self.countdown_label.setGeometry(50, 180, 200, 30)
        font = self.countdown_label.font()
        font.setPointSize(16)
        self.countdown_label.setFont(font)
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setText("Temps restant : 00:00:00")
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.remaining_time = 0

    def start_countdown(self):
        Notifier.notify('Timer lancé', title='TIMER')
        hours = self.hour_field.value()
        minutes = self.minute_field.value()
        seconds = self.second_field.value()

        self.remaining_time = hours * 3600 + minutes * 60 + seconds
        self.update_countdown()

        self.countdown_timer.start(1000)

    def update_countdown(self):
        hours = self.remaining_time // 3600
        minutes = (self.remaining_time % 3600) // 60
        seconds = self.remaining_time % 60

        self.countdown_label.setText(f"Temps restant : {hours:02d}:{minutes:02d}:{seconds:02d}")

        if self.remaining_time > 0:
            self.remaining_time -= 1
            if self.remaining_time<=10:
                Notifier.notify(self.remaining_time, title='TIMER')
        else:
            self.stop_countdown()
            self.close()

    def stop_countdown(self):
        self.countdown_label.setText("Temps écoulé !")
        os.system("pmset sleepnow")

    def Annuler(self):
        Notifier.notify("Timer arrêté", title='TIMER')
        self.countdown_label.setText("Temps restant : 00:00:00")
        self.countdown_timer.stop()
        self.remaining_time = 0


app = QApplication([])
css_file = QFile(f"{os.getcwd()}/static/style.css")
css_file.open(QFile.ReadOnly)
app.setStyleSheet(css_file.readAll().data().decode("utf-8"))
css_file.close()
# Définissez l'icône de l'application
app.setWindowIcon(QIcon(f"{os.getcwd()}/static/timer.png"))
window = Index()
window.show()
app.exec()
