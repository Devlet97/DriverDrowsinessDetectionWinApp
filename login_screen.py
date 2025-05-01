from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import pyrebase

# --- Firebase Config ---
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

class LoginScreen(QWidget):
    def __init__(self, on_login_success_callback, go_back_callback):
        super().__init__()
        self.on_login_success_callback = on_login_success_callback
        self.go_back_callback = go_back_callback
        self.init_ui()

    def init_ui(self):
        # Ana layout (yatay)
        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Sol taraf (resim)
        left_widget = QFrame()
        left_widget.setStyleSheet("""
            QFrame {
                background-color: #f0f4f8;
            }
        """)
        # Sol widget'ın genişliğini ekranın yarısı olarak ayarla
        left_widget.setMinimumWidth(400)
        left_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        
        # Resim container'ı
        image_container = QLabel()
        image_container.setAlignment(Qt.AlignCenter)
        image_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        image_container.setStyleSheet("""
            QLabel {
                background-color: #f0f4f8;
            }
        """)
        
        # Resmi yükle
        self.pixmap = QPixmap("assets/foto4.png")
        self.update_image_size(image_container)
        
        left_layout.addWidget(image_container)
        
        # Sağ taraf (giriş formu)
        right_widget = QFrame()
        right_widget.setStyleSheet("""
            QFrame {
                background-color: white;
            }
        """)
        # Sağ widget'ın genişliğini ekranın yarısı olarak ayarla
        right_widget.setMinimumWidth(400)
        right_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(20)
        right_layout.setContentsMargins(40, 40, 40, 40)

        # Geri dönme butonu
        back_button = QPushButton("←")
        back_button.setObjectName("backButton")  # CSS için id
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.clicked.connect(self.go_back_callback)
        back_button.setFixedSize(40, 40)
        back_button.setToolTip("Geri Dön")
        
        # Başlık container
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)

        # Başlık
        title_label = QLabel("Hoş Geldiniz")
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 10px;
        """)
        title_layout.addWidget(title_label)

        subtitle_label = QLabel("Lütfen hesabınıza giriş yapın")
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
        right_layout.addLayout(header_layout)

        # Giriş formu
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # Email alanı
        email_layout = QVBoxLayout()
        email_label = QLabel("Email")
        email_label.setStyleSheet("""
            font-weight: bold;
            color: #333333;
            margin-bottom: 5px;
        """)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("ornek@email.com")
        self.email_input.setStyleSheet("""
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
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        form_layout.addLayout(email_layout)

        # Şifre alanı
        password_layout = QVBoxLayout()
        password_label = QLabel("Şifre")
        password_label.setStyleSheet("""
            font-weight: bold;
            color: #333333;
            margin-bottom: 5px;
        """)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("••••••••")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
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
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        form_layout.addLayout(password_layout)

        right_layout.addLayout(form_layout)

        # Giriş butonu
        self.login_button = QPushButton("Giriş Yap")
        self.login_button.setStyleSheet("""
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
        self.login_button.clicked.connect(self.login_user)
        right_layout.addWidget(self.login_button)

        # Hata mesajı
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #dc3545; font-size: 14px;")
        self.error_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.error_label)

        right_layout.addStretch()

        # Ana layout'a widget'ları ekle
        main_layout.addWidget(left_widget, 1)  # Stretch factor 1
        main_layout.addWidget(right_widget, 1)  # Stretch factor 1
        
        self.setLayout(main_layout)
        
    def resizeEvent(self, event):
        """Pencere boyutu değiştiğinde çağrılır"""
        super().resizeEvent(event)
        # Sol taraftaki resmi yeniden boyutlandır
        image_container = self.findChild(QLabel)
        if image_container:
            self.update_image_size(image_container)
    
    def update_image_size(self, container):
        """Resmi container boyutuna göre ölçeklendir"""
        if hasattr(self, 'pixmap'):
            scaled_pixmap = self.pixmap.scaled(
                container.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            container.setPixmap(scaled_pixmap)

    def login_user(self):
        try:
            email = self.email_input.text()
            password = self.password_input.text()
            
            if not email or not password:
                self.error_label.setText("Lütfen tüm alanları doldurun")
                return
                
            user = auth.sign_in_with_email_and_password(email, password)
            uid = user['localId']
            user_data = db.child("suruculer").child(uid).get().val()

            print("✅ Giriş başarılı!")
            print("🧾 Kullanıcı Bilgileri:", user_data)
            print("UID:", uid)

            self.on_login_success_callback(user_data)

        except Exception as e:
            print("❌ Giriş başarısız:", e)
            self.error_label.setText("Giriş başarısız. Lütfen bilgilerinizi kontrol edin.")
