import customtkinter as ctk
import json
import os
import sys
import pygame

# Set Tema UI (Dark mode dengan aksen dark-blue)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def resource_path(relative_path):
    """ Dapatkan laluan tepat untuk fail aset sama ada run skrip biasa atau dari .exe PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AppBelajar(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Tetapan Utama Tetingkap
        self.title("Aplikasi Latihan Belajar")
        self.geometry("650x550")
        self.resizable(False, False)

        # Inisialisasi Audio Pygame
        pygame.mixer.init()
        self.sound_correct = self.load_sound("correct.wav")
        self.sound_wrong = self.load_sound("wrong.wav")

        # Muat Turun Soalan dari JSON
        self.soalan_list = self.load_soalan()
        self.current_index = 0
        self.score = 0

        # Bina Antaramuka (UI)
        self.setup_ui()
        self.papar_soalan()

    def load_sound(self, filename):
        path = resource_path(filename)
        if os.path.exists(path):
            return pygame.mixer.Sound(path)
        return None

    def play_sound(self, sound_object):
        if sound_object:
            sound_object.play()

    def load_soalan(self):
        json_path = resource_path("soalan.json")
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return [{"soalan": "Fail soalan.json tidak dijumpai!", "pilihan": ["-"], "jawapan": "-"}]

    def setup_ui(self):
        # Kad Utama (Background Container)
        self.main_card = ctk.CTkFrame(self, corner_radius=20, fg_color="#1E1E2E")
        self.main_card.pack(pady=20, padx=20, fill="both", expand=True)

        # Header / Skor Bar
        self.score_label = ctk.CTkLabel(
            self.main_card, 
            text="Skor: 0", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#89B4FA"
        )
        self.score_label.pack(anchor="ne", padx=25, pady=(15, 0))

        # Kad Soalan
        self.question_card = ctk.CTkFrame(self.main_card, corner_radius=15, fg_color="#313244")
        self.question_card.pack(pady=15, padx=20, fill="x")

        self.lbl_soalan = ctk.CTkLabel(
            self.question_card, 
            text="Soalan...", 
            font=ctk.CTkFont(size=18, weight="bold"),
            wraplength=520,
            text_color="#CDD6F4"
        )
        self.lbl_soalan.pack(pady=25, padx=15)

        # Ruang Butang Jawapan
        self.btn_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.btn_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.buttons = []
        for i in range(4):
            btn = ctk.CTkButton(
                self.btn_frame,
                text="",
                font=ctk.CTkFont(size=15, weight="bold"),
                height=50,
                corner_radius=12,
                fg_color="#45475A",
                hover_color="#585B70",
                text_color="#F5E0DC",
                command=lambda idx=i: self.semak_jawapan(idx)
            )
            btn.pack(pady=6, fill="x")
            self.buttons.append(btn)

        # Label Maklum Balas (Feedback)
        self.lbl_feedback = ctk.CTkLabel(
            self.main_card, 
            text="", 
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.lbl_feedback.pack(pady=10)

    def papar_soalan(self):
        if self.current_index < len(self.soalan_list):
            item = self.soalan_list[self.current_index]
            self.lbl_soalan.configure(text=f"{self.current_index + 1}. {item['soalan']}")
            self.lbl_feedback.configure(text="")

            for i, pilihan in enumerate(item['pilihan']):
                self.buttons[i].configure(
                    text=pilihan, 
                    state="normal", 
                    fg_color="#45475A",
                    hover_color="#585B70"
                )
        else:
            self.tamat_kuiz()

    def semak_jawapan(self, idx_pilihan):
        item = self.soalan_list[self.current_index]
        jawapan_user = item['pilihan'][idx_pilihan]
        jawapan_betul = item['jawapan']

        # Nyahaktifkan semua butang sementara
        for btn in self.buttons:
            btn.configure(state="disabled")

        if jawapan_user == jawapan_betul:
            self.score += 10
            self.score_label.configure(text=f"Skor: {self.score}")
            self.buttons[idx_pilihan].configure(fg_color="#A6E3A1", text_color="#11111B") # Hijau
            self.lbl_feedback.configure(text="Tepat Sekali! 🎉", text_color="#A6E3A1")
            self.play_sound(self.sound_correct)
        else:
            self.buttons[idx_pilihan].configure(fg_color="#F38BA8", text_color="#11111B") # Merah
            self.lbl_feedback.configure(text=f"Salah! Jawapan betul: {jawapan_betul}", text_color="#F38BA8")
            self.play_sound(self.sound_wrong)

        # Pergi ke soalan seterusnya selepas 1.5 saat
        self.after(1500, self.soalan_seterusnya)

    def soalan_seterusnya(self):
        self.current_index += 1
        self.papar_soalan()

    def tamat_kuiz(self):
        self.question_card.pack_forget()
        self.btn_frame.pack_forget()
        self.lbl_feedback.pack_forget()

        lbl_tamat = ctk.CTkLabel(
            self.main_card,
            text=f"Tahniah! Kuiz Selesai! 🏆\n\nJumlah Skor Anda: {self.score}",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#FAB387"
        )
        lbl_tamat.pack(expand=True)

if __name__ == "__main__":
    app = AppBelajar()
    app.mainloop()