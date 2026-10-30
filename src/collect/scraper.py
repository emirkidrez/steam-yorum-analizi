import requests  # İnternetten veri çekmek için gereken requests kütüphanesini ekledik.
import json  # Parametreleri JSON formatına çevirmek için json kütüphanesini ekledik.
import time  # Steam'i yormamak için istekler arasında beklemek üzere time kütüphanesini ekledik.

def get_steam_reviews(app_id, max_reviews=200):  # İncelemeleri çekecek ana fonksiyonun kodunu yazdık.
    url = "https://api.steampowered.com/IUserReviewsService/GetAppReviews/v1/"  # Eski endpoint kapandığı için Steam'in yeni resmi API adresini ayarladık.
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}  # İsteğin tarayıcıdan geliyormuş gibi görünmesi için kimlik bilgisini ekledik.
    tum_incelemeler = []  # Çektiğimiz tüm incelemeleri biriktireceğimiz boş listeyi oluşturduk.
    cursor = "*"  # İlk sayfa için başlangıç imlecini "*" olarak ayarladık.

    while len(tum_incelemeler) < max_reviews:  # İstediğimiz inceleme sayısına ulaşana kadar sayfa sayfa çekmeye devam ettik.
        girdi = {  # Yeni API parametreleri input_json içinde gönderildiği için bir sözlük hazırladık.
            "appid": app_id,  # Hangi oyunun incelemelerini istediğimizi söyledik.
            "filter": 1,  # 1 = en yeni incelemeler, bu sayede sonunda boş liste dönüp döngü bitiyor.
            "languages": ["all"],  # Tüm dillerdeki incelemeleri istedik.
            "num_per_page": 100,  # Sayfa başına izin verilen en yüksek inceleme sayısını (100) seçtik.
            "cursor": cursor,  # Hangi sayfada kaldığımızı Steam'e bildirdik.
        }

        response = requests.get(url, params={"input_json": json.dumps(girdi)}, headers=headers, timeout=15)  # İsteği parametrelerle birlikte gönderdik, 15 saniyede cevap gelmezse vazgeçsin dedik.

        if response.status_code != 200:  # Cevap başarılı değilse hata durumunu kontrol ettik.
            print(f"API bağlantı hatası! Kod: {response.status_code}")  # Hatanın kodunu ekrana yazdırdık.
            break  # Hata varsa döngüyü durdurduk.

        try:  # Gelen cevabı JSON'a çevirmeyi güvenli şekilde denedik.
            sayfa = response.json()["response"]  # Veri "response" anahtarının içinde geldiği için direkt onu aldık.
        except (ValueError, KeyError):  # JSON gelmezse ya da yapı beklediğimizden farklıysa hatayı yakaladık.
            print("Steam beklenen JSON yapısını göndermedi.")  # Sorunun ne olduğunu ekrana yazdırdık.
            break  # Döngüyü durdurduk.

        incelemeler = sayfa.get("reviews", [])  # Bu sayfadaki inceleme listesini aldık, yoksa boş liste verdik.
        if not incelemeler:  # Liste boşsa artık çekecek inceleme kalmamış demektir.
            break  # Döngüyü bitirdik.

        for rv in incelemeler:  # Sayfadaki her incelemeyi tek tek dolaştık.
            tum_incelemeler.append({  # Sadece işimize yarayan alanları seçip listeye ekledik.
                "id": rv["recommendationid"],  # İncelemenin benzersiz kimliğini aldık.
                "dil": rv["language"],  # İncelemenin yazıldığı dili aldık.
                "metin": rv["review"],  # İnceleme metnini aldık.
                "olumlu": rv["voted_up"],  # Oyuncunun oyunu önerip önermediğini (True/False) aldık.
                "oy": rv["votes_up"],  # İncelemenin kaç kişi tarafından faydalı bulunduğunu aldık.
                "oynama_dk": rv["author"]["playtime_at_review"],  # Yazarın inceleme anındaki oynama süresini (dakika) aldık.
                "tarih": rv["timestamp_created"],  # İncelemenin yazılma zamanını (Unix saniyesi) aldık.
            })

        yeni_cursor = sayfa.get("cursor")  # Steam'in bir sonraki sayfa için verdiği imleci aldık.
        if not yeni_cursor or yeni_cursor == cursor:  # İmleç yoksa ya da değişmediyse sayfalar bitmiş demektir.
            break  # Döngüyü bitirdik.
        cursor = yeni_cursor  # Bir sonraki turda kaldığımız yerden devam etmek için imleci güncelledik.
        print(f"{len(tum_incelemeler)} inceleme çekildi...")  # İlerlemeyi görebilmek için sayıyı ekrana yazdırdık.
        time.sleep(1)  # Steam'i yormamak ve engellenmemek için her sayfadan sonra 1 saniye bekledik.

    return tum_incelemeler[:max_reviews]  # İstediğimiz sayıdan fazlasını kesip listeyi geri döndürdük.

veri = get_steam_reviews(254700)  # Resident Evil 4 (2005) ile test ettik.
print(f"Toplam çekilen inceleme: {len(veri)}")  # Kaç inceleme çekebildiğimizi yazdırdık.
print(veri[0] if veri else "Veri yok")  # İlk incelemeyi örnek olarak ekrana yazdırdık.
