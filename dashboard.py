import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Atur tema dasar CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Smart Water Filter Dashboard")
        self.geometry("1200x780")

        # --- Variabel Inti untuk Logika Filter ---
        self.max_uses = 50
        self.current_uses = 42 # -> 16% sisa
        self.life_remaining_percent = (self.max_uses - self.current_uses) / self.max_uses

        # --- Variabel Dinamis untuk System Info ---
        self.current_pressure = 55 # PSI (Good)
        # Coba ubah ini ke 30 (Low) atau 90 (High) untuk melihat warna berubah
        
        # --- PENAMBAHAN: Variabel Dinamis untuk Status Komponen ---
        # (Anda bisa mengubah status ini secara dinamis nanti)
        self.component_data = [
            ("Pump Status", "OK"),
            ("TDS Meter", "ACTIVE"),
            ("Suhu Sensor", "ACTIVE"),
            ("Ultrasonic", "CHECK"),
        ]
        
        # --- Variabel untuk menampung widget yang perlu di-update ---
        self.chart_canvas = None
        self.chart_frame = None
        self.btn_1 = None
        self.btn_2 = None
        self.btn_3 = None

        # --- Konfigurasi Grid Utama ---
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0) # Title
        self.grid_rowconfigure(1, weight=0) # Notification (Sekarang digunakan)
        self.grid_rowconfigure(2, weight=1) # KPI Cards
        self.grid_rowconfigure(3, weight=4) # Main Content (Graph)
        
        # --- Panggil semua elemen UI ---
        self.create_title_header()
        self.create_kpi_cards()
        self.create_main_content()
        self.create_sidebar()

        # --- Inisialisasi status tombol dan grafik ---
        self.update_graph_range("1-50") # Set '1-50 Uses' sebagai default aktif

    def create_title_header(self):
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")
        
        title_label = ctk.CTkLabel(title_frame, text="Smart Water Filter", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(title_frame, text="Real-time monitoring of your water system.", font=ctk.CTkFont(size=14), text_color="gray")
        subtitle_label.pack(anchor="w", pady=(0, 5))

    def create_kpi_cards(self):
        kpi_container = ctk.CTkFrame(self, fg_color="transparent")
        kpi_container.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        kpi_container.grid_columnconfigure((0, 1, 2), weight=1)

        kpi_data = [
            {"title": "Total Dissolved Solids (TDS)", "before": "280 ppm", "after": "15 ppm"},
            {"title": "Electrical Conductivity (EC)", "before": "560 µS/cm", "after": "30 µS/cm"},
            {"title": "Temperature", "before": "22°C", "after": "21°C"}
        ]

        for i, data in enumerate(kpi_data):
            card = ctk.CTkFrame(kpi_container, corner_radius=10)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            card.grid_rowconfigure((1,2), weight=1)
            card.grid_columnconfigure((0,2), weight=1)
            title = ctk.CTkLabel(card, text=data["title"], font=ctk.CTkFont(size=12), text_color="gray")
            title.grid(row=0, column=0, columnspan=3, padx=15, pady=(15, 5), sticky="w")
            before_val = ctk.CTkLabel(card, text=data["before"], font=ctk.CTkFont(size=24, weight="bold"), text_color="#E85D5D")
            before_val.grid(row=1, column=0, padx=15, pady=5, sticky="s")
            before_lab = ctk.CTkLabel(card, text="BEFORE", font=ctk.CTkFont(size=10), text_color="gray")
            before_lab.grid(row=2, column=0, padx=15, pady=(0, 15), sticky="n")
            arrow = ctk.CTkLabel(card, text="→", font=ctk.CTkFont(size=24), text_color="gray")
            arrow.grid(row=1, column=1, rowspan=2, pady=10)
            after_val = ctk.CTkLabel(card, text=data["after"], font=ctk.CTkFont(size=24, weight="bold"), text_color="#5DE89D")
            after_val.grid(row=1, column=2, padx=15, pady=5, sticky="s")
            after_lab = ctk.CTkLabel(card, text="AFTER", font=ctk.CTkFont(size=10), text_color="gray")
            after_lab.grid(row=2, column=2, padx=15, pady=(0, 15), sticky="n")

    def create_main_content(self):
        graph_frame = ctk.CTkFrame(self, corner_radius=10)
        graph_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        graph_frame.grid_rowconfigure(2, weight=1)
        graph_frame.grid_columnconfigure(0, weight=1)

        graph_header = ctk.CTkFrame(graph_frame, fg_color="transparent")
        graph_header.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        graph_title = ctk.CTkLabel(graph_header, text="Filter Life Degradation", font=ctk.CTkFont(size=18, weight="bold"))
        graph_title.pack(side="left")

        toggle_frame = ctk.CTkFrame(graph_header, fg_color="transparent")
        toggle_frame.pack(side="right")
        
        self.btn_1 = ctk.CTkButton(toggle_frame, text="1-10 Uses", fg_color="transparent", width=80,
                                   command=lambda: self.update_graph_range("1-10"))
        self.btn_1.pack(side="left", padx=2)
        
        self.btn_2 = ctk.CTkButton(toggle_frame, text="1-50 Uses", width=80,
                                   command=lambda: self.update_graph_range("1-50"))
        self.btn_2.pack(side="left", padx=2)
        
        self.btn_3 = ctk.CTkButton(toggle_frame, text="All (Projected)", fg_color="transparent", width=90,
                                   command=lambda: self.update_graph_range("All"))
        self.btn_3.pack(side="left", padx=2)

        consumption_frame = ctk.CTkFrame(graph_frame, fg_color="transparent")
        consumption_frame.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        con_label = ctk.CTkLabel(consumption_frame, text="Current Status", font=ctk.CTkFont(size=12), text_color="gray")
        con_label.pack(anchor="w")
        con_val_str = f"{self.life_remaining_percent*100:.0f}% Remaining"
        con_val = ctk.CTkLabel(consumption_frame, text=con_val_str, font=ctk.CTkFont(size=36, weight="bold"))
        con_val.pack(anchor="w", side="left")
        con_change_str = f"{self.current_uses} Uses"
        con_change = ctk.CTkLabel(consumption_frame, text=con_change_str, text_color="#E85D5D", font=ctk.CTkFont(size=12))
        con_change.pack(anchor="w", side="left", padx=10, pady=(10,0))

        self.chart_frame = ctk.CTkFrame(graph_frame, fg_color="transparent")
        self.chart_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def update_graph_range(self, range_key):
        # 1. Update style tombol
        active_color = ("#3A7EBF", "#3A7EBF") 
        transparent = "transparent"
        self.btn_1.configure(fg_color=active_color if range_key == "1-10" else transparent)
        self.btn_2.configure(fg_color=active_color if range_key == "1-50" else transparent)
        self.btn_3.configure(fg_color=active_color if range_key == "All" else transparent)

        # 2. Siapkan data berdasarkan 'range_key'
        base_x = [0, 5, 10, 15, 20, 25, 30, 35, 40, self.current_uses] 
        base_y = [100, 95, 88, 80, 70, 60, 50, 40, 25, self.life_remaining_percent * 100]

        if range_key == "1-10":
            x_data = [d for d in base_x if d <= 10]
            y_data = base_y[:len(x_data)]
        elif range_key == "1-50":
            x_data = base_x
            y_data = base_y
        elif range_key == "All":
            x_data = base_x + [self.max_uses]
            y_data = base_y + [0] # Proyeksi akan habis di 0%

        # 3. Panggil fungsi untuk menggambar ulang grafik
        self.embed_matplotlib_graph(x_data, y_data)

    def embed_matplotlib_graph(self, x_data, y_data):
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()

        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#2B2B2B') 
        ax.set_facecolor('#2B2B2B')
        
        if self.life_remaining_percent < 0.2:
            plot_color = "#E85D5D" # Red
        elif self.life_remaining_percent < 0.5:
            plot_color = "#f2b94a" # Yellow
        else:
            plot_color = "#5DE89D" # Green
            
        ax.plot(x_data, y_data, color=plot_color, linewidth=2, marker='o', markersize=4)
        ax.fill_between(x_data, y_data, color=plot_color, alpha=0.1)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('gray')
        ax.spines['bottom'].set_color('gray')
        
        ax.set_xlabel("Number of Uses", color='gray')
        ax.set_ylabel("Filter Life %", color='gray')
        
        ax.tick_params(axis='x', colors='gray')
        ax.tick_params(axis='y', colors='gray')
        
        ax.set_ylim(0, 105)
        ax.set_xlim(-1, max(x_data) + 1) 

        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

    def create_sidebar(self):
        sidebar_frame = ctk.CTkFrame(self, fg_color="transparent")
        sidebar_frame.grid(row=2, column=1, rowspan=2, padx=20, pady=10, sticky="nsew")
        
        sidebar_frame.grid_rowconfigure(0, weight=0)
        sidebar_frame.grid_rowconfigure(1, weight=0)
        sidebar_frame.grid_rowconfigure(2, weight=1) # <-- Ini akan diisi oleh card baru

        self.create_filter_status_card(sidebar_frame)
        self.create_system_info_card(sidebar_frame)
        # --- PERUBAHAN PANGGILAN FUNGSI ---
        self.create_component_status_card(sidebar_frame) 

    def create_filter_status_card(self, parent_frame):
        filter_card = ctk.CTkFrame(parent_frame, corner_radius=10)
        filter_card.grid(row=0, column=0, padx=0, pady=10, sticky="new")
        
        title = ctk.CTkLabel(filter_card, text="Filter Status", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(padx=20, pady=(20, 10), anchor="w")
        
        usage_frame = ctk.CTkFrame(filter_card, fg_color="transparent")
        usage_frame.pack(padx=20, pady=(5,0), fill="x")
        usage_label = ctk.CTkLabel(usage_frame, text="Current Usage", text_color="gray")
        usage_label.pack(side="left")
        usage_count_str = f"{self.current_uses} / {self.max_uses} uses"
        usage_count = ctk.CTkLabel(usage_frame, text=usage_count_str, font=ctk.CTkFont(weight="bold"))
        usage_count.pack(side="right")

        status_frame = ctk.CTkFrame(filter_card, fg_color="transparent")
        status_frame.pack(padx=20, pady=(5,5), fill="x")
        life_label = ctk.CTkLabel(status_frame, text="Life Remaining", text_color="gray")
        life_label.pack(side="left")
        percent_str = f"{self.life_remaining_percent*100:.0f}%"
        percent_label = ctk.CTkLabel(status_frame, text=percent_str, font=ctk.CTkFont(weight="bold"))
        percent_label.pack(side="right")

        if self.life_remaining_percent < 0.2:
            progress_color = "#E85D5D" # Red
        elif self.life_remaining_percent < 0.5:
            progress_color = "#f2b94a" # Yellow
        else:
            progress_color = "#5DE89D" # Green

        progress = ctk.CTkProgressBar(filter_card, height=8)
        progress.set(self.life_remaining_percent)
        progress.configure(progress_color=progress_color) 
        progress.pack(padx=20, pady=(0, 20), fill="x")

    def create_system_info_card(self, parent_frame):
        sys_card = ctk.CTkFrame(parent_frame, corner_radius=10)
        sys_card.grid(row=1, column=0, padx=0, pady=10, sticky="new")
        
        title = ctk.CTkLabel(sys_card, text="System Information", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(padx=20, pady=(20, 10), anchor="w")

        sys_data = {
            "Uptime": "12d 4h 32m",
            "Flow Rate": "1.2 GPM",
            "Water Pressure": f"{self.current_pressure} PSI", 
            "Firmware Version": "v2.1.3"
        }

        for key, value in sys_data.items():
            info_frame = ctk.CTkFrame(sys_card, fg_color="transparent")
            info_frame.pack(padx=20, pady=7, fill="x") 
            
            key_label = ctk.CTkLabel(info_frame, text=key, text_color="gray")
            key_label.pack(side="left")
            
            val_color = "white" # Default
            
            if key == "Water Pressure":
                if self.current_pressure < 40:      
                    val_color = "#E85D5D" # Red
                elif self.current_pressure > 80: 
                    val_color = "#f2b94a" # Yellow
                else:                               
                    val_color = "#5DE89D" # Green

            value_label = ctk.CTkLabel(info_frame, text=value, font=ctk.CTkFont(weight="bold"), text_color=val_color)
            value_label.pack(side="right")

    # --- FUNGSI BARU (PENGGANTI QUICK ACTIONS) ---
    def create_component_status_card(self, parent_frame):
        """Membuat card diagnostik untuk status komponen individual."""
        
        status_card = ctk.CTkFrame(parent_frame, corner_radius=10)
        # sticky="nsew" agar card ini mengisi sisa ruang di grid sidebar (row=2)
        status_card.grid(row=2, column=0, padx=0, pady=10, sticky="nsew")

        title = ctk.CTkLabel(status_card, text="Component Status", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(padx=20, pady=(20, 10), anchor="w")

        # Definisikan palet warna untuk status
        status_colors = {
            "OK": "#5DE89D",      # Green
            "ACTIVE": "#3A7EBF",  # Blue
            "CHECK": "#f2b94a",   # Yellow
            "ERROR": "#E85D5D"    # Red
        }

        # Loop melalui data komponen yang disimpan di self.component_data
        for i, (name, status) in enumerate(self.component_data):
            
            # Dapatkan warna, default ke "gray" jika status tidak dikenal
            color = status_colors.get(status, "gray") 
            
            # Tentukan padding: item terakhir mendapat padding bawah ekstra
            pady_config = 7
            if i == len(self.component_data) - 1:
                pady_config = (7, 20) 

            # Frame untuk setiap baris (Nama Komponen | Indikator | Status)
            item_frame = ctk.CTkFrame(status_card, fg_color="transparent")
            item_frame.pack(padx=20, pady=pady_config, fill="x")

            # Label Nama (rata kiri)
            name_label = ctk.CTkLabel(item_frame, text=name, text_color="gray")
            name_label.pack(side="left")
            
            # Label Status (rata kanan)
            status_label = ctk.CTkLabel(item_frame, text=status, font=ctk.CTkFont(weight="bold"), text_color=color)
            status_label.pack(side="right")
            
            # Indikator visual "dot" (rata kanan, sebelum status)
            dot_label = ctk.CTkLabel(item_frame, text="●", font=ctk.CTkFont(size=14), text_color=color)
            dot_label.pack(side="right", padx=(0, 5))


# --- Jalankan Aplikasi ---
if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()