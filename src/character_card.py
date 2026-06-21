import tkinter as tk
from pathlib import Path
from typing import Callable


class CharacterCard:
    def __init__(
        self,
        parent: tk.Widget,
        character: str,
        sprite_path: Path,
        row: int,
        column: int,
        on_toggle_sprite: Callable[[], None] | None = None,
    ) -> None:
        self.character = character
        self.sprite_path = sprite_path
        self.on_toggle_sprite = on_toggle_sprite
        self.image = self._load_image(self.sprite_path)
        self.job_labels: list[tk.Label] = []

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

        for crystal in ["Wind", "Water", "Fire", "Earth"]:
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
            self.job_labels.append(job_label)

    def _load_image(self, path: Path) -> tk.PhotoImage:
        if not path.exists():
            raise FileNotFoundError(f"Sprite not found: {path}")
        image = tk.PhotoImage(file=str(path))
        return image

    def update_jobs(self, assignments: dict[str, str]) -> None:
        for label, job in zip(self.job_labels, assignments.values()):
            label.config(text=job)

    def update_sprite(self, path: Path, button_text: str) -> None:
        self.image = self._load_image(path)
        self.sprite_label.configure(image=self.image)
        self.sprite_label.image = self.image
        if self.sprite_button is not None:
            self.sprite_button.configure(text=button_text)
