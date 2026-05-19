from tkinter import StringVar, messagebox, ttk, filedialog
from typing import Optional
from datetime import datetime
from app.controllers import reports_service, confederations_service, teams_service


class ReportsView(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, padding=12)

        report_notebook = ttk.Notebook(self)
        report_notebook.pack(fill="both", expand=True)

        report_notebook.add(self._build_bitacora_report(), text="Bitácora de Sesiones")
        report_notebook.add(self._build_players_report(), text="Jugadores Filtrados")
        report_notebook.add(self._build_team_value_report(), text="Valor por Equipo")
        report_notebook.add(self._build_host_countries_report(), text="Países Anfitriones")

    def _build_bitacora_report(self) -> ttk.Frame:
        frame = ttk.Frame(self, padding=12)

        ttk.Label(frame, text="Reporte de Bitácora de Sesiones", font=("", 12, "bold")).pack(anchor="w", pady=(0, 12))

        form_frame = ttk.LabelFrame(frame, text="Filtros", padding=10)
        form_frame.pack(fill="x", pady=(0, 12))

        ttk.Label(form_frame, text="Entrada (YYYY-MM-DD HH:MM[:SS]):").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.bitacora_entrada = StringVar()
        ttk.Entry(form_frame, textvariable=self.bitacora_entrada, width=24).grid(row=0, column=1, sticky="ew", padx=(0, 20))

        ttk.Label(form_frame, text="Salida (YYYY-MM-DD HH:MM[:SS]):").grid(row=0, column=2, sticky="w", padx=(0, 10))
        self.bitacora_salida = StringVar()
        ttk.Entry(form_frame, textvariable=self.bitacora_salida, width=24).grid(row=0, column=3, sticky="ew")

        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(0, 12))
        ttk.Button(btn_frame, text="Generar PDF", command=self._generate_bitacora_pdf).pack(side="left", padx=(0, 10))
        ttk.Label(btn_frame, text="Status: Listo").pack(side="left")

        info_frame = ttk.LabelFrame(frame, text="Información", padding=10)
        info_frame.pack(fill="both", expand=True)
        ttk.Label(
            info_frame,
            text="Este reporte muestra los ingresos y salidas de usuarios en la fecha y hora especificadas.",
        ).pack(anchor="w")

        return frame

    def _generate_bitacora_pdf(self) -> None:
        entrada_raw = self.bitacora_entrada.get().strip()
        salida_raw = self.bitacora_salida.get().strip()

        if not entrada_raw or not salida_raw:
            messagebox.showwarning("Campos requeridos", "Ingresa fecha y hora de entrada y salida.")
            return

        entrada = self._parse_datetime(entrada_raw)
        salida = self._parse_datetime(salida_raw)
        if not entrada or not salida:
            messagebox.showerror(
                "Formato inválido",
                "Usa el formato YYYY-MM-DD HH:MM o YYYY-MM-DD HH:MM:SS."
            )
            return

        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile=f"bitacora_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            if file_path:
                pdf_buffer = reports_service.generate_bitacora_report(entrada, salida)
                with open(file_path, "wb") as f:
                    f.write(pdf_buffer.getvalue())
                messagebox.showinfo("OK", f"PDF generado exitosamente:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {str(e)}")

    @staticmethod
    def _parse_datetime(value: str) -> Optional[str]:
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
            try:
                parsed = datetime.strptime(value, fmt)
                return parsed.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
        return None

    def _build_players_report(self) -> ttk.Frame:
        frame = ttk.Frame(self, padding=12)

        ttk.Label(frame, text="Reporte de Jugadores Filtrados", font=("", 12, "bold")).pack(anchor="w", pady=(0, 12))

        form_frame = ttk.LabelFrame(frame, text="Filtros", padding=10)
        form_frame.pack(fill="x", pady=(0, 12))

        ttk.Label(form_frame, text="Peso Mínimo (kg):").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.player_peso_min = StringVar(value="50")
        ttk.Entry(form_frame, textvariable=self.player_peso_min, width=15).grid(row=0, column=1, sticky="ew", padx=(0, 20))

        ttk.Label(form_frame, text="Peso Máximo (kg):").grid(row=0, column=2, sticky="w", padx=(0, 10))
        self.player_peso_max = StringVar(value="120")
        ttk.Entry(form_frame, textvariable=self.player_peso_max, width=15).grid(row=0, column=3, sticky="ew", padx=(0, 20))

        ttk.Label(form_frame, text="Estatura Mínima (m):").grid(row=1, column=0, sticky="w", padx=(0, 10))
        self.player_est_min = StringVar(value="1.60")
        ttk.Entry(form_frame, textvariable=self.player_est_min, width=15).grid(row=1, column=1, sticky="ew", padx=(0, 20))

        ttk.Label(form_frame, text="Estatura Máxima (m):").grid(row=1, column=2, sticky="w", padx=(0, 10))
        self.player_est_max = StringVar(value="2.10")
        ttk.Entry(form_frame, textvariable=self.player_est_max, width=15).grid(row=1, column=3, sticky="ew", padx=(0, 20))

        ttk.Label(form_frame, text="Equipo (opcional):").grid(row=2, column=0, sticky="w", padx=(0, 10))
        self.player_equipo_var = StringVar()
        self.player_equipo_combo = ttk.Combobox(form_frame, textvariable=self.player_equipo_var, state="readonly", width=20)
        self.player_equipo_combo.grid(row=2, column=1, columnspan=3, sticky="ew")

        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        self._load_equipos_for_report()

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(0, 12))
        ttk.Button(btn_frame, text="Generar PDF", command=self._generate_players_pdf).pack(side="left", padx=(0, 10))

        info_frame = ttk.LabelFrame(frame, text="Información", padding=10)
        info_frame.pack(fill="both", expand=True)
        ttk.Label(info_frame, text="Este reporte muestra jugadores filtrados por peso, estatura y equipo (opcional).").pack(anchor="w")

        return frame

    def _load_equipos_for_report(self) -> None:
        equipos = teams_service.list_teams()
        equipos_list = ["Todos"] + [e["nombre"] for e in equipos]
        self.player_equipo_combo["values"] = equipos_list
        self.player_equipo_combo.current(0)

    def _generate_players_pdf(self) -> None:
        try:
            peso_min = float(self.player_peso_min.get())
            peso_max = float(self.player_peso_max.get())
            est_min = float(self.player_est_min.get())
            est_max = float(self.player_est_max.get())
            equipo_sel = self.player_equipo_var.get()

            if peso_min >= peso_max or est_min >= est_max:
                messagebox.showerror("Error", "Los mínimos deben ser menores que los máximos.")
                return

            id_equipo = None
            if equipo_sel and equipo_sel != "Todos":
                for equipo in teams_service.list_teams():
                    if equipo["nombre"] == equipo_sel:
                        id_equipo = equipo["id_equipo"]
                        break

            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile=f"jugadores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            if file_path:
                pdf_buffer = reports_service.generate_players_report(peso_min, peso_max, est_min, est_max, id_equipo)
                with open(file_path, "wb") as f:
                    f.write(pdf_buffer.getvalue())
                messagebox.showinfo("OK", f"PDF generado exitosamente:\n{file_path}")
        except ValueError:
            messagebox.showerror("Error", "Los valores numéricos deben ser válidos.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {str(e)}")

    def _build_team_value_report(self) -> ttk.Frame:
        frame = ttk.Frame(self, padding=12)

        ttk.Label(frame, text="Reporte de Valor Total de Jugadores por Equipo", font=("", 12, "bold")).pack(anchor="w", pady=(0, 12))

        form_frame = ttk.LabelFrame(frame, text="Filtros", padding=10)
        form_frame.pack(fill="x", pady=(0, 12))

        ttk.Label(form_frame, text="Confederación:").pack(anchor="w", pady=(0, 5))
        self.conf_var = StringVar()
        self.conf_combo = ttk.Combobox(form_frame, textvariable=self.conf_var, state="readonly", width=40)
        self.conf_combo.pack(fill="x", pady=(0, 10))

        self._load_confederaciones()

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(0, 12))
        ttk.Button(btn_frame, text="Generar PDF", command=self._generate_team_value_pdf).pack(side="left", padx=(0, 10))

        info_frame = ttk.LabelFrame(frame, text="Información", padding=10)
        info_frame.pack(fill="both", expand=True)
        ttk.Label(info_frame, text="Este reporte muestra el valor total de jugadores por equipo de una confederación específica.").pack(anchor="w")

        return frame

    def _load_confederaciones(self) -> None:
        confs = confederations_service.list_confederations()
        conf_list = [c["nombre"] for c in confs]
        self.conf_combo["values"] = conf_list

    def _generate_team_value_pdf(self) -> None:
        conf_name = self.conf_var.get()
        if not conf_name:
            messagebox.showwarning("Error", "Selecciona una confederación.")
            return

        try:
            conf_id = None
            for conf in confederations_service.list_confederations():
                if conf["nombre"] == conf_name:
                    conf_id = conf["id_confederacion"]
                    break

            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile=f"valor_equipos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            if file_path:
                pdf_buffer = reports_service.generate_team_value_report(conf_id)
                with open(file_path, "wb") as f:
                    f.write(pdf_buffer.getvalue())
                messagebox.showinfo("OK", f"PDF generado exitosamente:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {str(e)}")

    def _build_host_countries_report(self) -> ttk.Frame:
        frame = ttk.Frame(self, padding=12)

        ttk.Label(frame, text="Países que Jugarán en Cada País Anfitrión", font=("", 12, "bold")).pack(anchor="w", pady=(0, 12))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(0, 12))
        ttk.Button(btn_frame, text="Generar PDF", command=self._generate_host_countries_pdf).pack(side="left", padx=(0, 10))

        info_frame = ttk.LabelFrame(frame, text="Información", padding=10)
        info_frame.pack(fill="both", expand=True)
        ttk.Label(info_frame, text="Este reporte muestra qué países participarán en cada uno de los países anfitriones (México, USA, Canadá).").pack(anchor="w")

        return frame

    def _generate_host_countries_pdf(self) -> None:
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialfile=f"paises_anfitriones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            if file_path:
                pdf_buffer = reports_service.generate_host_countries_report()
                with open(file_path, "wb") as f:
                    f.write(pdf_buffer.getvalue())
                messagebox.showinfo("OK", f"PDF generado exitosamente:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {str(e)}")
