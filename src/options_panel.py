import tkinter as tk


class OptionsPanel:
    def __init__(self, parent: tk.Widget) -> None:
        self.options_open = False
        self.exclude_berserker_var = tk.BooleanVar(value=False)
        self.allow_same_crystal_job_var = tk.BooleanVar(value=False)
        self.include_previous_crystals_var = tk.BooleanVar(value=False)

        self.frame = tk.Frame(parent, bg="#121b35", bd=1, relief="solid")
        self.frame.place_forget()
        self._build_panel()

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

    def _build_checkbutton(self, label: str, variable: tk.BooleanVar) -> None:
        check = tk.Checkbutton(
            self.frame,
            text=label,
            variable=variable,
            fg="#edf2ff",
            bg="#121b35",
            selectcolor="#121b35",
            activebackground="#121b35",
            activeforeground="#edf2ff",
            font=("Segoe UI", 10),
            bd=0,
            highlightthickness=0,
            anchor="w",
        )
        check.pack(fill="x", padx=12, pady=4)

    def toggle(self) -> None:
        if self.options_open:
            self.frame.place_forget()
            self.options_open = False
            return

        self.frame.place(relx=1.0, rely=0.0, x=-16, y=56, anchor="ne", width=260)
        self.options_open = True

    def get_settings(self) -> tuple[bool, bool, bool]:
        return (
            self.exclude_berserker_var.get(),
            self.allow_same_crystal_job_var.get(),
            self.include_previous_crystals_var.get(),
        )
