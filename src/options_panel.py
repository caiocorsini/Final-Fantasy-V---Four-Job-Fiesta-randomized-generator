import tkinter as tk

from .constants import CRYSTALS


class OptionsPanel:
    def __init__(self, parent: tk.Widget) -> None:
        self.options_open = False
        self.deep_customization_open = False
        self.base_width = 260
        self.wide_width = 420
        self.exclude_berserker_var = tk.BooleanVar(value=False)
        self.allow_same_crystal_job_var = tk.BooleanVar(value=False)
        self.include_previous_crystals_var = tk.BooleanVar(value=False)
        self.job_inclusion_vars: dict[str, tk.BooleanVar] = {}
        self.deep_customization_frame: tk.Frame | None = None
        self.deep_customization_container: tk.Frame | None = None

        self.frame = tk.Frame(parent, bg="#121b35", bd=1, relief="solid")
        self.frame.place_forget()
        self._build_panel()

        self.exclude_berserker_var.trace_add(
            "write", self._sync_berserker_selection
        )

    def _build_panel(self) -> None:
        title = tk.Label(
            self.frame,
            text="Options",
            fg="#edf2ff",
            bg="#121b35",
            font=("Segoe UI", 12, "bold"),
        )
        title.pack(padx=12, pady=(12, 6), anchor="w")

        self._build_checkbutton("Exclude Berserker", self.exclude_berserker_var)
        self._build_checkbutton(
            "Allow same job in same crystal", self.allow_same_crystal_job_var
        )
        self._build_checkbutton(
            "Include previous crystal jobs", self.include_previous_crystals_var
        )

        deep_button = tk.Button(
            self.frame,
            text="Deep Customization",
            command=self.toggle_deep_customization,
            bg="#2f3c6b",
            fg="#edf2ff",
            activebackground="#3f4c7b",
            relief="flat",
            padx=10,
            pady=6,
            font=("Segoe UI", 10, "bold"),
        )
        deep_button.pack(fill="x", padx=12, pady=(8, 4))

        self._build_deep_customization_panel()

        close_button = tk.Button(
            self.frame,
            text="Close",
            command=self.toggle,
            bg="#5fc5ff",
            fg="#081222",
            relief="flat",
            padx=10,
            pady=6,
            font=("Segoe UI", 10, "bold"),
        )
        close_button.pack(padx=12, pady=(10, 12), anchor="e")

    def _build_deep_customization_panel(self) -> None:
        self.deep_customization_container = tk.Frame(
            self.frame,
            bg="#101a2d",
        )

        self.deep_customization_canvas = tk.Canvas(
            self.deep_customization_container,
            bg="#101a2d",
            highlightthickness=0,
            height=260,
        )
        self.deep_customization_scrollbar = tk.Scrollbar(
            self.deep_customization_container,
            orient="vertical",
            command=self.deep_customization_canvas.yview,
        )
        self.deep_customization_canvas.configure(yscrollcommand=self.deep_customization_scrollbar.set)

        self.deep_customization_frame = tk.Frame(
            self.deep_customization_canvas,
            bg="#101a2d",
        )

        self.deep_customization_canvas.create_window(
            (0, 0), window=self.deep_customization_frame, anchor="nw"
        )
        self.deep_customization_frame.bind(
            "<Configure>", self._on_deep_customization_configure
        )

        self.deep_customization_canvas.pack(side="left", fill="both", expand=True)
        self.deep_customization_scrollbar.pack(side="right", fill="y")

        title = tk.Label(
            self.deep_customization_frame,
            text="Select jobs to include in randomization",
            fg="#edf2ff",
            bg="#101a2d",
            font=("Segoe UI", 10, "bold"),
        )
        title.pack(fill="x", padx=12, pady=(10, 6), anchor="w")

        for crystal, jobs in CRYSTALS.items():
            crystal_label = tk.Label(
                self.deep_customization_frame,
                text=crystal,
                fg="#a8b5d4",
                bg="#101a2d",
                font=("Segoe UI", 9, "bold"),
            )
            crystal_label.pack(fill="x", padx=12, pady=(8, 2), anchor="w")

            jobs_frame = tk.Frame(self.deep_customization_frame, bg="#101a2d")
            jobs_frame.pack(fill="x", padx=12)

            for job in jobs:
                selected = True
                if job == "Berserker" and self.exclude_berserker_var.get():
                    selected = False

                job_var = tk.BooleanVar(value=selected)
                self.job_inclusion_vars[job] = job_var
                if job == "Berserker":
                    job_var.trace_add("write", self._sync_berserker_checkbox)
                self._build_checkbutton(job, job_var, parent=jobs_frame)

        self.deep_customization_container.pack_forget()

    def _sync_berserker_checkbox(self, *_args: object) -> None:
        berserker_var = self.job_inclusion_vars.get("Berserker")
        if berserker_var is not None:
            self.exclude_berserker_var.set(not berserker_var.get())

    def toggle_deep_customization(self) -> None:
        if self.deep_customization_open:
            self.deep_customization_container.pack_forget()
            self.deep_customization_open = False
            self._update_panel_width(False)
            return

        self.deep_customization_container.pack(fill="both", padx=12, pady=(0, 4), expand=True)
        self.deep_customization_open = True
        self._update_panel_width(True)

    def _sync_berserker_selection(self, *_args: object) -> None:
        berserker_var = self.job_inclusion_vars.get("Berserker")
        if berserker_var is not None:
            berserker_var.set(not self.exclude_berserker_var.get())

    def _on_deep_customization_configure(self, event: tk.Event) -> None:
        self.deep_customization_canvas.configure(
            scrollregion=self.deep_customization_canvas.bbox("all")
        )

    def _update_panel_width(self, wide: bool) -> None:
        width = self.wide_width if wide else self.base_width
        self.frame.place_configure(width=width)

    def _build_checkbutton(
        self,
        label: str,
        variable: tk.BooleanVar,
        parent: tk.Widget | None = None,
    ) -> None:
        if parent is None:
            parent = self.frame

        check = tk.Checkbutton(
            parent,
            text=label,
            variable=variable,
            fg="#edf2ff",
            bg="#101a2d" if parent is self.deep_customization_frame else "#121b35",
            selectcolor="#121b35",
            activebackground="#121b35",
            activeforeground="#edf2ff",
            font=("Segoe UI", 10),
            bd=0,
            highlightthickness=0,
            anchor="w",
        )
        if parent is self.frame:
            check.pack(fill="x", padx=0, pady=2)
        else:
            check.pack(fill="x", side="left", padx=0, pady=2)

    def toggle(self) -> None:
        if self.options_open:
            self.frame.place_forget()
            self.options_open = False
            return

        self.frame.place(relx=1.0, rely=0.0, x=-16, y=56, anchor="ne", width=260)
        self.options_open = True

    def get_settings(self) -> tuple[bool, bool, bool, set[str]]:
        return (
            self.exclude_berserker_var.get(),
            self.allow_same_crystal_job_var.get(),
            self.include_previous_crystals_var.get(),
            self.get_selected_jobs(),
        )

    def get_selected_jobs(self) -> set[str]:
        return {
            job for job, var in self.job_inclusion_vars.items() if var.get()
        }

    def set_selected_jobs(self, selected_jobs: list[str]) -> None:
        for job, var in self.job_inclusion_vars.items():
            var.set(job in selected_jobs)

        if "Berserker" in self.job_inclusion_vars:
            self.exclude_berserker_var.set(
                not self.job_inclusion_vars["Berserker"].get()
            )
