from PIL import Image, ImageTk
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
        self.title("Buyuk Sayilar Yasasi - 2025 TUBITAK")
        self.attributes("-fullscreen", True)
        self.configure(bg="black")

        self.colors = ["#ff4d4d", "#ffa64d", "#ffff66", "#66ff66", "#66b3ff", "#bf80ff"]
        self.color_index = 0

        self.update_idletasks()  # pencere boyutunu doğru alabilmek için
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()

        try:
            if os.path.exists("background.jpg"):
                bg_image = Image.open("background.jpg").resize((w, h), Image.ANTIALIAS)
                self.bg_photo = ImageTk.PhotoImage(bg_image)
                bg_label = tk.Label(self, image=self.bg_photo)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                bg_label.lower()
            else:
                print("background.jpg bulunamadi!")
        except Exception as e:
            print("Arka plan yuklenemedi:", e)

        self.baslangic_ekrani()
        self.after(600, self.baslik_renk_efekti)

    def baslangic_ekrani(self):
        for widget in self.winfo_children():
            widget.place_forget()
            widget.pack_forget()

        self.title_label = tk.Label(self, text="BUYUK SAYILAR YASASI", font=("Arial", 42, "bold"),
                                    bg="black", fg="white")
        self.title_label.pack(pady=40)

        self.slider = tk.Scale(self, from_=1000, to=10000, orient="horizontal", resolution=100,
                               length=500, tickinterval=1000, bg="#1a1a1a", fg="white",
                               label="Deneme Sayisi Secin", font=("Arial", 14), troughcolor="#444")
        self.slider.set(5000)
        self.slider.pack(pady=30)

        tk.Button(self, text="Simulasyonu Baslat", font=("Arial", 18, "bold"),
                  bg="green", fg="white", command=self.baslat_gecis).pack(pady=20)

        tk.Button(self, text="Cikis", font=("Arial", 12),
                  bg="red", fg="white", command=self.destroy).pack(side="bottom", pady=10)

    def baslik_renk_efekti(self):
        if hasattr(self, "title_label"):
            try:
                self.title_label.config(fg=self.colors[self.color_index])
                self.color_index = (self.color_index + 1) % len(self.colors)
                self.after(600, self.baslik_renk_efekti)
            except:
                pass

    def baslat_gecis(self):
        for widget in self.winfo_children():
            widget.pack_forget()
            widget.place_forget()

        self.status_label = tk.Label(self, text="Simulasyon hazirlaniyor...", font=("Arial", 18),
                                     bg="black", fg="white")
        self.status_label.pack(pady=40)

        self.progress = ttk.Progressbar(self, length=500, mode="determinate")
        self.progress.pack(pady=10)

        threading.Thread(target=self.simulasyonu_calistir, daemon=True).start()

    def simulasyonu_calistir(self):
        deneme_sayisi = self.slider.get()
        yazi = tura = kiz = erkek = 0
        zar = [0] * 6
        yazi_sayilari, tura_sayilari = [], []
        kiz_sayilari, erkek_sayilari = [], []
        zar_sayilari = [[] for _ in range(6)]

        sozler = [
            "🎲 Zarlar yuvarlaniyor...", "🪙 Yazi tura atiliyor...",
            "👶 Cinsiyet belirleniyor...", "📊 Sonuçlar hesaplaniyor...",
            "💭 Hayallerin kadar buyuksun.", "🌌 Evren anlamla doludur.",
            "📚 Bilgi guçtur.", "🌠 2025 TuBITAK: Geleceği birlikte yaziyoruz!"
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

        self.status_label.config(text="Grafikler hazirlaniyor...")
        time.sleep(1)
        self.grafikleri_goster(yazi_sayilari, tura_sayilari, zar_sayilari, kiz_sayilari, erkek_sayilari)

    def grafikleri_goster(self, yazi_sayilari, tura_sayilari, zar_sayilari, kiz_sayilari, erkek_sayilari):
        fig, axs = plt.subplots(1, 3, figsize=(18, 5))
        axs[0].plot(yazi_sayilari, label=f"Yazi %{yazi_sayilari[-1]:.2f}")
        axs[0].plot(tura_sayilari, label=f"Tura %{tura_sayilari[-1]:.2f}")
        axs[0].axhline(50, color='gray', linestyle='--')
        axs[0].legend(); axs[0].set_title("Yazi Tura"); axs[0].grid()

        renkler = ['blue', 'orange', 'green', 'red', 'purple', 'brown']
        for i in range(6):
            axs[1].plot(zar_sayilari[i], label=f"{i+1} %{zar_sayilari[i][-1]:.2f}", color=renkler[i])
        axs[1].axhline(100/6, color='gray', linestyle='--')
        axs[1].legend(); axs[1].set_title("Zar"); axs[1].grid()

        axs[2].plot(kiz_sayilari, label=f"Kiz %{kiz_sayilari[-1]:.2f}")
        axs[2].plot(erkek_sayilari, label=f"Erkek %{erkek_sayilari[-1]:.2f}")
        axs[2].axhline(50, color='gray', linestyle='--')
        axs[2].legend(); axs[2].set_title("Cinsiyet"); axs[2].grid()

        plt.tight_layout()
        plt.show()
        self.baslangic_ekrani()

if __name__ == "__main__":
    app = BuyukSayilarYasasiApp()
    app.mainloop()
