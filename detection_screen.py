import cv2
import mediapipe as mp
import numpy as np
import winsound
import time
from scipy.spatial import distance
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from session_manager import logout
import datetime
import firebase_admin
from firebase_admin import credentials, db
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pygame import mixer
import os
from detection_screen_ui import DetectionScreenUI
from detection_utils import (
    EAR_THRESHOLD, CLOSED_FRAMES_THRESHOLD, OPEN_EYES_DURATION_THRESHOLD,
    BREAK_REMINDER_INTERVAL, MAX_SESSION_DURATION, RIGHT_EYE, LEFT_EYE,
    calculate_ear, format_time, beep, init_sound_system
)
from detection_firebase import FirebaseManager
from detection_email import EmailManager

class DetectionScreen(QWidget):
    def __init__(self, go_to_choose_callback):
        super().__init__()
        self.go_to_choose_callback = go_to_choose_callback
        self.ui = DetectionScreenUI()
        self.ui.init_ui(self)
        
        # Sistem yöneticilerini başlat
        self.firebase_manager = FirebaseManager()
        self.email_manager = EmailManager()
        
        # Temel değişkenler
        self.running = False
        self.session_completed = False
        self.is_currently_sleepy = False
        self.break_reminder_shown = False
        self.break_sound_play_count = 0
        self.break_sound = init_sound_system()

        # Zaman değişkenleri
        self.session_start_time = None
        self.last_break_reminder = None
        self.sleep_detection_count = 0
        self.session_logs = []

        # Yüz analiz sistemini başlat
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Kamera ayarı
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)

        # Timer ayarı
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Yorgunluk analiz değişkenleri
        self.closed_frames = 0
        self.prev_frame_time = 0
        self.open_eyes_start_time = None
        self.last_blink_time = None

    def show_break_reminder(self):
        self.ui.show_break_reminder(self)

    def close_break_reminder(self, msg_box):
        if msg_box.isVisible():
            msg_box.close()
            self.break_reminder_shown = False

    def show_success_message(self, message):
        self.ui.show_success_message(self, message)

    def show_error_message(self, message):
        self.ui.show_error_message(self, message)

    def start_detection(self):
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            self.cap.set(3, 1280)
            self.cap.set(4, 720)

        self.running = True
        self.session_completed = False
        self.button_start.setEnabled(False)
        self.button_exit.setEnabled(True)
        self.button_report.setEnabled(False)
        
        # Tüm sayaçları sıfırla ve başlat
        current_time = time.time()
        self.session_start_time = current_time
        self.last_break_reminder = current_time
        self.sleep_detection_count = 0
        self.session_logs = []
        self.break_reminder_shown = False
        self.break_sound_play_count = 0
        self.closed_frames = 0
        self.prev_frame_time = 0
        self.open_eyes_start_time = None
        self.last_blink_time = None
        self.is_currently_sleepy = False
        
        self.add_session_log("Oturum başlatıldı", current_time)
        self.timer.start(30)

    def exit_detection(self):
        self.running = False
        self.timer.stop()
        
        # Son log kaydını ekle
        if self.session_start_time is not None:
            final_duration = time.time() - self.session_start_time
            self.add_session_log(f"Oturum sonlandırıldı (Toplam süre: {format_time(final_duration)})", time.time())
        
        # Tüm sayaçları sıfırla
        self.session_start_time = None
        self.last_break_reminder = None
        self.sleep_detection_count = 0
        self.closed_frames = 0
        self.prev_frame_time = 0
        self.open_eyes_start_time = None
        self.last_blink_time = None
        self.is_currently_sleepy = False
        self.break_reminder_shown = False
        self.break_sound_play_count = 0
        
        if self.cap.isOpened():
            self.cap.release()
        self.label_video.setText("Kamera durduruldu. Başlatmak için butona tıklayın.")
        self.button_start.setEnabled(True)
        self.button_exit.setEnabled(False)
        self.session_completed = True
        self.button_report.setEnabled(True)
        print("🛑 Kamera durduruldu. Kullanıcı oturumu açık.")

    def logout_user(self):
        print("🚪 Oturum kapatılıyor...")
        self.running = False
        self.timer.stop()
        if self.cap.isOpened():
            self.cap.release()
        self.session_completed = False
        self.button_report.setEnabled(False)
        logout()
        self.go_to_choose_callback()

    def update_frame(self):
        if not self.running or self.session_start_time is None:
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        # Görüntü boyutlarını al
        img_h, img_w = frame.shape[:2]

        current_time = time.time()
        fps = 1 / (current_time - self.prev_frame_time) if self.prev_frame_time != 0 else 0
        self.prev_frame_time = current_time

        # Görüntüyü yatay olarak çevir
        frame = cv2.flip(frame, 1)

        # Zaman hesaplamaları
        session_duration = current_time - self.session_start_time
        next_break_time = self.last_break_reminder + BREAK_REMINDER_INTERVAL
        time_until_break = max(0, next_break_time - current_time)

        # Mola kontrolü
        if time_until_break <= 0 and not self.break_reminder_shown:
            self.break_reminder_shown = True
            self.show_break_reminder()
            self.play_break_sound()
            self.add_session_log("Mola hatırlatması gösterildi", current_time)

        # Yüz işleme
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)

        label = "YÜZ BULUNAMADI"
        color = (0, 0, 0)
        was_sleepy = self.is_currently_sleepy
        self.is_currently_sleepy = False

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmarks = face_landmarks.landmark

                right_eye = [(int(landmarks[i].x * img_w), int(landmarks[i].y * img_h)) for i in RIGHT_EYE]
                left_eye = [(int(landmarks[i].x * img_w), int(landmarks[i].y * img_h)) for i in LEFT_EYE]

                right_ear = calculate_ear(right_eye)
                left_ear = calculate_ear(left_eye)
                avg_ear = (right_ear + left_ear) / 2.0

                if avg_ear < EAR_THRESHOLD:
                    self.closed_frames += 1
                    self.last_blink_time = current_time
                    if self.open_eyes_start_time is not None:
                        self.open_eyes_start_time = None
                else:
                    self.closed_frames = 0
                    if self.open_eyes_start_time is None:
                        self.open_eyes_start_time = current_time

                # Uykululuk kontrolü
                if self.open_eyes_start_time is not None:
                    open_duration = current_time - self.open_eyes_start_time
                    if open_duration >= OPEN_EYES_DURATION_THRESHOLD:
                        label = "UYKULU (Gozler Uzun Sure Acik)"
                        color = (0, 0, 255)
                        self.is_currently_sleepy = True
                        beep()
                    elif self.closed_frames >= CLOSED_FRAMES_THRESHOLD:
                        label = "UYKULU"
                        color = (0, 0, 255)
                        self.is_currently_sleepy = True
                        beep()
                    else:
                        label = "UYANIK"
                        color = (0, 255, 0)
                else:
                    if self.closed_frames >= CLOSED_FRAMES_THRESHOLD:
                        label = "UYKULU"
                        color = (0, 0, 255)
                        self.is_currently_sleepy = True
                        beep()
                    else:
                        label = "UYANIK"
                        color = (0, 255, 0)

                # Uykululuk sayacını güncelle
                if self.is_currently_sleepy and not was_sleepy:
                    self.sleep_detection_count += 1
                    self.add_session_log("Uykulu durumu tespit edildi", current_time)

                # Göz noktalarını çiz
                for point in right_eye + left_eye:
                    cv2.circle(frame, point, 2, color, -1)

                # Bilgi paneli
                cv2.putText(frame, label, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
                cv2.putText(frame, f"EAR: {avg_ear:.2f}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)
                cv2.putText(frame, f"FPS: {fps:.1f}", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
                
                if self.open_eyes_start_time is not None:
                    open_duration = current_time - self.open_eyes_start_time
                    cv2.putText(frame, f"Acik Kalma: {open_duration:.1f}s", (10, 180), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

                # Yeni bilgi paneli
                cv2.putText(frame, f"Uykulu Yakalanma: {self.sleep_detection_count}", (img_w - 400, img_h - 140),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                cv2.putText(frame, f"Gecen Sure: {format_time(session_duration)}", (img_w - 400, img_h - 100),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                cv2.putText(frame, f"Mola icin Kalan: {format_time(time_until_break)}", (img_w - 400, img_h - 60),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                break

        # Görüntüyü Qt formatına çevir
        bytes_per_line = 3 * frame.shape[1]
        qt_image = QImage(frame.data, frame.shape[1], frame.shape[0], bytes_per_line, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(self.label_video.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label_video.setPixmap(scaled_pixmap)

    def play_break_sound(self):
        try:
            if self.break_sound_play_count < 3:
                mixer.music.load(self.break_sound)
                mixer.music.play()
                self.break_sound_play_count += 1
                QTimer.singleShot(3000, self.play_break_sound)
        except Exception as e:
            print(f"Ses çalma hatası: {str(e)}")

    def add_session_log(self, event_type, timestamp):
        log_entry = {
            "timestamp": datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            "event_type": event_type
        }
        self.session_logs.append(log_entry)

    def send_report(self):
        if not self.session_completed:
            print("Aktif bir oturum tamamlanmadan rapor gönderilemez.")
            return

        try:
            current_time = datetime.datetime.now()
            session_start = datetime.datetime.fromtimestamp(self.session_start_time) if self.session_start_time else current_time
            
            total_duration_seconds = (current_time.timestamp() - session_start.timestamp())
            formatted_duration = format_time(total_duration_seconds)
            
            report_data = {
                "session_start": session_start.strftime('%Y-%m-%d %H:%M:%S'),
                "session_end": current_time.strftime('%Y-%m-%d %H:%M:%S'),
                "sleep_detection_count": self.sleep_detection_count,
                "session_duration": formatted_duration,
                "logs": [log for log in self.session_logs]
            }
            
            # Firebase'e kaydet
            success, message = self.firebase_manager.save_report(report_data)
            if not success:
                self.show_error_message(message)
                return

            # Sürücü bilgilerini al
            driver_info = self.firebase_manager.get_driver_info(self.email_manager.email_settings['sender_email'])
            
            # E-posta içeriğini oluştur
            email_body = self.email_manager.create_email_content(driver_info, report_data, self.session_logs)
            
            # E-postayı gönder
            success, message = self.email_manager.send_email("Sürücü Uykululuk Raporu - Uyarı", email_body)
            if success:
                self.show_success_message("✅ Rapor başarıyla gönderildi!")
            else:
                self.show_error_message(message)

            # Yeni oturum için hazırlık
            self.session_start_time = None
            self.last_break_reminder = None
            self.sleep_detection_count = 0
            self.session_logs = []
            self.session_completed = False
            self.button_report.setEnabled(False)

        except Exception as e:
            self.show_error_message(f"❌ Rapor gönderilirken hata oluştu!\n{str(e)}")

    def closeEvent(self, event):
        self.running = False
        if self.cap.isOpened():
            self.cap.release()
        event.accept()
