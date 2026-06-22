import tkinter as tk
from pathlib import Path
from typing import Any, Callable


class CharacterCard:
    def __init__(
        self,
        parent: tk.Widget,
        character: str,
        sprite_path: Path,
        row: int,
        column: int,
        on_toggle_sprite: Callable[[], None] | None = None,
        crystal_jobs: dict[str, list[str]] | None = None,
        on_job_changed: Callable[[str, str, str], None] | None = None,
    ) -> None:
        self.character = character
        self.sprite_path = sprite_path
        self.on_toggle_sprite = on_toggle_sprite
        self.on_job_changed = on_job_changed
        self.crystal_jobs = crystal_jobs or {}
        self.image = self._load_image(self.sprite_path)
        self.job_labels: list[tk.Label] = []
        self.job_vars: list[tk.StringVar] = []
        self.current_assignments: dict[str, str] = {}
        self.crystals = ["Wind", "Water", "Fire", "Earth"]

        self.frame = tk.Frame(
            parent,
            bg="#18254c",
            bd=0,
            relief="flat",
            padx=12,
            pady=12,
            width=340,
            height=320,
        )
        self.frame.grid(row=row, column=column, padx=12, pady=12, sticky="nsew")
        self.frame.grid_propagate(False)
        self._build_card()

    def _build_card(self) -> None:
        sprite_container = tk.Frame(self.frame, bg="#18254c")
        sprite_container.pack(pady=(0, 10), fill="x")

        self.sprite_label = tk.Label(
            sprite_container, image=self.image, bg="#18254c"
        )
        self.sprite_label.image = self.image
        self.sprite_label.pack()

        if self.on_toggle_sprite is not None:
            self.sprite_button = tk.Button(
                sprite_container,
                text="Galuf",
                command=self.on_toggle_sprite,
                bg="#5fc5ff",
                fg="#081222",
                activebackground="#7fd4ff",
                relief="flat",
                width=5,
                height=1,
                font=("Segoe UI", 7, "bold"),
            )
            self.sprite_button.place(relx=0.0, rely=0.0, x=4, y=4)
        else:
            self.sprite_button = None

        name_label = tk.Label(
            self.frame,
            text=self.character,
            fg="#ffffff",
            bg="#18254c",
            font=("Segoe UI", 14, "bold"),
        )
        name_label.pack(pady=(0, 6))

        for crystal_index, crystal in enumerate(self.crystals):
            row_frame = tk.Frame(self.frame, bg="#1f305a")
            row_frame.pack(fill="x", pady=4)

            crystal_label = tk.Label(
                row_frame,
                text=f"{crystal}:",
                fg="#a7b8dc",
                bg="#1f305a",
                font=("Segoe UI", 9, "bold"),
                width=10,
                anchor="w",
            )
            crystal_label.pack(side="left")

            job_label = tk.Label(
                row_frame,
                text="-",
                fg="#edf2ff",
                bg="#1f305a",
                font=("Segoe UI", 10),
                anchor="w",
                width=13,
            )
            job_label.pack(side="left", fill="x", expand=True)
            # Make the label clickable
            job_label.bind("<Button-1>", lambda event, idx=crystal_index: self._on_job_clicked(idx))
            job_label.config(cursor="hand2")
            self.job_labels.append(job_label)

            # Add dropdown menu for job selection
            available_jobs = self.crystal_jobs.get(crystal, ["-"])
            job_var = tk.StringVar(value="-")
            self.job_vars.append(job_var)

            # Create a menu for the dropdown
            menu = tk.Menu(
                row_frame,
                tearoff=0,
                bg="#152246",
                fg="#edf2ff",
                activebackground="#2f3c6b",
                activeforeground="#edf2ff",
                font=("Segoe UI", 9),
            )
            for job in available_jobs:
                menu.add_command(
                    label=job,
                    command=lambda selected=job, idx=crystal_index: self._on_dropdown_changed(idx, selected),
                )

            # Create dropdown button that shows just a small arrow
            dropdown_button = tk.Button(
                row_frame,
                text="▼",
                command=lambda m=menu, btn=None: self._show_menu(m, btn),
                bg="#2f3c6b",
                fg="#a7b8dc",
                activebackground="#3f4c7b",
                activeforeground="#edf2ff",
                highlightthickness=0,
                relief="flat",
                font=("Segoe UI", 8),
                width=2,
                height=1,
                padx=2,
                pady=0,
            )
            dropdown_button.pack(side="right", padx=(4, 0))
            dropdown_button.menu = menu


    def _load_image(self, path: Path) -> tk.PhotoImage:
        if not path.exists():
            raise FileNotFoundError(f"Sprite not found: {path}")
        image = tk.PhotoImage(file=str(path))
        return image

    def _show_menu(self, menu: tk.Menu, button: tk.Button | None) -> None:
        """Display the dropdown menu."""
        menu.post(menu.winfo_pointerx(), menu.winfo_pointery() - 5)

    def update_jobs(self, assignments: dict[str, str]) -> None:
        self.current_assignments = assignments.copy()
        for label, job_var, job in zip(self.job_labels, self.job_vars, assignments.values()):
            label.config(text=job)
            job_var.set(job)

    def _on_job_clicked(self, crystal_index: int) -> None:
        """Handle job label clicks to cycle through available jobs."""
        crystal = self.crystals[crystal_index]
        available_jobs = self.crystal_jobs.get(crystal, [])
        
        if not available_jobs:
            return
        
        current_job = self.current_assignments.get(crystal, "-")
        
        # Find the next job in the list
        if current_job in available_jobs:
            current_idx = available_jobs.index(current_job)
            next_idx = (current_idx + 1) % len(available_jobs)
        else:
            next_idx = 0
        
        new_job = available_jobs[next_idx]
        
        # Update the label
        self.job_labels[crystal_index].config(text=new_job)
        self.current_assignments[crystal] = new_job
        
        # Update the dropdown
        self.job_vars[crystal_index].set(new_job)
        
        # Notify the main app if callback is provided
        if self.on_job_changed:
            self.on_job_changed(self.character, crystal, new_job)

    def _on_dropdown_changed(self, crystal_index: int, selected_job: str) -> None:
        """Handle dropdown selection changes."""
        crystal = self.crystals[crystal_index]
        
        # Update the label
        self.job_labels[crystal_index].config(text=selected_job)
        self.current_assignments[crystal] = selected_job
        
        # Notify the main app if callback is provided
        if self.on_job_changed:
            self.on_job_changed(self.character, crystal, selected_job)

    def update_sprite(self, path: Path, button_text: str) -> None:
        self.image = self._load_image(path)
        self.sprite_label.configure(image=self.image)
        self.sprite_label.image = self.image
        if self.sprite_button is not None:
            self.sprite_button.configure(text=button_text)
