import firebase_admin
from firebase_admin import credentials, db

class FirebaseManager:
    def __init__(self):
        self.db_ref = None
        self.init_firebase()

    def init_firebase(self):
        """Firebase bağlantısını başlatır"""
        try:
            if firebase_admin._apps:
                firebase_admin.delete_app(firebase_admin.get_app())
            
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://driverdrowsinessdetection-wap2-default-rtdb.europe-west1.firebasedatabase.app'
            })
            self.db_ref = db.reference('suruculer')
            print("Firebase bağlantısı başarılı")
        except Exception as e:
            print(f"Firebase bağlantısı başlatılamadı: {str(e)}")
            self.db_ref = None

    def save_report(self, report_data):
        """Raporu Firebase'e kaydeder"""
        if self.db_ref is None:
            return False, "Firebase bağlantısı mevcut değil"

        try:
            new_report_ref = self.db_ref.push(report_data)
            return True, "Firebase'e veri başarıyla kaydedildi"
        except Exception as e:
            return False, f"Firebase kayıt hatası: {str(e)}"

    def get_driver_info(self, email):
        """Sürücü bilgilerini Firebase'den alır"""
        if self.db_ref is None:
            return None

        try:
            all_drivers = self.db_ref.get()
            if all_drivers:
                for uid, driver_data in all_drivers.items():
                    if isinstance(driver_data, dict) and driver_data.get('email') == email:
                        return driver_data
            return None
        except Exception as e:
            print(f"Sürücü bilgileri alınamadı: {str(e)}")
            return None 