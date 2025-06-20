import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

def veritabani_olustur_ve_veri_ekle():
    """SQLite veritabanı oluşturur ve örnek COVID-19 verilerini ekler"""
    conn = sqlite3.connect('covid_verileri.db')
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS covid_vefatlar')
    cursor.execute('''
    CREATE TABLE covid_vefatlar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarih DATE,
        yeni_vefat INTEGER,
        toplam_vefat INTEGER
    )
    ''')
    
    ornek_veriler = [
        ('2020-01-01', 0, 0),
        ('2020-06-01', 5000, 10000),
        ('2020-12-31', 10000, 500000),
        ('2021-06-01', 8000, 1500000),
        ('2021-12-31', 12000, 3500000),
        ('2022-06-01', 5000, 4000000),
        ('2022-12-31', 3000, 4500000),
        ('2023-06-01', 1000, 4700000)
    ]
    
    cursor.executemany('INSERT INTO covid_vefatlar (tarih, yeni_vefat, toplam_vefat) VALUES (?, ?, ?)', ornek_veriler)
    conn.commit()
    conn.close()
    print("Veritabanı oluşturuldu ve örnek veriler eklendi: covid_verileri.db")

def yillik_vefat_grafigi_olustur():
    """Veritabanından yıllık vefat verilerini çekerek grafik oluşturur"""
    try:
        conn = sqlite3.connect('covid_verileri.db')
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT 
            strftime('%Y', tarih) as yil,
            MAX(toplam_vefat) - MIN(toplam_vefat) as yillik_vefat
        FROM covid_vefatlar
        GROUP BY yil
        ORDER BY yil
        ''')
        
        veriler = cursor.fetchall()
        yillar = [veri[0] for veri in veriler]
        vefatlar = [veri[1] for veri in veriler]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(yillar, vefatlar, color='#e63946')
        
        plt.title('Yıllara Göre COVID-19 Vefat Sayıları', fontsize=14)
        plt.xlabel('Yıl')
        plt.ylabel('Vefat Sayısı')
        plt.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f"{int(height/1000)}K" if height < 1000000 else f"{int(height/1000000)}M",
                    ha='center', va='bottom')
        
        plt.savefig('covid_yillik_vefat.png', bbox_inches='tight', dpi=300)
        plt.close()
        print("Grafik oluşturuldu: covid_yillik_vefat.png")
        
    except sqlite3.Error as e:
        print(f"Veritabanı hatası: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    veritabani_olustur_ve_veri_ekle()
    
    yillik_vefat_grafigi_olustur()