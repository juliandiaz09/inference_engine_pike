# -*- coding: utf-8 -*-
"""Tkinter user interface for avian expert system."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from .domain import (
    EXAMPLE_PRESETS,
    FEATURE_LABELS,
    FEATURE_OPTIONS,
    FEATURE_GROUPS,
    FEATURE_ORDER,
    RECOGNITION_MODE_BACKWARD,
    RECOGNITION_MODE_FORWARD,
    MODE_LABELS,
    FEATURE_DISPLAY_OPTIONS,
    FEATURE_DISPLAY_TO_VALUE,
    humanize_label,
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

        # Colores alternos para el treeview de trazas
        style.configure(
            "Trace.Treeview",
            background="#eef2ff",
            fieldbackground="#eef2ff",
            foreground="#1e293b",
            font=("Segoe UI", 10),
            rowheight=26,
        )
        style.configure(
            "Trace.Treeview.Heading",
            background="#1d4ed8",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
        )
        style.map(
            "Trace.Treeview",
            background=[("selected", "#bfdbfe")],
            foreground=[("selected", "#0f172a")],
        )

    def _build_layout(self) -> None:
        main_container = ttk.Frame(self, style="App.TFrame")
        main_container.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(main_container, bg="#0f172a", highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        root = ttk.Frame(canvas, style="App.TFrame", padding=18)
        canvas.create_window((0, 0), window=root, anchor="nw", width=canvas.winfo_width())

        root.columnconfigure(0, weight=0)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(1, weight=1)

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_canvas_configure(event):
            canvas.itemconfig(1, width=event.width)

        root.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_configure)

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

        ttk.Label(features_box, text="Características", style="SectionLabel.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )

        row_index = 1
        for group_name, group_features in FEATURE_GROUPS.items():
            group_card = ttk.Frame(features_box, style="Card.TFrame")
            group_card.grid(row=row_index, column=0, columnspan=2, sticky="ew", pady=(0, 12))
            group_card.columnconfigure(0, weight=1)
            ttk.Label(
                group_card,
                text=humanize_label(group_name),
                style="SectionLabel.TLabel",
            ).grid(row=0, column=0, sticky="w", pady=(0, 8))

            inner = ttk.Frame(group_card, style="Card.TFrame")
            inner.grid(row=1, column=0, sticky="ew")
            inner.columnconfigure(0, weight=1)
            inner.columnconfigure(1, weight=1)

            for index, feature_name in enumerate(group_features):
                col = index % 2
                field = ttk.Frame(inner, style="Card.TFrame")
                field.grid(row=0, column=col, sticky="ew", padx=(0, 10 if col == 0 else 0))
                field.columnconfigure(0, weight=1)

                ttk.Label(
                    field,
                    text=FEATURE_LABELS.get(feature_name, humanize_label(feature_name)),
                    style="CardText.TLabel",
                ).grid(row=0, column=0, sticky="w")
                var = tk.StringVar()
                combo = ttk.Combobox(
                    field,
                    textvariable=var,
                    state="readonly",
                    values=FEATURE_DISPLAY_OPTIONS[feature_name],
                )
                combo.grid(row=1, column=0, sticky="ew", pady=(4, 0))
                self._feature_vars[feature_name] = var

            row_index += 1

        action_box = ttk.Frame(parent, style="Card.TFrame")
        action_box.grid(row=5, column=0, sticky="ew", pady=(10, 0))
        action_box.columnconfigure(0, weight=1)
        action_box.columnconfigure(1, weight=1)

        ttk.Button(action_box, text="Inferir", style="Action.TButton", command=self._infer).grid(
            row=0, column=0, sticky="ew", padx=(0, 8)
        )
        ttk.Button(action_box, text="Limpiar", style="Action.TButton", command=self._clear).grid(
            row=0, column=1, sticky="ew"
        )

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
            background="#0f172a",
            foreground="#e2e8f0",
            insertbackground="#e2e8f0",
            font=("Consolas", 11),
            relief="flat",
        )
        self._result_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self._result_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self._result_text.configure(yscrollcommand=scrollbar.set)

        # ── Tags de formato para el panel de resultados ──────────────────────
        self._result_text.tag_configure(
            "title",
            foreground="#38bdf8",
            font=("Segoe UI", 13, "bold"),
            spacing1=6,
            spacing3=4,
        )
        self._result_text.tag_configure(
            "separator",
            foreground="#334155",
            font=("Consolas", 10),
            spacing1=2,
            spacing3=2,
        )
        self._result_text.tag_configure(
            "mode_label",
            foreground="#94a3b8",
            font=("Segoe UI", 10),
        )
        self._result_text.tag_configure(
            "section_header",
            foreground="#fbbf24",
            font=("Segoe UI", 11, "bold"),
            spacing1=8,
            spacing3=4,
        )
        self._result_text.tag_configure(
            "feature_key",
            foreground="#7dd3fc",
            font=("Consolas", 11),
        )
        self._result_text.tag_configure(
            "feature_value",
            foreground="#e2e8f0",
            font=("Consolas", 11),
        )
        self._result_text.tag_configure(
            "success",
            foreground="#4ade80",
            font=("Segoe UI", 11, "bold"),
            spacing1=6,
        )
        self._result_text.tag_configure(
            "warning",
            foreground="#fbbf24",
            font=("Segoe UI", 11, "bold"),
            spacing1=6,
        )
        self._result_text.tag_configure(
            "error",
            foreground="#f87171",
            font=("Segoe UI", 11, "bold"),
            spacing1=6,
        )
        self._result_text.tag_configure(
            "species_name",
            foreground="#a78bfa",
            font=("Segoe UI", 12, "bold"),
            spacing1=4,
        )
        self._result_text.tag_configure(
            "field_label",
            foreground="#94a3b8",
            font=("Consolas", 11),
        )
        self._result_text.tag_configure(
            "field_value",
            foreground="#e2e8f0",
            font=("Consolas", 11, "bold"),
        )
        self._result_text.tag_configure(
            "score_high",
            foreground="#4ade80",
            font=("Consolas", 11, "bold"),
        )
        self._result_text.tag_configure(
            "score_med",
            foreground="#fbbf24",
            font=("Consolas", 11, "bold"),
        )
        self._result_text.tag_configure(
            "score_low",
            foreground="#f87171",
            font=("Consolas", 11, "bold"),
        )
        self._result_text.tag_configure(
            "body",
            foreground="#cbd5e1",
            font=("Consolas", 11),
        )

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
            style="Trace.Treeview",
        )
        self._trace_tree.heading("#0", text="Etapa")
        self._trace_tree.heading("detalle", text="Descripción")
        self._trace_tree.column("#0", width=220, anchor="w")
        self._trace_tree.column("detalle", width=620, anchor="w")
        self._trace_tree.grid(row=0, column=0, sticky="nsew")

        # Tags para filas alternas en el treeview
        self._trace_tree.tag_configure("odd", background="#dbeafe", foreground="#1e293b")
        self._trace_tree.tag_configure("even", background="#eef2ff", foreground="#1e293b")
        self._trace_tree.tag_configure("fact", background="#dcfce7", foreground="#166534")
        self._trace_tree.tag_configure("rule", background="#fef9c3", foreground="#92400e")
        self._trace_tree.tag_configure("result", background="#ede9fe", foreground="#4c1d95")
        self._trace_tree.tag_configure("error_row", background="#fee2e2", foreground="#991b1b")

        trace_scroll = ttk.Scrollbar(
            trace_frame, orient="vertical", command=self._trace_tree.yview
        )
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
                ("Conclusión", "#0f172a"),
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
            "Flujo hacia adelante: hechos → reglas → conclusión"
            if mode == RECOGNITION_MODE_FORWARD
            else "Flujo hacia atrás: meta → subobjetivos → hechos"
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
        for feature_name in FEATURE_ORDER:
            value = preset.get(feature_name, FEATURE_OPTIONS[feature_name][0])
            self._feature_vars[feature_name].set(humanize_label(value))

        self._refresh_mode_badge()
        self._write_result(
            f"Ejemplo cargado: {preset_name}\n\nPresiona 'Inferir' para ver el resultado."
        )
        self._populate_trace(
            [
                ("Preparación", f"Se cargó el ejemplo {preset_name}."),
                (
                    "Sugerencia",
                    "Selecciona un modo de inferencia y presiona Inferir.",
                ),
            ]
        )

    def _clear(self) -> None:
        for var in self._feature_vars.values():
            var.set("")
        self._write_result("Formulario limpio. Selecciona nuevas características.")
        self._populate_trace([("Estado", "Sin inferencia ejecutada todavía.")])
        self._refresh_mode_badge()

    def _infer(self) -> None:
        try:
            features = {
                feature_name: FEATURE_DISPLAY_TO_VALUE[feature_name].get(
                    var.get(),
                    var.get().replace(" ", "_").lower(),
                )
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

        for idx, (title, detail) in enumerate(items):
            # Elegir tag según contenido de la descripción
            text_lower = detail.lower()
            if any(k in text_lower for k in ("hecho registrado", "agregando", "hecho")):
                row_tag = "fact"
            elif any(k in text_lower for k in ("regla disparada", "clasificar", "rule")):
                row_tag = "rule"
            elif any(k in text_lower for k in ("resultado", "especie", "conclusión", "meta demostrada")):
                row_tag = "result"
            elif any(k in text_lower for k in ("error", "no se pudo", "no coincide")):
                row_tag = "error_row"
            else:
                row_tag = "odd" if idx % 2 == 0 else "even"

            self._trace_tree.insert("", "end", text=title, values=(detail,), tags=(row_tag,))

    def _write_result(self, text: str) -> None:
        """Write formatted result text with syntax highlighting."""
        self._result_text.configure(state="normal")
        self._result_text.delete("1.0", tk.END)

        for line in text.splitlines():
            stripped = line.rstrip()

            # Separadores de igual o guión
            if set(stripped.replace(" ", "")) <= {"=", "═"} and len(stripped) > 4:
                self._result_text.insert(tk.END, stripped + "\n", "separator")

            elif set(stripped.replace(" ", "")) <= {"-", "─"} and len(stripped) > 4:
                self._result_text.insert(tk.END, stripped + "\n", "separator")

            # Cabeceras principales (todo mayúsculas, sin prefijo especial)
            elif stripped.isupper() and len(stripped) > 3 and not stripped.startswith("  "):
                self._result_text.insert(tk.END, stripped + "\n", "title")

            # Línea de modo
            elif stripped.startswith("Modo:"):
                self._result_text.insert(tk.END, stripped + "\n", "mode_label")

            # Características ingresadas (encabezado)
            elif stripped.startswith("Características ingresadas"):
                self._result_text.insert(tk.END, stripped + "\n", "section_header")

            # Ítem de característica:  "  • Clave: Valor"
            elif stripped.startswith("•"):
                parts = stripped[1:].split(":", 1)
                if len(parts) == 2:
                    self._result_text.insert(tk.END, "  • ", "separator")
                    self._result_text.insert(tk.END, parts[0].strip(), "feature_key")
                    self._result_text.insert(tk.END, ": ", "separator")
                    self._result_text.insert(tk.END, parts[1].strip() + "\n", "feature_value")
                else:
                    self._result_text.insert(tk.END, stripped + "\n", "body")

            # Resultado exitoso
            elif stripped.startswith("✓"):
                self._result_text.insert(tk.END, stripped + "\n", "success")

            # Advertencia / posibles aves
            elif stripped.startswith("≈"):
                self._result_text.insert(tk.END, stripped + "\n", "warning")

            # Error / no encontrado
            elif stripped.startswith("✗"):
                self._result_text.insert(tk.END, stripped + "\n", "error")

            # Nombre de especie
            elif stripped.startswith("Especie:"):
                label, _, value = stripped.partition(":")
                self._result_text.insert(tk.END, "  " + label + ": ", "field_label")
                self._result_text.insert(tk.END, value.strip() + "\n", "species_name")

            # Coincidencia con color según porcentaje
            elif stripped.startswith("Coincidencia:"):
                label, _, value = stripped.partition(":")
                pct_str = value.strip().replace("%", "")
                try:
                    pct = int(pct_str)
                except ValueError:
                    pct = 0
                score_tag = (
                    "score_high" if pct >= 80
                    else "score_med" if pct >= 50
                    else "score_low"
                )
                self._result_text.insert(tk.END, "  " + label + ": ", "field_label")
                self._result_text.insert(tk.END, value.strip() + "\n", score_tag)

            # Orden / Familia / Clase
            elif stripped.startswith(("Orden:", "Familia:", "Clase:")):
                label, _, value = stripped.partition(":")
                self._result_text.insert(tk.END, "  " + label + ": ", "field_label")
                self._result_text.insert(tk.END, value.strip() + "\n", "field_value")

            # Línea vacía
            elif stripped == "":
                self._result_text.insert(tk.END, "\n")

            # Todo lo demás
            else:
                self._result_text.insert(tk.END, stripped + "\n", "body")

        self._result_text.configure(state="disabled")


def run_app() -> None:
    app = AvianExpertApp()
    app._refresh_mode_badge()
    app.mainloop()