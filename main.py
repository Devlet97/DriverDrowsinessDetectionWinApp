import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget, QSizePolicy
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QRect, Qt
from PyQt5.QtGui import QFont
from guide_screen import GuideScreen
from choose_screen import ChooseScreen
from auth_screen import AuthScreen
from login_screen import LoginScreen
from detection_screen import DetectionScreen
from session_manager import is_logged_in, set_logged_in, logout

class DriverDrowsinessApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sürücü Yorgunluk Tespit Sistemi")
        
        # Pencere bayrakları - maximize/minimize butonlarını aktif et
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)
        
        # Minimum pencere boyutu
        self.setMinimumSize(800, 600)
        
        # Pencereyi yeniden boyutlandırılabilir yap
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Global stil ayarları
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: 'Poppins', 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 10px;
                padding: 10px;
                min-width: 120px;
                min-height: 40px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004494;
            }
            QPushButton#backButton {
                background-color: transparent;
                color: #007BFF;
                border: 2px solid #007BFF;
                border-radius: 5px;
                min-width: 40px;
                min-height: 40px;
                padding: 5px;
                font-size: 20px;
            }
            QPushButton#backButton:hover {
                background-color: #f0f4f8;
                border-color: #0056b3;
                color: #0056b3;
            }
            QPushButton#backButton:pressed {
                background-color: #e8ecf1;
                border-color: #004494;
                color: #004494;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #007BFF;
                border-radius: 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #0056b3;
            }
            QLabel {
                font-size: 16px;
                color: #333333;
            }
            QScrollArea {
                border: none;
            }
        """)

        # Ekranları oluştur
        self.guide_screen = GuideScreen(self.go_to_choose_screen)
        self.choose_screen = ChooseScreen(self.go_to_login_screen, self.go_to_auth_screen)
        self.auth_screen = AuthScreen(self.on_auth_success, self.go_to_choose_screen)
        self.login_screen = LoginScreen(self.on_login_success, self.go_to_choose_screen)
        self.detection_screen = DetectionScreen(self.go_to_choose_screen)

        # Stack'e ekle
        self.addWidget(self.guide_screen)
        self.addWidget(self.choose_screen)
        self.addWidget(self.auth_screen)
        self.addWidget(self.login_screen)
        self.addWidget(self.detection_screen)

        # Açılışta oturum kontrolü
        if is_logged_in():
            print("Oturum açık bulundu. Tespit ekranına geçiliyor.")
            self.setCurrentWidget(self.detection_screen)
        else:
            print("Uygulama başlatılıyor.")
            self.setCurrentWidget(self.guide_screen)

    def resizeEvent(self, event):
        """Pencere boyutu değiştiğinde tüm widget'ları yeniden boyutlandır"""
        super().resizeEvent(event)
        current_widget = self.currentWidget()
        if current_widget:
            current_widget.setGeometry(0, 0, self.width(), self.height())

    def go_to_choose_screen(self):
        self.setCurrentWidget(self.choose_screen)

    def go_to_login_screen(self):
        self.setCurrentWidget(self.login_screen)

    def go_to_auth_screen(self):
        self.setCurrentWidget(self.auth_screen)

    def on_auth_success(self):
        print("Kayıt başarılı. Tespit ekranına geçiliyor.")
        set_logged_in(True)
        self.setCurrentWidget(self.detection_screen)

    def on_login_success(self, user_data):
        print("Giriş başarılı. Tespit ekranına geçiliyor.")
        print("Kullanıcı:", user_data)
        set_logged_in(True)
        self.setCurrentWidget(self.detection_screen)

    def animate_transition(self, target_widget):
        # Geçerli widget'ı sakla
        current_widget = self.currentWidget()
        
        # Hedef widget'ı göster ve pozisyonunu ayarla
        self.setCurrentWidget(target_widget)
        target_widget.setGeometry(self.width(), 0, self.width(), self.height())
        
        # Animasyonları oluştur
        # Mevcut ekranı sola kaydır
        current_anim = QPropertyAnimation(current_widget, b"geometry")
        current_anim.setDuration(300)
        current_anim.setStartValue(QRect(0, 0, self.width(), self.height()))
        current_anim.setEndValue(QRect(-self.width(), 0, self.width(), self.height()))
        current_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        # Yeni ekranı sağdan getir
        target_anim = QPropertyAnimation(target_widget, b"geometry")
        target_anim.setDuration(300)
        target_anim.setStartValue(QRect(self.width(), 0, self.width(), self.height()))
        target_anim.setEndValue(QRect(0, 0, self.width(), self.height()))
        target_anim.setEasingCurve(QEasingCurve.OutCubic)
        
        # Animasyonları başlat
        current_anim.start()
        target_anim.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DriverDrowsinessApp()
    window.resize(800, 600)  # Başlangıç boyutu
    window.show()
    sys.exit(app.exec_())
