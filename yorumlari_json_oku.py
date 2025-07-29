import json

def yorumlari_oku() -> list:
    """yorumlar_tarihli_filtreli.json dosyasını oku ve liste olarak döndür"""
    try:
        with open("yorumlar_tarihli_filtreli.json", "r", encoding="utf-8") as json_dosya:
            yorumlar = json.load(json_dosya)
            return yorumlar
    except FileNotFoundError:
        print("yorumlar_tarihli_filtreli.json bulunamadı.")
        return []
    except json.JSONDecodeError:
        print("JSON dosyası bozuk veya okunamıyor.")
        return []
