from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                                 QFileDialog, QHBoxLayout, QScrollArea, QFrame, QSizePolicy)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import base64
import pyrebase
import io
from PIL import Image

# --- Firebase ayarları
firebaseConfig = {
    "apiKey": "AIzaSyBU-Vzi6i7h9TGLJR4l9zF1H19O38qlAhU",
    "authDomain": "driverdrowsinessdetection-wap2.firebaseapp.com",
    "databaseURL": "https://driverdrowsinessdetection-wap2-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "driverdrowsinessdetection-wap2",
    "storageBucket": "driverdrowsinessdetection-wap2.appspot.com",
    "messagingSenderId": "672264542778",
    "appId": "1:672264542778:web:cf379d09ff4b1fec403303"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

class AuthScreen(QWidget):
    def __init__(self, on_auth_success_callback, go_back_callback):
        super().__init__()
        self.on_auth_success_callback = on_auth_success_callback
        self.go_back_callback = go_back_callback
        self.photo_data = None
        self.init_ui()

    def init_ui(self):
        # Ana layout (yatay)
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Sol taraf (kayıt formu)
        left_widget = QFrame()
        left_widget.setStyleSheet("""
            QFrame {
                background-color: white;
            }
        """)
        left_widget.setMinimumWidth(400)
        left_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(20)
        left_layout.setContentsMargins(40, 40, 40, 40)

        # Başlık Container
        title_container = QWidget()
        title_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        title_layout = QVBoxLayout(title_container)
        title_layout.setSpacing(5)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # Geri dönme butonu
        back_button = QPushButton("←")
        back_button.setObjectName("backButton")  # CSS için id
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.clicked.connect(self.go_back_callback)
        back_button.setFixedSize(40, 40)
        back_button.setToolTip("Geri Dön")

        # Başlık
        title_label = QLabel("Kayıt Ol")
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 10px;
        """)
        title_layout.addWidget(title_label)

        subtitle_label = QLabel("Lütfen bilgilerinizi girin")
        subtitle_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        subtitle_label.setStyleSheet("""
            font-size: 16px;
            color: #666666;
            margin-bottom: 30px;
        """)
        title_layout.addWidget(subtitle_label)

        # Geri butonu ve başlık container'ını yatay layout'a ekle
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 20)  # Alt boşluk ekle
        header_layout.addWidget(back_button)
        header_layout.addWidget(title_container)
        header_layout.addStretch()  # Sağa doğru boşluk ekle
        left_layout.addLayout(header_layout)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f4f8;
                width: 8px;
                margin: 0px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 123, 255, 0.5);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        # Form container
        form_widget = QWidget()
        form_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(0, 0, 20, 0)

        # Form alanları
        fields = [
            ("TC Kimlik No", "12345678901"),
            ("İsim", "Adınız"),
            ("Soyisim", "Soyadınız"),
            ("Sürücü Belgesi No", "123456789"),
            ("Araç Plaka", "34ABC123"),
            ("Email", "ornek@email.com"),
            ("Parola", "••••••••")
        ]

        self.inputs = {}
        for field, placeholder in fields:
            field_container = QWidget()
            field_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            field_layout = QVBoxLayout(field_container)
            field_layout.setSpacing(5)
            field_layout.setContentsMargins(0, 0, 0, 0)
            
            label = QLabel(field)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            label.setStyleSheet("""
                font-weight: bold;
                color: #333333;
                margin-bottom: 5px;
            """)
            
            inp = QLineEdit()
            inp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            inp.setFixedHeight(45)  # Sabit yükseklik
            inp.setPlaceholderText(placeholder)
            if field == "Parola":
                inp.setEchoMode(QLineEdit.Password)
            inp.setStyleSheet("""
                QLineEdit {
                    padding: 12px;
                    border: 1px solid #cccccc;
                    border-radius: 5px;
                    background-color: #ffffff;
                    font-size: 14px;
                }
                QLineEdit:focus {
                    border: 1px solid #007BFF;
                }
            """)
            
            field_layout.addWidget(label)
            field_layout.addWidget(inp)
            form_layout.addWidget(field_container)
            self.inputs[field] = inp

        # Fotoğraf seçimi container
        photo_container = QWidget()
        photo_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        photo_layout = QHBoxLayout(photo_container)
        photo_layout.setSpacing(10)
        photo_layout.setContentsMargins(0, 0, 0, 0)
        
        self.photo_label = QLabel("Henüz fotoğraf seçilmedi")
        self.photo_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.photo_label.setFixedHeight(45)  # Input'larla aynı yükseklik
        self.photo_label.setStyleSheet("""
            padding: 12px;
            background-color: white;
            border: 1px solid #cccccc;
            border-radius: 5px;
            min-width: 200px;
            color: #666666;
        """)
        
        self.photo_button = QPushButton("Fotoğraf Seç")
        self.photo_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.photo_button.setFixedSize(120, 45)  # Sabit boyut
        self.photo_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
                padding: 12px;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.photo_button.clicked.connect(self.select_photo)
        
        photo_layout.addWidget(self.photo_label)
        photo_layout.addWidget(self.photo_button)
        form_layout.addWidget(photo_container)

        # Kayıt butonu container
        button_container = QWidget()
        button_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_layout = QVBoxLayout(button_container)
        button_layout.setContentsMargins(0, 20, 0, 0)
        
        self.register_button = QPushButton("Kaydol ve Başlat")
        self.register_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.register_button.setFixedHeight(50)  # Daha büyük buton
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004494;
            }
        """)
        self.register_button.clicked.connect(self.register_user)
        button_layout.addWidget(self.register_button)

        # Hata mesajı
        self.error_label = QLabel("")
        self.error_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.error_label.setStyleSheet("color: #dc3545; font-size: 14px;")
        self.error_label.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(self.error_label)
        
        form_layout.addWidget(button_container)
        form_layout.addStretch()  # Alt boşluk için

        scroll.setWidget(form_widget)
        left_layout.addWidget(scroll)

        # Sağ taraf (resim)
        right_widget = QFrame()
        right_widget.setStyleSheet("""
            QFrame {
                background-color: #f0f4f8;
            }
        """)
        right_widget.setMinimumWidth(400)
        right_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Resim container
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setStyleSheet("background-color: #f0f4f8;")
        
        # Resmi yükle
        self.original_pixmap = QPixmap("assets/foto5.png")
        right_layout.addWidget(self.image_label)

        # Ana layout'a widget'ları ekle
        main_layout.addWidget(left_widget, 1)  # Stretch factor 1
        main_layout.addWidget(right_widget, 1)  # Stretch factor 1
        
        self.setLayout(main_layout)
        
        # İlk resim ölçeklendirmesi
        self.resizeImage()

    def resizeEvent(self, event):
        """Pencere boyutu değiştiğinde çağrılır"""
        super().resizeEvent(event)
        self.resizeImage()
        
    def resizeImage(self):
        """Resmi container boyutuna göre ölçeklendir"""
        if hasattr(self, 'image_label') and hasattr(self, 'original_pixmap'):
            # Resmi label boyutuna göre ölçeklendir
            scaled_pixmap = self.original_pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

    def select_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Fotoğraf Seç", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.photo_label.setText(file_path.split("/")[-1])
            with open(file_path, "rb") as f:
                img_bytes = f.read()
                self.photo_data = base64.b64encode(img_bytes).decode('utf-8')

    def register_user(self):
        try:
            # Boş alan kontrolü
            for field, inp in self.inputs.items():
                if not inp.text():
                    self.error_label.setText(f"Lütfen {field} alanını doldurun")
                    return

            email = self.inputs["Email"].text()
            password = self.inputs["Parola"].text()
            
            if len(password) < 6:
                self.error_label.setText("Şifre en az 6 karakter olmalıdır")
                return

            user = auth.create_user_with_email_and_password(email, password)
            uid = user['localId']

            user_data = {
                "tc_kimlik": self.inputs["TC Kimlik No"].text(),
                "isim": self.inputs["İsim"].text(),
                "soyisim": self.inputs["Soyisim"].text(),
                "ehliyet_no": self.inputs["Sürücü Belgesi No"].text(),
                "arac_plaka": self.inputs["Araç Plaka"].text(),
                "email": email,
                "foto": self.photo_data if self.photo_data else ""
            }

            db.child("suruculer").child(uid).set(user_data)
            self.on_auth_success_callback()

        except Exception as e:
            print("HATA:", e)
            self.error_label.setText("Kayıt işlemi başarısız. Lütfen bilgilerinizi kontrol edin.")
