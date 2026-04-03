"""Tkinter user interface for avian expert system."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .domain import (
    EXAMPLE_PRESETS,
    FEATURE_LABELS,
    FEATURE_OPTIONS,
    FEATURE_ORDER,
    RECOGNITION_MODE_BACKWARD,
    RECOGNITION_MODE_FORWARD,
    MODE_LABELS,
)
from .inference import AvianExpertSystem, format_result


class AvianExpertApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Sistema experto de identificación de aves")
        self.geometry("1280x820")
        self.minsize(1100, 720)

        self._engine = AvianExpertSystem()
        self._feature_vars: dict[str, tk.StringVar] = {}
        self._mode_var = tk.StringVar(value=RECOGNITION_MODE_FORWARD)
        self._example_var = tk.StringVar(value=next(iter(EXAMPLE_PRESETS)))

        self._build_style()
        self._build_layout()
        self._load_example(self._example_var.get())

    def _build_style(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        self.configure(bg="#0f172a")

        style.configure("App.TFrame", background="#0f172a")
        style.configure("Hero.TFrame", background="#111827")
        style.configure("Card.TFrame", background="#f8fafc")
        style.configure("CardAlt.TFrame", background="#eef2ff")
        style.configure("Accent.TFrame", background="#0ea5e9")

        style.configure(
            "HeroTitle.TLabel",
            background="#111827",
            foreground="#f8fafc",
            font=("Segoe UI", 24, "bold"),
        )
        style.configure(
            "HeroSub.TLabel",
            background="#111827",
            foreground="#cbd5e1",
            font=("Segoe UI", 11),
        )
        style.configure(
            "CardTitle.TLabel",
            background="#f8fafc",
            foreground="#0f172a",
            font=("Segoe UI", 14, "bold"),
        )
        style.configure(
            "CardText.TLabel",
            background="#f8fafc",
            foreground="#334155",
            font=("Segoe UI", 10),
        )
        style.configure(
            "AccentText.TLabel",
            background="#0ea5e9",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "SectionLabel.TLabel",
            background="#f8fafc",
            foreground="#0f172a",
            font=("Segoe UI", 11, "bold"),
        )
        style.configure(
            "Action.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 8),
        )
        style.configure(
            "Mode.TRadiobutton",
            background="#f8fafc",
            foreground="#0f172a",
            font=("Segoe UI", 10),
        )
        style.configure(
            "ModeSelected.TRadiobutton",
            background="#f8fafc",
            foreground="#0ea5e9",
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Action.TButton",
            background=[("active", "#dbeafe"), ("!active", "#e2e8f0")],
        )

    def _build_layout(self) -> None:
        root = ttk.Frame(self, style="App.TFrame", padding=18)
        root.pack(fill="both", expand=True)
        root.columnconfigure(0, weight=0)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(1, weight=1)

        hero = ttk.Frame(root, style="Hero.TFrame", padding=(24, 20))
        hero.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 16))
        hero.columnconfigure(0, weight=1)

        ttk.Label(
            hero,
            text="Sistema experto para clasificación de aves",
            style="HeroTitle.TLabel",
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            hero,
            text=(
                "Identifica especies de aves ingresando características observadas. "
                "Puedes elegir encadenamiento hacia adelante o hacia atrás para ver "
                "el proceso de inferencia con reglas taxonómicas verificables."
            ),
            style="HeroSub.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(6, 0))

        self._mode_badge = ttk.Label(hero, style="AccentText.TLabel", padding=(14, 6))
        self._mode_badge.grid(row=0, column=1, rowspan=2, sticky="e")

        left_card = ttk.Frame(root, style="Card.TFrame", padding=18)
        left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 16))
        left_card.columnconfigure(0, weight=1)

        right_area = ttk.Frame(root, style="App.TFrame")
        right_area.grid(row=1, column=1, sticky="nsew")
        right_area.rowconfigure(0, weight=3)
        right_area.rowconfigure(1, weight=2)
        right_area.columnconfigure(0, weight=1)

        result_card = ttk.Frame(right_area, style="Card.TFrame", padding=18)
        result_card.grid(row=0, column=0, sticky="nsew", pady=(0, 16))
        result_card.rowconfigure(1, weight=1)
        result_card.columnconfigure(0, weight=1)

        process_card = ttk.Frame(right_area, style="CardAlt.TFrame", padding=18)
        process_card.grid(row=1, column=0, sticky="nsew")
        process_card.rowconfigure(2, weight=1)
        process_card.columnconfigure(0, weight=1)

        self._build_left_card(left_card)
        self._build_result_card(result_card)
        self._build_process_card(process_card)

    def _build_left_card(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Configuración", style="CardTitle.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            parent,
            text="Selecciona el modo de inferencia y las características del ave.",
            style="CardText.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 14))

        mode_box = ttk.Frame(parent, style="Card.TFrame")
        mode_box.grid(row=2, column=0, sticky="ew", pady=(0, 16))
        mode_box.columnconfigure(0, weight=1)

        ttk.Label(mode_box, text="Tipo de encadenamiento", style="SectionLabel.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Radiobutton(
            mode_box,
            text=MODE_LABELS[RECOGNITION_MODE_FORWARD],
            value=RECOGNITION_MODE_FORWARD,
            variable=self._mode_var,
            style="Mode.TRadiobutton",
            command=self._refresh_mode_badge,
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Radiobutton(
            mode_box,
            text=MODE_LABELS[RECOGNITION_MODE_BACKWARD],
            value=RECOGNITION_MODE_BACKWARD,
            variable=self._mode_var,
            style="Mode.TRadiobutton",
            command=self._refresh_mode_badge,
        ).grid(row=2, column=0, sticky="w", pady=(4, 0))

        example_box = ttk.Frame(parent, style="Card.TFrame")
        example_box.grid(row=3, column=0, sticky="ew", pady=(0, 16))
        example_box.columnconfigure(0, weight=1)

        ttk.Label(example_box, text="Ejemplos", style="SectionLabel.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        example_combo = ttk.Combobox(
            example_box,
            values=list(EXAMPLE_PRESETS.keys()),
            state="readonly",
            textvariable=self._example_var,
        )
        example_combo.grid(row=1, column=0, sticky="ew", pady=(8, 8))
        ttk.Button(
            example_box,
            text="Cargar ejemplo",
            style="Action.TButton",
            command=self._load_selected_example,
        ).grid(row=2, column=0, sticky="ew")

        features_box = ttk.Frame(parent, style="Card.TFrame")
        features_box.grid(row=4, column=0, sticky="nsew")
        features_box.columnconfigure(0, weight=1)
        features_box.columnconfigure(1, weight=1)

        ttk.Label(features_box, text="Caracteristicas", style="SectionLabel.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )

        for index, feature_name in enumerate(FEATURE_ORDER):
            col = index % 2
            row = 1 + index // 2
            field = ttk.Frame(features_box, style="Card.TFrame")
            field.grid(row=row, column=col, sticky="ew", padx=(0, 10 if col == 0 else 0), pady=(0, 10))
            field.columnconfigure(0, weight=1)

            ttk.Label(field, text=FEATURE_LABELS[feature_name], style="CardText.TLabel").grid(
                row=0, column=0, sticky="w"
            )
            var = tk.StringVar()
            combo = ttk.Combobox(
                field,
                textvariable=var,
                state="readonly",
                values=FEATURE_OPTIONS[feature_name],
            )
            combo.grid(row=1, column=0, sticky="ew", pady=(4, 0))
            self._feature_vars[feature_name] = var

        action_box = ttk.Frame(parent, style="Card.TFrame")
        action_box.grid(row=5, column=0, sticky="ew", pady=(10, 0))
        action_box.columnconfigure(0, weight=1)
        action_box.columnconfigure(1, weight=1)

        ttk.Button(
            action_box,
            text="Inferir",
            style="Action.TButton",
            command=self._infer,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ttk.Button(
            action_box,
            text="Limpiar",
            style="Action.TButton",
            command=self._clear,
        ).grid(row=0, column=1, sticky="ew")

    def _build_result_card(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Resultado de clasificación", style="CardTitle.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            parent,
            text="Se muestran las especies identificadas con sus órdenes y familias taxonómicas.",
            style="CardText.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 12))

        text_frame = ttk.Frame(parent, style="Card.TFrame")
        text_frame.grid(row=2, column=0, sticky="nsew")
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        self._result_text = tk.Text(
            text_frame,
            wrap="word",
            bd=0,
            padx=16,
            pady=16,
            background="#ffffff",
            foreground="#0f172a",
            insertbackground="#0f172a",
            font=("Consolas", 11),
            relief="flat",
        )
        self._result_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self._result_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self._result_text.configure(yscrollcommand=scrollbar.set)

    def _build_process_card(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Procesamiento y reglas disparadas", style="CardTitle.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            parent,
            text="Visualiza el flujo de razonamiento y las reglas específicas que se disparan.",
            style="CardText.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 10))

        self._flow_canvas = tk.Canvas(
            parent,
            height=110,
            bg="#eef2ff",
            bd=0,
            highlightthickness=0,
        )
        self._flow_canvas.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        trace_frame = ttk.Frame(parent, style="CardAlt.TFrame")
        trace_frame.grid(row=3, column=0, sticky="nsew")
        trace_frame.columnconfigure(0, weight=1)
        trace_frame.rowconfigure(0, weight=1)

        self._trace_tree = ttk.Treeview(
            trace_frame,
            columns=("detalle",),
            show="tree headings",
            height=7,
        )
        self._trace_tree.heading("#0", text="Etapa")
        self._trace_tree.heading("detalle", text="Descripcion")
        self._trace_tree.column("#0", width=220, anchor="w")
        self._trace_tree.column("detalle", width=620, anchor="w")
        self._trace_tree.grid(row=0, column=0, sticky="nsew")

        trace_scroll = ttk.Scrollbar(trace_frame, orient="vertical", command=self._trace_tree.yview)
        trace_scroll.grid(row=0, column=1, sticky="ns")
        self._trace_tree.configure(yscrollcommand=trace_scroll.set)

    def _refresh_mode_badge(self) -> None:
        mode = self._mode_var.get()
        self._mode_badge.configure(text=MODE_LABELS[mode])
        self._draw_flow(mode)

    def _draw_flow(self, mode: str) -> None:
        canvas = self._flow_canvas
        canvas.delete("all")

        width = max(canvas.winfo_width(), 760)
        height = 110
        canvas.configure(width=width, height=height)

        if mode == RECOGNITION_MODE_FORWARD:
            nodes = [
                ("Hechos", "#0ea5e9"),
                ("Reglas", "#1d4ed8"),
                ("Conclusion", "#0f172a"),
            ]
            arrows = [(0, 1), (1, 2)]
        else:
            nodes = [
                ("Meta", "#0ea5e9"),
                ("Subobjetivos", "#1d4ed8"),
                ("Hechos", "#0f172a"),
            ]
            arrows = [(0, 1), (1, 2)]

        node_width = 180
        gap = 42
        total_width = len(nodes) * node_width + (len(nodes) - 1) * gap
        start_x = (width - total_width) // 2
        y1 = 28
        y2 = 76

        boxes = []
        for index, (label, fill) in enumerate(nodes):
            x1 = start_x + index * (node_width + gap)
            x2 = x1 + node_width
            canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=fill, width=0)
            canvas.create_text(
                (x1 + x2) // 2,
                (y1 + y2) // 2,
                text=label,
                fill="#ffffff",
                font=("Segoe UI", 11, "bold"),
            )
            boxes.append((x1, x2))

        for left, right in arrows:
            x1 = boxes[left][1]
            x2 = boxes[right][0]
            y = 52
            canvas.create_line(x1 + 10, y, x2 - 10, y, fill="#64748b", width=3, arrow="last")

        caption = (
            "Flujo de adelante: hechos -> reglas -> conclusión"
            if mode == RECOGNITION_MODE_FORWARD
            else "Flujo de atrás: meta -> subobjetivos -> hechos"
        )
        canvas.create_text(
            width // 2,
            96,
            text=caption,
            fill="#334155",
            font=("Segoe UI", 10),
        )

    def _load_selected_example(self) -> None:
        self._load_example(self._example_var.get())

    def _load_example(self, preset_name: str) -> None:
        preset = EXAMPLE_PRESETS[preset_name]
        for feature_name, value in preset.items():
            self._feature_vars[feature_name].set(value)

        self._refresh_mode_badge()
        self._write_result(
            f"Ejemplo cargado: {preset_name}\n\nPresiona 'Inferir' para ver el resultado."
        )
        self._populate_trace(
            [
                ("Preparacion", f"Se cargo el ejemplo {preset_name}."),
                (
                    "Sugerencia",
                    "Selecciona un modo de encadenamiento y presiona Inferir.",
                ),
            ]
        )

    def _clear(self) -> None:
        for var in self._feature_vars.values():
            var.set("")
        self._write_result("Formulario limpio. Selecciona nuevas caracteristicas.")
        self._populate_trace([("Estado", "Sin inferencia ejecutada todavia.")])
        self._refresh_mode_badge()

    def _infer(self) -> None:
        try:
            features = {
                feature_name: var.get()
                for feature_name, var in self._feature_vars.items()
            }
            result = self._engine.infer(features, self._mode_var.get())
        except Exception as exc:
            messagebox.showerror("Error de inferencia", str(exc))
            return

        self._write_result(format_result(result))
        self._populate_trace(
            [(f"{index:02d}", step) for index, step in enumerate(result.trace, start=1)]
        )
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
    app = AvianExpertApp()
    app._refresh_mode_badge()
    app.mainloop()
