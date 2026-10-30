import requests  # İnternetten veri çekmek için gereken requests kütüphansini ekledik.

def get_steam_reviews(app_id):  # İncelemeleri çekecek ana fonksiyonu kodunu yazdık.
    url = f"https://store.steampowered.com/appreviews/{app_id}?json=1"  # Steam API adresini ve oyunun ID'sini (app_id) ayarladık.
    response = requests.get(url)  # Belirlediğimiz o adrese veri isteği gönderecek kodu yazdık.
    
    if response.status_code == 200:  # Siteye bağlantı başarılı oldu mu (200) diye baktık.
        print(f"Başarılı! Steam API'ye bağlanıldı. (App ID: {app_id})")  # Eğer başarılıysa ekrana bilgi mesajı yazdırdık.
        return response.json()  # Gelen veriyi okunabilir JSON formatında dışarı aktardık.
    else:  # Eğer siteye bağlanamazsak çalışacak kısmı yazdık.
        print("API bağlantı hatası!")  # Bağlanamazsak ekrana çıkacak hata mesajını yazdırdık.

get_steam_reviews(254700)  # Kodu Resident Evil 4'ün (2014 UHD) ID numarasıyla çalıştırıp test ettik.
