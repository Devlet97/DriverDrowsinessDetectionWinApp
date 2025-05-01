from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton, 
                            QHBoxLayout, QFrame, QSizePolicy, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap

class DetectionScreenUI:
    @staticmethod
    def init_ui(self):
        # Pencere boyutunu ayarla
        self.resize(1280, 800)
        self.setMinimumSize(800, 600)  # Minimum pencere boyutu
        
        # Arka plan rengini beyaz yap
        self.setStyleSheet("""
            QWidget {
                background-color: white;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Başlık ve geri butonu container'ı
        header_container = QWidget()
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 10)

        # Geri dönme butonu
        back_button = QPushButton("←")
        back_button.setObjectName("backButton")
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.clicked.connect(self.go_to_choose_callback)
        back_button.setFixedSize(40, 40)
        back_button.setToolTip("Geri Dön")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #007bff;
                border-radius: 20px;
                color: #007bff;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #007bff;
                color: white;
            }
            QPushButton:pressed {
                background-color: #0056b3;
                border-color: #0056b3;
                color: white;
            }
        """)
        header_layout.addWidget(back_button)

        # Başlık
        title_label = QLabel("Sürücü Yorgunluk Tespiti")  # Başlığı daha profesyonel hale getirdim
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            color: #007bff;
            margin-bottom: 10px;
            font-weight: bold;
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        main_layout.addWidget(header_container)

        # Video frame - Responsive
        video_frame = QFrame()
        video_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        video_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 10px;
                border: 2px solid #007bff;
                min-height: 400px;
            }
        """)
        video_layout = QVBoxLayout(video_frame)
        video_layout.setContentsMargins(5, 5, 5, 5)

        self.label_video = QLabel("Kamera bekleniyor...")  # Daha profesyonel bir mesaj
        self.label_video.setAlignment(Qt.AlignCenter)
        self.label_video.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_video.setStyleSheet("""
            font-size: 16px;
            color: #666666;
            background-color: #f0f4f8;
        """)
        video_layout.addWidget(self.label_video)
        main_layout.addWidget(video_frame, stretch=1)

        # Butonlar - Responsive
        buttons_container = QWidget()
        buttons_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(0, 10, 0, 0)

        button_style = """
            QPushButton {
                background-color: %s;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: %s;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """

        self.button_start = QPushButton("Başlat")
        self.button_start.setStyleSheet(button_style % ('#007bff', '#0056b3'))
        self.button_start.clicked.connect(self.start_detection)
        buttons_layout.addWidget(self.button_start)

        self.button_exit = QPushButton("Durdur")
        self.button_exit.setStyleSheet(button_style % ('#007bff', '#0056b3'))
        self.button_exit.clicked.connect(self.exit_detection)
        buttons_layout.addWidget(self.button_exit)

        self.button_report = QPushButton("Rapor Gönder")
        self.button_report.setStyleSheet(button_style % ('#007bff', '#0056b3'))
        self.button_report.clicked.connect(self.send_report)
        self.button_report.setEnabled(False)
        buttons_layout.addWidget(self.button_report)

        self.button_logout = QPushButton("Çıkış Yap")
        self.button_logout.setStyleSheet(button_style % ('#007bff', '#0056b3'))
        self.button_logout.clicked.connect(self.logout_user)
        buttons_layout.addWidget(self.button_logout)

        main_layout.addWidget(buttons_container)
        self.setLayout(main_layout)

    @staticmethod
    def show_break_reminder(self):
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #dc3545;
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
            }
            QMessageBox QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
                font-size: 12px;
            }
            QMessageBox QPushButton:hover {
                background-color: #c82333;
            }
        """)
        msg_box.setWindowTitle("Mola Hatırlatması")
        msg_box.setText("Lütfen mola verin!\nGözlerinizi dinlendirin")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setWindowFlags(msg_box.windowFlags() | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        msg_box.show()

        # 3 saniye sonra mesaj kutusunu kapat
        QTimer.singleShot(3000, lambda: self.close_break_reminder(msg_box))

    @staticmethod
    def close_break_reminder(self, msg_box):
        if msg_box.isVisible():
            msg_box.close()
            self.break_reminder_shown = False

    @staticmethod
    def show_success_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #28a745;
                font-size: 16px;
                padding: 10px;
            }
            QMessageBox QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
                font-size: 12px;
            }
            QMessageBox QPushButton:hover {
                background-color: #218838;
            }
        """)
        msg_box.setWindowTitle("Başarılı")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()

    @staticmethod
    def show_error_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #dc3545;
                font-size: 16px;
                padding: 10px;
            }
            QMessageBox QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
                font-size: 12px;
            }
            QMessageBox QPushButton:hover {
                background-color: #c82333;
            }
        """)
        msg_box.setWindowTitle("Hata")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.exec_() 