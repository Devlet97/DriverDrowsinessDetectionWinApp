import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailManager:
    def __init__(self):
        self.email_settings = {
            'sender_email': 'dovletyar4@gmail.com',
            'sender_password': 'boqd xgsf uqji mtlz',
            'receiver_email': 'dovletyar2@gmail.com',
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587
        }

    def create_email_content(self, driver_info, report_data, session_logs):
        """E-posta içeriğini oluşturur"""
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #007BFF;">SÜRÜŞ RAPORU</h2>
            <h3 style="color: #495057;">SÜRÜCÜ BİLGİLERİ:</h3>
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;">
        """

        if driver_info:
            body += f"""
                <p><strong>İsim:</strong> {driver_info.get('isim', 'Bilgi yok')} {driver_info.get('soyisim', '')}</p>
                <p><strong>TC Kimlik No:</strong> {driver_info.get('tc_kimlik', 'Bilgi yok')}</p>
                <p><strong>Ehliyet No:</strong> {driver_info.get('ehliyet_no', 'Bilgi yok')}</p>
                <p><strong>Araç Plaka:</strong> {driver_info.get('arac_plaka', 'Bilgi yok')}</p>
                <p><strong>Email:</strong> {driver_info.get('email', 'Bilgi yok')}</p>
            """
        else:
            body += "<p style='color: #dc3545;'><strong>Uyarı:</strong> Sürücü bilgilerine erişilemedi. Lütfen sistem yöneticisi ile iletişime geçin.</p>"

        body += f"""
            </div>
            
            <h3 style="color: #495057;">SÜRÜŞ BİLGİLERİ:</h3>
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <p><strong>Başlangıç Zamanı:</strong> {report_data['session_start']}</p>
                <p><strong>Bitiş Zamanı:</strong> {report_data['session_end']}</p>
                <p><strong>Toplam Süre:</strong> {report_data['session_duration']}</p>
                <p style="color: {'#dc3545' if report_data['sleep_detection_count'] > 0 else '#28a745'}">
                    <strong>Uykulu Yakalanma Sayısı:</strong> {report_data['sleep_detection_count']}
                </p>
            </div>

            <h3 style="color: #6c757d;">OLAY KAYITLARI:</h3>
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
        """

        for log in session_logs:
            event_color = '#dc3545' if 'Uykulu' in log['event_type'] else '#28a745'
            body += f"""
                <p style="color: {event_color}">
                    <strong>{log['timestamp']}</strong> - {log['event_type']}
                </p>
            """

        body += """
            </div>
            <p style="color: #6c757d; font-size: 12px; margin-top: 20px;">
                Bu rapor Sürücü Uykululuk Algılama Sistemi tarafından otomatik olarak oluşturulmuştur.
            </p>
        </body>
        </html>
        """
        return body

    def send_email(self, subject, body):
        """E-postayı gönderir"""
        try:
            msg = MIMEMultipart()
            msg['From'] = f"Sürücü Uykululuk Algılama Sistemi <{self.email_settings['sender_email']}>"
            msg['To'] = self.email_settings['receiver_email']
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html', 'utf-8'))

            server = smtplib.SMTP(self.email_settings['smtp_server'], self.email_settings['smtp_port'])
            server.starttls()
            server.login(self.email_settings['sender_email'], self.email_settings['sender_password'])
            server.send_message(msg)
            server.quit()
            return True, "E-posta başarıyla gönderildi"
        except smtplib.SMTPAuthenticationError:
            return False, "Gmail kimlik doğrulama hatası! Lütfen Gmail Uygulama Şifresini kontrol edin."
        except Exception as e:
            return False, f"E-posta gönderme hatası: {str(e)}" 