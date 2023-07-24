# simple-web-scrapper

Bu Python projesi, conf.json dosyasına girilen bilgilere dayanarak belirli saatlerde veri toplama işlemini gerçekleştiren bir web scraping uygulamasıdır.

### Gereksinimler

Projenin çalıştırılması için aşağıdaki gereksinimlere ihtiyaç vardır:

- Python (versiyon 3.x)
- MongoDB veritabanı

Ayreten, requirements.in içindeki librarylerin de **environment oluşturulduktan sonra** indirilmesi gerekmektedir.

- pip install -r requirements.in

requirements.in dosyasının içeriği

- pymongo
- requests
- beautifulsoup4
- schedule

### Kurulum

1. Proje dizinine gidin:
```bash
cd proje_dizini
```

2. Sanal ortamı oluşturun ve etkinleştirin:
```bash
python -m venv env
env/Scripts/activate   # Windows için
source env/bin/activate   # macOS veya Linux için
```

3. Gerekli Python kütüphanelerini yükleyin:
```bash
pip install -r requirements.txt
```

### Kullanım

Proje, conf.json dosyasındaki yapılandırmalara göre web sitelerinden veri çeker. *conf.json* dosyasında belirtilen saatlerde çalışarak verileri güncel tutar ve verilerde fiyat değişiklikleri varsa veritabanını günceller.

1. conf.json dosyasını yapılandırın:

```json
{
    "scrappers": [
        {
            "name": "kitapyurdu",
            "words": [
                "python"
            ],
            "url": "https://www.kitapyurdu.com/",
            "when": [
                "12:30",
                "10:30"
            ]
        },
        {
            "name": "kitapsepeti",
            "words": [
                "python"
            ],
            "url": "https://www.kitapsepeti.com/",
            "when": [
                "12:30",
                "10:30"
            ]
        }
    ]
}
```

2. Proje kök dizinindeki terminalde aşağıdaki komutları çalıştırın:

```bash
docker-compose up -d --build   # to build docker images.
python ./src/main.py   # run
```

## Lisans
Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için LICENSE dosyasına bakın.

