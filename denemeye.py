from PIL import Image, ImageTk, ImageOps
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import random
import threading
import time
import os

class BuyukSayilarYasasiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Büyük Sayılar Yasası - 2025 TÜBİTAK")
        self.attributes("-fullscreen", True)

        self.colors = ["#ff4d4d", "#ffa64d", "#ffff66", "#66ff66", "#66b3ff", "#bf80ff"]
        self.color_index = 0

        self.update_idletasks()
        self.w, self.h = self.winfo_screenwidth(), self.winfo_screenheight()

        # Canvas oluştur
        self.canvas = tk.Canvas(self, width=self.w, height=self.h, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Arka plan yükle
        if os.path.exists("background.jpg"):
            bg_image = Image.open("background.jpg").resize((self.w, self.h), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw", tags="background")
        else:
            print("background.jpg bulunamadı!")
            self.bg_photo = None

        self.baslangic_ekrani()
        self.after(600, self.baslik_renk_efekti)

    def baslangic_ekrani(self):
        # Sadece widgetları temizle (arka planı silme)
        self.canvas.delete("widget")

        # Başlık
        self.title_label = tk.Label(self, text="BÜYÜK SAYILAR YASASI", font=("Arial", 42, "bold"),
                                    bg="#000000", fg="white")
        self.canvas.create_window(self.w//2, 100, window=self.title_label, tags="widget")

        # Slider
        self.slider = tk.Scale(self, from_=1000, to=10000, orient="horizontal", resolution=100,
                              length=500, tickinterval=1000, bg="#1a1a1a", fg="white",
                              label="Deneme Sayısı Seçin", font=("Arial", 14), troughcolor="#444")
        self.slider.set(5000)
        self.canvas.create_window(self.w//2, 200, window=self.slider, tags="widget")

        # Başlat butonu
        btn_start = tk.Button(self, text="Simülasyonu Başlat", font=("Arial", 18, "bold"),
                              bg="green", fg="white", command=self.baslat_gecis)
        self.canvas.create_window(self.w//2, 300, window=btn_start, tags="widget")

        # Çıkış butonu
        btn_exit = tk.Button(self, text="Çıkış", font=("Arial", 12),
                             bg="red", fg="white", command=self.destroy)
        self.canvas.create_window(self.w//2, self.h - 50, window=btn_exit, tags="widget")

        # Logoları göster
        self.resimleri_goster()

    def baslik_renk_efekti(self):
        if hasattr(self, "title_label"):
            try:
                self.title_label.config(fg=self.colors[self.color_index])
                self.color_index = (self.color_index + 1) % len(self.colors)
            except:
                pass
        self.after(600, self.baslik_renk_efekti)

    def baslat_gecis(self):
        self.canvas.delete("widget")

        self.status_label = tk.Label(self, text="Simülasyon hazırlanıyor...", font=("Arial", 18),
                                     bg="#000000", fg="white")
        self.canvas.create_window(self.w//2, 100, window=self.status_label, tags="widget")

        self.progress = ttk.Progressbar(self, length=500, mode="determinate")
        self.canvas.create_window(self.w//2, 150, window=self.progress, tags="widget")

        threading.Thread(target=self.simulasyonu_calistir, daemon=True).start()

    def simulasyonu_calistir(self):
        deneme_sayisi = self.slider.get()
        yazi = tura = kiz = erkek = 0
        zar = [0] * 6
        yazi_sayilari, tura_sayilari = [], []
        kiz_sayilari, erkek_sayilari = [], []
        zar_sayilari = [[] for _ in range(6)]

        sozler = [
            "🎲 Zarlar yuvarlanıyor...", "🪙 Yazı tura atılıyor...",
            "👶 Cinsiyet belirleniyor...", "📊 Sonuçlar hesaplanıyor...",
            "💭 Hayallerin kadar büyüksün.", "🌌 Evren anlamla doludur.",
            "📚 Bilgi güçtür.", "🌠 2025 TÜBİTAK: Geleceği birlikte yazıyoruz!"
        ]
        random.shuffle(sozler)

        self.progress["maximum"] = deneme_sayisi

        for step in range(1, deneme_sayisi + 1):
            if step % (deneme_sayisi // 8) == 0 and sozler:
                self.status_label.config(text=sozler.pop(0))
                time.sleep(random.uniform(1.0, 1.5))

            if random.choice(["Y", "T"]) == "Y":
                yazi += 1
            else:
                tura += 1
            yazi_sayilari.append(yazi / step * 100)
            tura_sayilari.append(tura / step * 100)

            if random.choice(["XX", "XY"]) == "XX":
                kiz += 1
            else:
                erkek += 1
            kiz_sayilari.append(kiz / step * 100)
            erkek_sayilari.append(erkek / step * 100)

            gelen = random.randint(0, 5)
            zar[gelen] += 1
            for i in range(6):
                oran = zar[i] / step * 100
                zar_sayilari[i].append(oran)

            if step % 100 == 0:
                self.progress["value"] = step

        self.status_label.config(text="Grafikler hazırlanıyor...")
        time.sleep(1)
        self.grafikleri_goster(yazi_sayilari, tura_sayilari, zar_sayilari, kiz_sayilari, erkek_sayilari)

    def grafikleri_goster(self, yazi_sayilari, tura_sayilari, zar_sayilari, kiz_sayilari, erkek_sayilari):
        fig, axs = plt.subplots(1, 3, figsize=(18, 5))
        axs[0].plot(yazi_sayilari, label=f"Yazı %{yazi_sayilari[-1]:.2f}")
        axs[0].plot(tura_sayilari, label=f"Tura %{tura_sayilari[-1]:.2f}")
        axs[0].axhline(50, color='gray', linestyle='--')
        axs[0].legend(); axs[0].set_title("Yazı Tura"); axs[0].grid()

        renkler = ['blue', 'orange', 'green', 'red', 'purple', 'brown']
        for i in range(6):
            axs[1].plot(zar_sayilari[i], label=f"{i+1} %{zar_sayilari[i][-1]:.2f}", color=renkler[i])
        axs[1].axhline(100/6, color='gray', linestyle='--')
        axs[1].legend(); axs[1].set_title("Zar"); axs[1].grid()

        axs[2].plot(kiz_sayilari, label=f"Kız %{kiz_sayilari[-1]:.2f}")
        axs[2].plot(erkek_sayilari, label=f"Erkek %{erkek_sayilari[-1]:.2f}")
        axs[2].axhline(50, color='gray', linestyle='--')
        axs[2].legend(); axs[2].set_title("Cinsiyet"); axs[2].grid()

        plt.tight_layout()
        plt.show()
        self.baslangic_ekrani()

    def resimleri_goster(self):
        dosyalar = ["karamehmet59.png", "meb.png"]
        boyutlar = [(400, 400), (400, 400)]  # Aynı boyutlarda

        toplam_genislik = sum([b[0] for b in boyutlar])
        bosluk_sayisi = len(dosyalar) + 1
        bosluk = (self.w - toplam_genislik) // bosluk_sayisi

        self.fotolar = []
        x = bosluk
        y = 450

        for i, dosya in enumerate(dosyalar):
            try:
                img = Image.open(dosya).resize(boyutlar[i], Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.fotolar.append(photo)
                self.canvas.create_image(x + boyutlar[i][0]//2, y, image=photo, tags="widget")
                x += boyutlar[i][0] + bosluk
            except Exception as e:
                print(f"{dosya} yüklenemedi:", e)

if __name__ == "__main__":
    app = BuyukSayilarYasasiApp()
    app.mainloop()
