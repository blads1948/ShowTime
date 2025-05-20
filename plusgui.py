
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import random
import threading
import time

class BuyukSayilarYasasiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Büyük Sayılar Yasası - 2025 TÜBİTAK")
        self.geometry("1200x800")
        self.configure(bg="black")
        self.resizable(False, False)

        # Renk geçişli başlık efekti
        self.colors = ["#ff4d4d", "#ffa64d", "#ffff66", "#66ff66", "#66b3ff", "#bf80ff"]
        self.color_index = 0

        try:
            bg_image = Image.open("background.jpg")
            self.bg_photo = ImageTk.PhotoImage(bg_image.resize((1200, 800)))
            bg_label = tk.Label(self, image=self.bg_photo)
            bg_label.place(relwidth=1, relheight=1)
        except:
            self.configure(bg="#0a0a0a")

        self.baslangic_ekrani()
        self.after(300, self.baslik_renk_efekti)

    def baslik_renk_efekti(self):
        renk = self.colors[self.color_index]
        self.title_label.config(fg=renk)
        self.color_index = (self.color_index + 1) % len(self.colors)
        self.after(300, self.baslik_renk_efekti)

    def baslangic_ekrani(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.title_label = tk.Label(self, text="BÜYÜK SAYILAR YASASI", font=("Arial", 42, "bold"),
                                    bg="#000000", fg="white")
        self.title_label.pack(pady=40)

        alt_yazi = tk.Label(self, text="2025 TÜBİTAK Proje Sunumu", font=("Arial", 18),
                            bg="#000000", fg="gray")
        alt_yazi.pack()

        self.slider = tk.Scale(self, from_=1000, to=10000, orient="horizontal", resolution=100,
                               length=500, tickinterval=1000, bg="#1a1a1a", fg="white",
                               label="Deneme Sayısı Seçin", font=("Arial", 14), troughcolor="#444")
        self.slider.set(5000)
        self.slider.pack(pady=40)

        tk.Button(self, text="🚀 Simülasyonu Başlat", font=("Arial", 18, "bold"),
                  bg="#00cc66", fg="white", command=self.baslat_gecis).pack(pady=20)

        tk.Button(self, text="Çıkış", font=("Arial", 12),
                  bg="red", fg="white", command=self.destroy).pack(side="bottom", pady=10)

    def baslat_gecis(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.status_label = tk.Label(self, text="Simülasyon hazırlanıyor...", font=("Arial", 18, "bold"),
                                     bg="black", fg="white")
        self.status_label.pack(pady=40)

        self.progress = ttk.Progressbar(self, length=600, mode="determinate")
        self.progress.pack(pady=10)
        self.update()
        threading.Thread(target=self.simulasyonu_calistir_gui_icin, daemon=True).start()

    def simulasyonu_calistir_gui_icin(self):
        deneme_sayisi = self.slider.get()
        yazi_sayilari, tura_sayilari = [], []
        kiz_sayilari, erkek_sayilari = [], []
        zar_sayilari = [[] for _ in range(6)]
        yazi = tura = kiz = erkek = 0
        zar = [0] * 6

        animasyon_yazilari = [
            "🎲 Zarlar yuvarlanıyor...", "🪙 Yazı tura atılıyor...",
            "👶 Cinsiyet belirleniyor...", "📊 Sonuçlar hesaplanıyor...",
            "💭 Hayallerin kadar büyüksün.",
            "🔑 Einstein: 'Hayal gücü bilgiden önemlidir.'",
            "🔥 Nietzsche: 'Beni öldürmeyen şey güçlendirir.'",
            "🛤️ Gandhi: 'Değişim seninle başlar.'",
            "🌌 Sagan: 'Evreni anlamak kendimizi anlamaktır.'",
            "📚 Konfüçyüs: 'Nereye gittiğini bilmiyorsan, vardığın yerin önemi yoktur.'",
            "🌠 2025 TÜBİTAK: Geleceği birlikte yazıyoruz!"
        ]
        random.shuffle(animasyon_yazilari)

        self.progress["maximum"] = deneme_sayisi

        for step in range(1, deneme_sayisi + 1):
            if step % (deneme_sayisi // 10) == 0 and animasyon_yazilari:
                mesaj = animasyon_yazilari.pop(0)
                self.status_label.config(text=mesaj)
                self.update_idletasks()
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

            if step % 50 == 0:
                self.progress["value"] = step
                self.update_idletasks()

        self.status_label.config(text="Simülasyon tamamlandı. Grafikler gösteriliyor...")
        time.sleep(1)
        self.grafikleri_goster(yazi_sayilari, tura_sayilari, zar_sayilari, kiz_sayilari, erkek_sayilari)

    def grafikleri_goster(self, yazi_sayilari, tura_sayilari, zar_sayilari, kiz_sayilari, erkek_sayilari):
        fig, axs = plt.subplots(1, 3, figsize=(18, 5))

        axs[0].plot(yazi_sayilari, label=f"Yazı: %{yazi_sayilari[-1]:.2f}")
        axs[0].plot(tura_sayilari, label=f"Tura: %{tura_sayilari[-1]:.2f}")
        axs[0].axhline(50, color='gray', linestyle='--', label="Beklenen %50")
        axs[0].set_title("Yazı Tura")
        axs[0].legend()
        axs[0].grid(True)

        renkler = ['blue', 'orange', 'green', 'red', 'purple', 'brown']
        for i in range(6):
            axs[1].plot(zar_sayilari[i], label=f"{i+1}: %{zar_sayilari[i][-1]:.2f}", color=renkler[i])
        axs[1].axhline(100/6, color='gray', linestyle='--', label="Beklenen %16.67")
        axs[1].set_title("Zar")
        axs[1].legend()
        axs[1].grid(True)

        axs[2].plot(kiz_sayilari, label=f"Kız: %{kiz_sayilari[-1]:.2f}")
        axs[2].plot(erkek_sayilari, label=f"Erkek: %{erkek_sayilari[-1]:.2f}")
        axs[2].axhline(50, color='gray', linestyle='--', label="Beklenen %50")
        axs[2].set_title("Cinsiyet")
        axs[2].legend()
        axs[2].grid(True)

        plt.tight_layout()
        plt.show()
        self.baslangic_ekrani()

if __name__ == "__main__":
    app = BuyukSayilarYasasiApp()
    app.mainloop()
