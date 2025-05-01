# Sürücü Yorgunluk Tespit Sistemi

**Sürücü Yorgunluk Tespit Sistemi**, sürüş güvenliğini artırmak amacıyla geliştirilmiş, gerçek zamanlı çalışan bir masaüstü bilgisayarlı görü uygulamasıdır. Sistem, sürücünün göz hareketlerini ve yüz ifadelerini analiz ederek yorgunluk belirtilerini tespit eder, gerektiğinde sesli/görsel uyarılar verir ve detaylı raporlar sunar.

---

## Özellikler

- **Gerçek Zamanlı Yorgunluk Tespiti**: Göz kırpma sıklığı ve göz açıklık oranı analizine dayalı tespit
- **Otomatik Mola Hatırlatıcı**: Uzun süreli sürüşlerde düzenli mola önerileri
- **Detaylı Raporlama**: Sürüş oturumuna dair yorgunluk analiz geçmişi
- **E-posta Bildirimleri**: Otomatik olarak yorgunluk raporlarının gönderimi
- **Kullanıcı Yönetimi**: Güvenli kayıt ve giriş sistemi
- **Modern Arayüz**: PyQt5 ile geliştirilmiş responsive ve kullanıcı dostu tasarım

---

## Teknik Özellikler

- Python 3.8 veya üzeri ile geliştirilmiş windows masaüstü uygulaması
- PyQt5 ile modern kullanıcı arayüzü
- OpenCV + Mediapipe Face Mesh ile yüz ve göz analizi
- Firebase Realtime Database entegrasyonu
- SMTP üzerinden otomatik e-posta gönderimi
- Özelleştirilebilir yorgunluk tespit eşikleri

---

## Kullanılan Teknolojiler

- Python 3.8+
- PyQt5
- OpenCV
- Mediapipe
- Firebase Realtime Database
- SMTP (email servisi)

---

## Sistem Gereksinimleri

- Windows 10/11 işletim sistemi
- Minimum 4GB RAM
- Webcam
- Aktif internet bağlantısı
- Python 3.8 veya üzeri

---

## Kurulum

1. Python bağımlılıklarını yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

2. Firebase yapılandırmasını yapın:
   - `serviceAccountKey.json` dosyasını proje klasörüne yerleştirin
   - Gerekli ayarları `login_screen.py` dosyasında güncelleyin

3. SMTP e-posta bilgilerini ayarlayın:
   - `detection_email.py` içinde sunucu ve hesap bilgilerinizi güncelleyin

4. Uygulamayı başlatın:
   ```bash
   python main.py
   ```

---

## Kullanım

1. Uygulama açıldığında kayıt olun veya giriş yapın
2. Kamera erişimine izin verin
3. "Başlat" butonuna tıklayarak tespit sistemini çalıştırın
4. Sistem şu işlemleri otomatik yapar:
   - Göz kırpma takibi ve analiz
   - Yorgunluk durumunu tespit ve sesli uyarı
   - Mola hatırlatmaları
   - Rapor kaydı ve e-posta gönderimi

---

## Güvenlik Özellikleri

- Şifreli kullanıcı doğrulama
- Firebase ile güvenli veri aktarımı
- Oturum bazlı kullanıcı yönetimi
- Erişim korumalı rapor gönderimi

---

## Kullanım Alanları

- Profesyonel sürücüler ve filo sistemleri
- Lojistik ve taşımacılık firmaları
- Sürücü eğitim merkezleri
- Akademik sürüş güvenliği araştırmaları

---

## Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.

---

## İletişim

Her türlü soru ve öneri için:
- dovletyar2@gmail.com
- https://github.com/Devlet97
