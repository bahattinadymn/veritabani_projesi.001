import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cok-gizli-super-guvenli-anahtar'
    

    
    DRIVER = 'ODBC Driver 17 for SQL Server'
    
    
    # Eğer localhost çalışmazsa burayı güncellememiz gerekebilir.
    SERVER = 'localhost'      
    
    DATABASE = 'KutuphaneDB' 
    
    # Şifre derdinden kurtulmak için bunu TRUE yapıyoruz
    USE_WINDOWS_AUTH = True 
    
    # Windows Auth True olduğu için aşağıdaki sa/şifre kısımları artık önemsiz
    UID = 'sa'        
    PWD = '47293' 

    
    if USE_WINDOWS_AUTH:
        # Trusted_Connection=yes diyerek Windows kimliğinle bağlanıyoruz
        connection_string = f'DRIVER={{{DRIVER}}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'
    else:
        connection_string = f'DRIVER={{{DRIVER}}};SERVER={SERVER};DATABASE={DATABASE};UID={UID};PWD={PWD};'
    
    params = urllib.parse.quote_plus(connection_string)
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_KULLANICI')
    MAIL_PASSWORD = os.getenv('MAIL_SIFRE')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_KULLANICI')