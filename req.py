from licensing.methods import Key, Helpers
import os
import sys
import requests
import zipfile
import shutil

RSAPubKey = "<RSAKeyValue><Modulus>yMMtn7k/D2sUdvs0hVBFNHYftLAf9w0ch8oHtoUDoGAoAh9BSDunGF2U/H0rHY3PkRbbSEg7VKDwyakzyo4jbj/lKgv+18JwsCjJaltmGOj31OxUhKNJ+dcsk+89xKB945X5nL2LjgvRhdgnc4V2xAQr9zhBH4KBV6jcVmuTP/CnOGoD+LYavdKB9NKDp9ebxGy61tVsVSwrtc8+AFA3eO7gh5eIkrzZZZmvdnDFgOw+BL5JJIuwUeoofH1hF4oqD2FIDGFlFzJyscsu85QHbqNFwfKyvvlN63x+WRiYcSaaY+19uJ7tu9jiTO/hlfxB6+v4fU2esEmzDFu+gPUjjQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
auth = "WyI0ODUyMjQzMCIsIi9TM3NCbDFXdFAwRmpCNXBKOS8weC9td3I3TVl5VEtQekthdFBXU3IiXQ==" 

def dogrula():
    anahtar = str(input("Doğrulama Anahtarını Girin: "))

    Helpers.WindowsOnly = True

    machine_code = Helpers.GetMachineCode()  # Makina kodunu al

    sonuc = Key.activate(token=auth, rsa_pub_key=RSAPubKey, product_id='20130', key=anahtar, machine_code=machine_code)

    if sonuc[0] == None or not Helpers.IsOnRightMachine(sonuc[0]):
        print("Lisans geçerli değil: {0}".format(sonuc[1]))
    else:
        print("Lisans geçerli!")
        indir_ve_calistir()

def indir_ve_calistir():
    # GitHub deposundaki güncelleme dosyasının URL'si
    url = "https://github.com/botyapan/aim/archive/main.zip"

    # Geçici bir konumda zip dosyasını indirin
    response = requests.get(url)
    with open("guncelleme.zip", "wb") as f:
        f.write(response.content)

    # Zip dosyasını açın
    with zipfile.ZipFile("guncelleme.zip", "r") as zip_ref:
        # Güncelleme dosyalarını ayrı bir klasöre çıkartın
        zip_ref.extractall("guncelleme_temp")

    # Zip dosyasını silin
    os.remove("guncelleme.zip")

    # Güncelleme dosyalarının bulunduğu klasördeki sürümü kontrol edin
    guncelleme_surumu = "main"  # Güncelleme dosyalarının sürümünü burada belirtin

    # Uygulamanın mevcut sürümünü burada belirtin
    mevcut_surum = "1.2.0"

    if guncelleme_surumu != mevcut_surum:
        # Güncelleme sürümü mevcut sürümden farklıysa güncellemeyi uygula

        # Hedef klasörü yedekleme
        shutil.move("hedef_klasor", "hedef_klasor_yedek")

        # Güncelleme dosyalarını hedef klasöre taşıma
        shutil.move("guncelleme_temp/aim-main", "hedef_klasor")

        # Yedek klasörü silme
        shutil.rmtree("hedef_klasor_yedek")

        # Güncelleme tamamlandı, uygulamayı yeniden başlatabilirsiniz
        print("Güncelleme tamamlandı. Uygulama yeniden başlatılıyor.")
    else:
        # Güncelleme sürümü mevcut sürümle aynıysa güncelleme yapma
        print("Mevcut sürüm zaten güncel. Güncelleme yapılmadı.")

    # Geçici klasörü silme
    shutil.rmtree("guncelleme_temp")

dogrula()
