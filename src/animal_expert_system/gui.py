"""Interfaz gráfica Tkinter — Sistema experto de felinos grandes."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .domain import (
    EXAMPLE_PRESETS,
    FEATURE_LABELS,
    FEATURE_OPTIONS,
    FEATURE_ORDER,
    MODE_BACKWARD,
    MODE_FORWARD,
    MODE_LABELS,
    humanize,
)
from .inference import AnimalExpertSystem, format_result


# Paleta inspirada en la naturaleza salvaje: negro profundo, dorado, marfil
DARK_BG    = "#0d0d0d"
PANEL_BG   = "#141414"
CARD_BG    = "#1c1c1c"
ACCENT     = "#c9a84c"   # dorado
ACCENT2    = "#e8c97a"   # dorado claro
TEXT_LIGHT = "#f0ead6"   # marfil
TEXT_MID   = "#a89880"
TEXT_DIM   = "#5c5245"
SUCCESS    = "#5aad6e"
DANGER     = "#c0392b"


class FelidsExpertApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Sistema Experto — Clasificación de Felinos Grandes")
        self.geometry("1320x840")
        self.minsize(1100, 740)
        self.configure(bg=DARK_BG)

        self._engine = AnimalExpertSystem()
        self._feature_vars: dict[str, tk.StringVar] = {}
        self._mode_var = tk.StringVar(value=MODE_FORWARD)
        self._example_var = tk.StringVar(value=next(iter(EXAMPLE_PRESETS)))

        self._build_style()
        self._build_layout()
        self._load_example(self._example_var.get())

    # ------------------------------------------------------------------
    # Estilos
    # ------------------------------------------------------------------

    def _build_style(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # Frames
        style.configure("App.TFrame",     background=DARK_BG)
        style.configure("Panel.TFrame",   background=PANEL_BG)
        style.configure("Card.TFrame",    background=CARD_BG)
        style.configure("Hero.TFrame",    background=PANEL_BG)

        # Labels
        style.configure("HeroTitle.TLabel",
            background=PANEL_BG, foreground=ACCENT,
            font=("Georgia", 20, "bold"))
        style.configure("HeroSub.TLabel",
            background=PANEL_BG, foreground=TEXT_MID,
            font=("Georgia", 10, "italic"))
        style.configure("Badge.TLabel",
            background=ACCENT, foreground=DARK_BG,
            font=("Courier", 9, "bold"), padding=(10, 5))
        style.configure("CardTitle.TLabel",
            background=CARD_BG, foreground=ACCENT2,
            font=("Georgia", 13, "bold"))
        style.configure("CardText.TLabel",
            background=CARD_BG, foreground=TEXT_MID,
            font=("Courier", 9))
        style.configure("SectionLabel.TLabel",
            background=CARD_BG, foreground=TEXT_LIGHT,
            font=("Courier", 10, "bold"))
        style.configure("FieldLabel.TLabel",
            background=CARD_BG, foreground=TEXT_MID,
            font=("Courier", 9))

        # Radiobuttons
        style.configure("Mode.TRadiobutton",
            background=CARD_BG, foreground=TEXT_LIGHT,
            font=("Courier", 10),
            indicatorcolor=ACCENT)
        style.map("Mode.TRadiobutton",
            background=[("active", CARD_BG)],
            foreground=[("active", ACCENT2)])

        # Botones
        style.configure("Action.TButton",
            font=("Courier", 10, "bold"),
            padding=(12, 8),
            background=ACCENT,
            foreground=DARK_BG,
            relief="flat")
        style.map("Action.TButton",
            background=[("active", ACCENT2), ("!active", ACCENT)],
            foreground=[("active", DARK_BG)])

        style.configure("Secondary.TButton",
            font=("Courier", 10),
            padding=(12, 8),
            background=CARD_BG,
            foreground=TEXT_LIGHT,
            relief="flat")
        style.map("Secondary.TButton",
            background=[("active", "#2a2a2a")])

        # Combobox
        style.configure("TCombobox",
            fieldbackground="#242424",
            background="#242424",
            foreground=TEXT_LIGHT,
            selectbackground=ACCENT,
            selectforeground=DARK_BG,
            arrowcolor=ACCENT)

        # Treeview
        style.configure("Treeview",
            background="#181818",
            foreground=TEXT_LIGHT,
            fieldbackground="#181818",
            rowheight=26,
            font=("Courier", 9))
        style.configure("Treeview.Heading",
            background=CARD_BG,
            foreground=ACCENT,
            font=("Courier", 9, "bold"),
            relief="flat")
        style.map("Treeview",
            background=[("selected", ACCENT)],
            foreground=[("selected", DARK_BG)])

        # Scrollbar
        style.configure("TScrollbar",
            background=CARD_BG,
            troughcolor=DARK_BG,
            arrowcolor=ACCENT)

    # ------------------------------------------------------------------
    # Layout principal
    # ------------------------------------------------------------------

    def _build_layout(self) -> None:
        root = ttk.Frame(self, style="App.TFrame", padding=16)
        root.pack(fill="both", expand=True)
        root.columnconfigure(0, weight=0, minsize=320)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(1, weight=1)

        # Hero banner
        hero = ttk.Frame(root, style="Hero.TFrame", padding=(20, 16))
        hero.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 14))
        hero.columnconfigure(0, weight=1)

        ttk.Label(hero,
            text="🐆  Sistema Experto — Clasificación de Felinos Grandes",
            style="HeroTitle.TLabel",
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(hero,
            text=(
                "Ingresa las características del felino, selecciona el modo de "
                "encadenamiento y observa la inferencia taxonómica en tiempo real."
            ),
            style="HeroSub.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        self._mode_badge = ttk.Label(hero, style="Badge.TLabel")
        self._mode_badge.grid(row=0, column=1, rowspan=2, sticky="e", padx=(16, 0))

        # Panel izquierdo
        left = ttk.Frame(root, style="Card.TFrame", padding=16)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 14))
        left.columnconfigure(0, weight=1)

        # Panel derecho
        right = ttk.Frame(root, style="App.TFrame")
        right.grid(row=1, column=1, sticky="nsew")
        right.rowconfigure(0, weight=3)
        right.rowconfigure(1, weight=2)
        right.columnconfigure(0, weight=1)

        result_card = ttk.Frame(right, style="Card.TFrame", padding=16)
        result_card.grid(row=0, column=0, sticky="nsew", pady=(0, 14))
        result_card.rowconfigure(1, weight=1)
        result_card.columnconfigure(0, weight=1)

        process_card = ttk.Frame(right, style="Card.TFrame", padding=16)
        process_card.grid(row=1, column=0, sticky="nsew")
        process_card.rowconfigure(2, weight=1)
        process_card.columnconfigure(0, weight=1)

        self._build_left_panel(left)
        self._build_result_card(result_card)
        self._build_process_card(process_card)

    # ------------------------------------------------------------------
    # Panel de configuración
    # ------------------------------------------------------------------

    def _build_left_panel(self, parent: ttk.Frame) -> None:
        row = 0

        ttk.Label(parent, text="Configuración", style="CardTitle.TLabel").grid(
            row=row, column=0, sticky="w"); row += 1
        ttk.Label(parent,
            text="Modo de razonamiento y características del felino.",
            style="CardText.TLabel",
        ).grid(row=row, column=0, sticky="w", pady=(2, 12)); row += 1

        # ── Modo de encadenamiento ─────────────────────────────────────
        sep1 = tk.Frame(parent, bg=TEXT_DIM, height=1)
        sep1.grid(row=row, column=0, sticky="ew", pady=(0, 8)); row += 1

        ttk.Label(parent, text="Tipo de encadenamiento",
            style="SectionLabel.TLabel").grid(row=row, column=0, sticky="w"); row += 1

        for mode_key in (MODE_FORWARD, MODE_BACKWARD):
            ttk.Radiobutton(
                parent,
                text=MODE_LABELS[mode_key],
                value=mode_key,
                variable=self._mode_var,
                style="Mode.TRadiobutton",
                command=self._refresh_mode_badge,
            ).grid(row=row, column=0, sticky="w", pady=(4, 0)); row += 1

        # ── Ejemplos ──────────────────────────────────────────────────
        sep2 = tk.Frame(parent, bg=TEXT_DIM, height=1)
        sep2.grid(row=row, column=0, sticky="ew", pady=(12, 8)); row += 1

        ttk.Label(parent, text="Ejemplos predefinidos",
            style="SectionLabel.TLabel").grid(row=row, column=0, sticky="w"); row += 1

        combo_ex = ttk.Combobox(
            parent,
            values=list(EXAMPLE_PRESETS.keys()),
            state="readonly",
            textvariable=self._example_var,
        )
        combo_ex.grid(row=row, column=0, sticky="ew", pady=(6, 6)); row += 1

        ttk.Button(parent, text="Cargar ejemplo",
            style="Secondary.TButton",
            command=self._load_selected_example,
        ).grid(row=row, column=0, sticky="ew"); row += 1

        # ── Características ───────────────────────────────────────────
        sep3 = tk.Frame(parent, bg=TEXT_DIM, height=1)
        sep3.grid(row=row, column=0, sticky="ew", pady=(12, 8)); row += 1

        ttk.Label(parent, text="Características del felino",
            style="SectionLabel.TLabel").grid(row=row, column=0, sticky="w"); row += 1

        for feature_name in FEATURE_ORDER:
            ttk.Label(parent, text=FEATURE_LABELS[feature_name],
                style="FieldLabel.TLabel",
            ).grid(row=row, column=0, sticky="w", pady=(8, 0)); row += 1

            var = tk.StringVar()
            ttk.Combobox(
                parent,
                textvariable=var,
                state="readonly",
                values=FEATURE_OPTIONS[feature_name],
            ).grid(row=row, column=0, sticky="ew"); row += 1
            self._feature_vars[feature_name] = var

        # ── Acciones ──────────────────────────────────────────────────
        sep4 = tk.Frame(parent, bg=TEXT_DIM, height=1)
        sep4.grid(row=row, column=0, sticky="ew", pady=(12, 8)); row += 1

        btn_frame = ttk.Frame(parent, style="Card.TFrame")
        btn_frame.grid(row=row, column=0, sticky="ew"); row += 1
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        ttk.Button(btn_frame, text="▶  Inferir",
            style="Action.TButton",
            command=self._infer,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ttk.Button(btn_frame, text="✕  Limpiar",
            style="Secondary.TButton",
            command=self._clear,
        ).grid(row=0, column=1, sticky="ew")

    # ------------------------------------------------------------------
    # Panel de resultados
    # ------------------------------------------------------------------

    def _build_result_card(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Resultado taxonómico",
            style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(parent,
            text="Clasificación inferida según el modo de encadenamiento seleccionado.",
            style="CardText.TLabel",
        ).grid(row=0, column=1, sticky="e")

        tf = ttk.Frame(parent, style="Card.TFrame")
        tf.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        tf.columnconfigure(0, weight=1)
        tf.rowconfigure(0, weight=1)

        self._result_text = tk.Text(
            tf,
            wrap="word",
            bd=0, padx=14, pady=14,
            background="#181818",
            foreground=TEXT_LIGHT,
            insertbackground=ACCENT,
            font=("Courier", 11),
            relief="flat",
            selectbackground=ACCENT,
            selectforeground=DARK_BG,
        )
        self._result_text.grid(row=0, column=0, sticky="nsew")

        sb = ttk.Scrollbar(tf, orient="vertical", command=self._result_text.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self._result_text.configure(yscrollcommand=sb.set)

    # ------------------------------------------------------------------
    # Panel de proceso de inferencia
    # ------------------------------------------------------------------

    def _build_process_card(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Proceso de inferencia",
            style="CardTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(parent,
            text="Flujo de razonamiento y etapas ejecutadas por el motor.",
            style="CardText.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(2, 8))

        self._flow_canvas = tk.Canvas(
            parent, height=90,
            bg=PANEL_BG, bd=0, highlightthickness=0,
        )
        self._flow_canvas.grid(row=2, column=0, sticky="ew", pady=(0, 8))

        trace_frame = ttk.Frame(parent, style="Card.TFrame")
        trace_frame.grid(row=3, column=0, sticky="nsew")
        trace_frame.columnconfigure(0, weight=1)
        trace_frame.rowconfigure(0, weight=1)

        self._trace_tree = ttk.Treeview(
            trace_frame,
            columns=("detalle",),
            show="tree headings",
            height=6,
        )
        self._trace_tree.heading("#0",      text="Etapa")
        self._trace_tree.heading("detalle", text="Descripción")
        self._trace_tree.column("#0",      width=100, anchor="w", stretch=False)
        self._trace_tree.column("detalle", width=700, anchor="w")
        self._trace_tree.grid(row=0, column=0, sticky="nsew")

        ts = ttk.Scrollbar(trace_frame, orient="vertical",
                           command=self._trace_tree.yview)
        ts.grid(row=0, column=1, sticky="ns")
        self._trace_tree.configure(yscrollcommand=ts.set)

    # ------------------------------------------------------------------
    # Lógica de la interfaz
    # ------------------------------------------------------------------

    def _refresh_mode_badge(self) -> None:
        mode = self._mode_var.get()
        self._mode_badge.configure(text=f"  {MODE_LABELS[mode]}  ")
        self._draw_flow(mode)

    def _draw_flow(self, mode: str) -> None:
        canvas = self._flow_canvas
        canvas.delete("all")

        width = max(canvas.winfo_width(), 760)
        height = 90
        canvas.configure(width=width, height=height)

        if mode == MODE_FORWARD:
            nodes   = [("Hechos", ACCENT), ("Reglas", "#8b5e1a"), ("Conclusión", "#3a2a0a")]
            caption = "Flujo: Hechos  →  Reglas  →  Conclusión"
        else:
            nodes   = [("Meta", ACCENT), ("Subobjetivos", "#8b5e1a"), ("Hechos", "#3a2a0a")]
            caption = "Flujo: Meta  →  Subobjetivos  →  Hechos"

        nw, gap = 180, 38
        total = len(nodes) * nw + (len(nodes) - 1) * gap
        sx = (width - total) // 2
        y1, y2 = 12, 56
        boxes = []

        for i, (label, fill) in enumerate(nodes):
            x1 = sx + i * (nw + gap)
            x2 = x1 + nw
            canvas.create_rectangle(x1, y1, x2, y2,
                fill=fill, outline=ACCENT, width=1)
            canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2,
                text=label, fill=TEXT_LIGHT,
                font=("Courier", 11, "bold"))
            boxes.append((x1, x2))

        for left, right in [(0, 1), (1, 2)]:
            canvas.create_line(
                boxes[left][1] + 6, 34,
                boxes[right][0] - 6, 34,
                fill=ACCENT, width=2, arrow="last",
                arrowshape=(10, 12, 4))

        canvas.create_text(width // 2, 75,
            text=caption, fill=TEXT_MID,
            font=("Courier", 9))

    def _load_selected_example(self) -> None:
        self._load_example(self._example_var.get())

    def _load_example(self, preset_name: str) -> None:
        from .domain import EXAMPLE_PRESETS
        preset = EXAMPLE_PRESETS[preset_name]
        for feature_name, value in preset.items():
            self._feature_vars[feature_name].set(value)

        self._refresh_mode_badge()
        self._write_result(
            f"Ejemplo cargado: {preset_name}\n\n"
            "Presiona '▶  Inferir' para ejecutar el motor de inferencia."
        )
        self._populate_trace([
            ("INFO", f"Ejemplo '{preset_name}' cargado correctamente."),
            ("INFO", "Selecciona el modo de encadenamiento y presiona Inferir."),
        ])

    def _clear(self) -> None:
        for var in self._feature_vars.values():
            var.set("")
        self._write_result("Formulario limpiado.\nSelecciona nuevas características y presiona Inferir.")
        self._populate_trace([("INFO", "Sin inferencia ejecutada todavía.")])
        self._refresh_mode_badge()

    def _infer(self) -> None:
        try:
            features = {k: v.get() for k, v in self._feature_vars.items()}
            result = self._engine.infer(features, self._mode_var.get())
        except Exception as exc:
            messagebox.showerror("Error de inferencia", str(exc))
            return

        self._write_result(format_result(result))
        self._populate_trace([
            (f"{i:02d}", step)
            for i, step in enumerate(result.trace, start=1)
        ])
        self._refresh_mode_badge()

    def _populate_trace(self, items: list[tuple[str, str]]) -> None:
        for row in self._trace_tree.get_children():
            self._trace_tree.delete(row)
        for title, detail in items:
            self._trace_tree.insert("", "end", text=title, values=(detail,))

    def _write_result(self, text: str) -> None:
        self._result_text.configure(state="normal")
        self._result_text.delete("1.0", tk.END)
        self._result_text.insert("1.0", text)
        self._result_text.configure(state="normal")


def run_app() -> None:
    app = FelidsExpertApp()
    app._refresh_mode_badge()
    app.mainloop()