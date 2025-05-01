from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QFont, QPixmap, QPainter, QColor, 
                        QLinearGradient)

class ChooseScreen(QWidget):
    def __init__(self, go_to_login_callback, go_to_register_callback):
        super().__init__()
        self.go_to_login_callback = go_to_login_callback
        self.go_to_register_callback = go_to_register_callback
        
        # Arka plan resmi
        self.background = QPixmap("assets/foto3.png")
        self.background = self.background.scaled(800, 600, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        
        self.init_ui()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Arka plan resmini çiz
        target_rect = self.rect()
        source_rect = self.background.rect()
        
        # Resmi merkeze hizala ve doldur
        if target_rect.width() / target_rect.height() > source_rect.width() / source_rect.height():
            new_width = target_rect.width()
            new_height = int(new_width * source_rect.height() / source_rect.width())
            y_offset = (target_rect.height() - new_height) // 2
            painter.drawPixmap(0, y_offset, new_width, new_height, self.background)
        else:
            new_height = target_rect.height()
            new_width = int(new_height * source_rect.width() / source_rect.height())
            x_offset = (target_rect.width() - new_width) // 2
            painter.drawPixmap(x_offset, 0, new_width, new_height, self.background)
        
        # Gradient overlay - daha yumuşak geçiş
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 0, 0, 100))  # Üst kısım daha az opak
        gradient.setColorAt(0.5, QColor(0, 0, 0, 130))  # Orta kısım
        gradient.setColorAt(1, QColor(0, 0, 0, 160))  # Alt kısım daha opak
        painter.fillRect(self.rect(), gradient)

    def init_ui(self):
        # Minimum pencere boyutu
        self.setMinimumSize(800, 600)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # İçerik container'ı
        content_frame = QFrame()
        content_frame.setStyleSheet("QFrame { background-color: transparent; }")
        content_layout = QVBoxLayout(content_frame)
        
        # Dinamik kenar boşlukları
        self.update_content_margins(content_layout)

        # Başlık
        title_label = QLabel("Hoş Geldiniz")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: transparent;
                text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);
                letter-spacing: 2px;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        self.update_title_font(title_label)
        content_layout.addWidget(title_label)

        # Açıklama metni
        description_label = QLabel(
            "Sürüş sırasında sürücünün yorgunluk ve dikkat "
            "durumunu yapay zeka ile analiz eder. Göz kırpma sıklığı, "
            "baş pozisyonu ve yüz ifadesi gibi faktörleri takip ederek "
            "olası tehlikeleri önceden tespit eder ve sizi uyarır."
        )
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.95);
                background-color: transparent;
                text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.5);
                margin: 30px;
                padding: 15px;
                font-family: 'Segoe UI', sans-serif;
                letter-spacing: 0.5px;
                line-height: 1.6;
            }
        """)
        self.update_description_font(description_label)
        content_layout.addWidget(description_label)

        # Butonlar için container
        buttons_frame = QFrame()
        buttons_frame.setStyleSheet("background-color: transparent;")
        buttons_layout = QVBoxLayout(buttons_frame)
        buttons_layout.setSpacing(25)  # Butonlar arası mesafe artırıldı

        # Giriş butonu
        login_button = QPushButton("Giriş Yap")
        login_button.setCursor(Qt.PointingHandCursor)
        login_button.clicked.connect(self.go_to_login_callback)
        buttons_layout.addWidget(login_button, alignment=Qt.AlignCenter)

        # Kayıt butonu
        register_button = QPushButton("Kayıt Ol")
        register_button.setCursor(Qt.PointingHandCursor)
        register_button.clicked.connect(self.go_to_register_callback)
        buttons_layout.addWidget(register_button, alignment=Qt.AlignCenter)

        content_layout.addWidget(buttons_frame)
        main_layout.addWidget(content_frame)
        self.setLayout(main_layout)
        
        self.update_all_styles()

    def update_content_margins(self, layout):
        # Dinamik kenar boşlukları
        width_margin = int(self.width() * 0.12)  # %12 margin
        height_margin = int(self.height() * 0.12)
        layout.setContentsMargins(
            width_margin,
            height_margin,
            width_margin,
            height_margin
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        # Arka plan resmini güncelle
        self.background = QPixmap("assets/foto3.png")
        scaled_size = self.size() * self.devicePixelRatio()
        self.background = self.background.scaled(
            scaled_size,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        
        # Tüm stilleri güncelle
        self.update_all_styles()
        
        # İçerik kenar boşluklarını güncelle
        content_frame = self.findChild(QFrame)
        if content_frame and content_frame.layout():
            self.update_content_margins(content_frame.layout())

    def update_all_styles(self):
        # Başlık fontunu güncelle
        title_label = self.findChild(QLabel, "")
        if title_label and title_label.text() == "Hoş Geldiniz":
            self.update_title_font(title_label)
        
        # Açıklama fontunu güncelle
        for label in self.findChildren(QLabel):
            if label.text() != "Hoş Geldiniz":
                self.update_description_font(label)
        
        # Buton stillerini güncelle
        self.update_button_styles()

    def update_title_font(self, label):
        # Başlık boyutu pencere genişliğine göre ayarlanır
        base_size = min(int(self.width() / 20), 52)  # Maximum 52px
        font_size = max(32, base_size)  # Minimum 32px
        
        label.setStyleSheet(
            label.styleSheet() +
            f"""
            font-size: {font_size}px;
            font-weight: bold;
            margin-bottom: {font_size/2}px;
            """
        )

    def update_description_font(self, label):
        # Açıklama metni boyutu pencere genişliğine göre ayarlanır
        base_size = min(int(self.width() / 45), 28)  # Maximum 28px
        font_size = max(16, base_size)  # Minimum 16px
        
        label.setStyleSheet(
            label.styleSheet() +
            f"""
            font-size: {font_size}px;
            """
        )

    def update_button_styles(self):
        # Buton boyutları pencere boyutuna göre ayarlanır
        window_min_dim = min(self.width(), self.height())
        button_height = min(int(window_min_dim * 0.09), 65)  # Maximum 65px
        button_width = min(int(self.width() * 0.3), 350)    # Maximum 350px
        font_size = min(int(button_height * 0.4), 26)       # Maximum 26px
        
        # Giriş butonu stili
        login_style = f"""
            QPushButton {{
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: {int(button_height/2)}px;
                padding: {int(button_height/4)}px {int(button_width/8)}px;
                font-size: {font_size}px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
                min-width: {button_width}px;
                min-height: {button_height}px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            }}
            QPushButton:hover {{
                background-color: #1976D2;
                box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3);
                transform: translateY(-2px);
                transition: all 0.3s ease;
            }}
            QPushButton:pressed {{
                background-color: #1565C0;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }}
        """
        
        # Kayıt butonu stili
        register_style = f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                border: 2px solid #2196F3;
                border-radius: {int(button_height/2)}px;
                padding: {int(button_height/4)}px {int(button_width/8)}px;
                font-size: {font_size}px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
                min-width: {button_width}px;
                min-height: {button_height}px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            }}
            QPushButton:hover {{
                background-color: rgba(33, 150, 243, 0.1);
                border-color: #1976D2;
                box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3);
                transform: translateY(-2px);
                transition: all 0.3s ease;
            }}
            QPushButton:pressed {{
                background-color: rgba(33, 150, 243, 0.2);
                border-color: #1565C0;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }}
        """

        # Butonları güncelle
        for button in self.findChildren(QPushButton):
            if button.text() == "Giriş Yap":
                button.setStyleSheet(login_style)
            elif button.text() == "Kayıt Ol":
                button.setStyleSheet(register_style)
