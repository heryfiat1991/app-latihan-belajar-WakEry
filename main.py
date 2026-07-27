import json
import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppBelajar(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Aplikasi Latihan Belajar PC")
        self.geometry("650x500")

        self.soalan_list = self.muat_soalan()
        self.indeks_soalan = 0
        self.skor = 0

        self.label_tajuk = ctk.CTkLabel(self, text="Latihan Interaktif", font=("Arial", 22, "bold"))
        self.label_tajuk.pack(pady=15)

        self.frame_soalan = ctk.CTkFrame(self, width=580, height=350, corner_radius=15)
        self.frame_soalan.pack(pady=10, padx=20, fill="both", expand=True)

        self.label_jenis = ctk.CTkLabel(self.frame_soalan, text="", font=("Arial", 12, "italic"), text_color="gray")
        self.label_jenis.pack(pady=(15, 5))

        self.label_soalan = ctk.CTkLabel(self.frame_soalan, text="", font=("Arial", 16), wraplength=500)
        self.label_soalan.pack(pady=10)

        self.frame_jawapan = ctk.CTkFrame(self.frame_soalan, fg_color="transparent")
        self.frame_jawapan.pack(pady=10, fill="x", padx=30)

        self.btn_hantar = ctk.CTkButton(self.frame_soalan, text="Semak Jawapan", command=self.semak_jawapan)
        self.btn_hantar.pack(pady=15)

        self.label_skor = ctk.CTkLabel(self, text="Skor: 0", font=("Arial", 14, "bold"))
        self.label_skor.pack(pady=10)

        self.tampil_soalan()

    def muat_soalan(self):
        try:
            with open("soalan.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Ralat", "Fail soalan.json tidak dijumpai!")
            return []

    def tampil_soalan(self):
        for widget in self.frame_jawapan.winfo_children():
            widget.destroy()

        if self.indeks_soalan < len(self.soalan_list):
            q = self.soalan_list[self.indeks_soalan]
            jenis_str = q['jenis'].replace('_', ' ').title()
            self.label_jenis.configure(text=f"Format: {jenis_str} ({self.indeks_soalan + 1}/{len(self.soalan_list)})")
            self.label_soalan.configure(text=q['soalan'])

            if q['jenis'] in ['pilihan_ganda', 'betul_salah']:
                self.var_pilihan = ctk.StringVar(value="")
                for pilihan in q['pilihan']:
                    rb = ctk.CTkRadioButton(
                        self.frame_jawapan, 
                        text=pilihan, 
                        value=pilihan, 
                        variable=self.var_pilihan,
                        font=("Arial", 14)
                    )
                    rb.pack(anchor="w", pady=5, padx=20)

            elif q['jenis'] == 'isi_kosong':
                self.entry_jawapan = ctk.CTkEntry(
                    self.frame_jawapan, 
                    placeholder_text="Taip jawapan anda di sini...", 
                    width=300,
                    font=("Arial", 14)
                )
                self.entry_jawapan.pack(pady=10)
        else:
            self.tunjukkan_keputusan()

    def semak_jawapan(self):
        q = self.soalan_list[self.indeks_soalan]
        jawapan_user = ""

        if q['jenis'] in ['pilihan_ganda', 'betul_salah']:
            jawapan_user = self.var_pilihan.get()
        elif q['jenis'] == 'isi_kosong':
            jawapan_user = self.entry_jawapan.get().strip()

        if not jawapan_user:
            messagebox.showwarning("Peringatan", "Sila berikan jawapan terlebih dahulu!")
            return

        if jawapan_user.lower() == q['jawapan'].lower():
            self.skor += 10
            messagebox.showinfo("Tepat!", f"Jawapan anda BETUL!\n\nPenjelasan: {q['penjelasan']}")
        else:
            messagebox.showerror("Salah!", f"Jawapan anda SALAH.\nJawapan betul: {q['jawapan']}\n\nPenjelasan: {q['penjelasan']}")

        self.label_skor.configure(text=f"Skor: {self.skor}")
        self.indeks_soalan += 1
        self.tampil_soalan()

    def tunjukkan_keputusan(self):
        self.label_jenis.configure(text="Latihan Selesai!")
        self.label_soalan.configure(
            text=f"Tahniah! Anda telah menyempurnakan latihan.\n\nJumlah Skor Akhir: {self.skor} mata"
        )
        for widget in self.frame_jawapan.winfo_children():
            widget.destroy()
        self.btn_hantar.configure(state="disabled")

if __name__ == "__main__":
    app = AppBelajar()
    app.mainloop()