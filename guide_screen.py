from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, 
                           QFrame, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QFont, QPixmap, QPainter, QColor, QFontDatabase, 
                        QLinearGradient, QPalette, QBrush)

class GuideScreen(QWidget):
    def __init__(self, next_callback):
        super().__init__()
        self.next_callback = next_callback
        self.init_ui()
        
        # Arka plan resmi
        self.background = QPixmap("assets/foto2.png")
        self.background = self.background.scaled(800, 600, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Arka plan resmini çiz
        target_rect = self.rect()
        source_rect = self.background.rect()
        
        # Resmi merkeze hizala
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
        
        # Gradient overlay - daha hafif bir karartma
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 0, 0, 100))  # Üst kısım daha az opak
        gradient.setColorAt(1, QColor(0, 0, 0, 140))  # Alt kısım biraz daha opak
        painter.fillRect(self.rect(), gradient)

    def init_ui(self):
        # Ana layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # İçerik container'ı
        content_frame = QFrame()
        content_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 25%);
                border-radius: 20px;
                padding: 20px;
            }
        """)
        frame_layout = QVBoxLayout(content_frame)
        frame_layout.setSpacing(30)
        frame_layout.setContentsMargins(40, 40, 40, 40)

        # Logo container
        logo_container = QWidget()
        logo_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        logo_container.setStyleSheet("background-color: transparent;")
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 30)  # Increased bottom margin

        # Logo
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap("assets/logo.png")
        self.update_logo_size()  # Initial logo size update
        self.logo_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(self.logo_label)

        frame_layout.addWidget(logo_container)

        # Başlık
        title_label = QLabel("Sürüş sırasında güvenliğinizi\nön planda tutuyoruz.")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        title_label.setStyleSheet("""
            font-size: 40px;
            font-weight: bold;
            color: white;
            margin-bottom: 20px;
            background-color: transparent;
            letter-spacing: 1px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            padding: 10px;
            line-height: 1.4;
        """)
        title_label.setWordWrap(True)
        frame_layout.addWidget(title_label)

        # Açıklama
        description_text = (
            "Bu uygulama kameranızdan aldığı görüntülerle yorgunluk belirtilerini algılar, "
            "uyarılar vererek sizi ve sevdiklerinizi olası kazalardan korur.\n\n"
            "Trafik güvenliği için bir adım daha atın.\n\n"
            "Yolculuğunuz boyunca gözünüz açık, zihniniz dinç kalsın!"
        )
        
        description_label = QLabel(description_text)
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        description_label.setStyleSheet("""
            font-size: 25px;
            color: rgba(255, 255, 255, 0.95);
            line-height: 1.8;
            margin: 20px 0;
            background-color: transparent;
            letter-spacing: 0.5px;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
            padding: 10px;
        """)
        description_label.setWordWrap(True)
        frame_layout.addWidget(description_label)

        # Devam butonu
        button = QPushButton("Devam Et")
        button.setCursor(Qt.PointingHandCursor)
        button.setFixedWidth(250)
        button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 25px;
                padding: 15px 40px;
                font-size: 20px;
                font-weight: bold;
                margin-top: 20px;
                border: 2px solid transparent;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            }
            QPushButton:hover {
                background-color: #0056b3;
                border: 2px solid #ffffff;
                box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3);
            }
            QPushButton:pressed {
                background-color: #004494;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }
        """)
        button.clicked.connect(self.next_callback)
        frame_layout.addWidget(button, alignment=Qt.AlignCenter)

        # Layout'ları birleştir
        main_layout.addWidget(content_frame)

    def resizeEvent(self, event):
        """Pencere boyutu değiştiğinde arka plan resmini ve logoyu yeniden boyutlandır"""
        super().resizeEvent(event)
        
        # Arka plan resmini güncelle
        self.background = QPixmap("assets/foto2.png")
        scaled_size = self.size() * self.devicePixelRatio()
        self.background = self.background.scaled(
            scaled_size,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        
        # Logoyu güncelle
        self.update_logo_size()

    def update_logo_size(self):
        """Logoyu pencere boyutuna göre ölçeklendir"""
        if hasattr(self, 'logo_label') and hasattr(self, 'logo_pixmap'):
            # Pencere genişliğinin %20'si kadar logo boyutu
            target_size = min(self.width() * 0.2, 200)  # Maximum 200px
            target_size = max(target_size, 120)  # Minimum 120px
            
            scaled_logo = self.logo_pixmap.scaled(
                int(target_size),
                int(target_size),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.logo_label.setPixmap(scaled_logo)
