import time
from scipy.spatial import distance
import winsound
from pygame import mixer

# Sistem parametreleri
EAR_THRESHOLD = 0.23  # Göz açıklık oranı eşiği
CLOSED_FRAMES_THRESHOLD = 60  # Kapalı göz tespit eşiği (frame sayısı)
OPEN_EYES_DURATION_THRESHOLD = 30  # Uzun süreli açık göz eşiği (saniye)
BREAK_REMINDER_INTERVAL = 4.5 * 3600  # Mola hatırlatma aralığı (4.5 saat)
MAX_SESSION_DURATION = 9 * 3600  # Maksimum sürüş süresi (9 saat)

# Yüz analiz noktaları
RIGHT_EYE = [33, 160, 158, 133, 153, 144]  # Sağ göz landmark noktaları
LEFT_EYE = [362, 385, 387, 263, 373, 380]  # Sol göz landmark noktaları

def calculate_ear(eye_landmarks):
    """
    Göz açıklık oranını (EAR - Eye Aspect Ratio) hesaplar.
    Bu oran, gözün dikey ve yatay açıklığı arasındaki ilişkiyi belirler.
    """
    A = distance.euclidean(eye_landmarks[1], eye_landmarks[5])
    B = distance.euclidean(eye_landmarks[2], eye_landmarks[4])
    C = distance.euclidean(eye_landmarks[0], eye_landmarks[3])
    ear = (A + B) / (2.0 * C)
    return ear

def format_time(seconds):
    """
    Verilen saniye değerini saat:dakika:saniye formatına dönüştürür.
    Özellikle sürüş ve mola sürelerinin gösterimi için kullanılır.
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def beep():
    """
    Sistem uyarı sesi çalar.
    Yorgunluk tespiti durumunda sürücüyü uyarmak için kullanılır.
    """
    duration = 300  # ms
    freq = 1500     # Hz
    winsound.Beep(freq, duration)

def init_sound_system():
    """
    Ses sistemini başlatır ve mola hatırlatma sesini yükler.
    Düzenli mola hatırlatmaları için kullanılır.
    """
    mixer.init()
    return "assets/mola.mp3" 