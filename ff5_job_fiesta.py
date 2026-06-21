import random
import sys
import tkinter as tk
from pathlib import Path
from typing import Any

CRYSTALS = {
    "Wind": ["Knight", "Monk", "Thief", "White Mage", "Black Mage", "Blue Mage"],
    "Water": ["Berserker", "Mystic Knight", "Time Mage", "Summoner", "Red Mage"],
    "Fire": ["Geomancer", "Beastmaster", "Ninja", "Bard", "Ranger"],
    "Earth": ["Samurai", "Dancer", "Dragoon", "Chemist"],
}
CHARACTERS = ["Bartz", "Lenna", "Faris", "Galuf/Krile"]
SPRITES = {
    "Bartz": "Assets/Bartz_feelancer.png",
    "Lenna": "Assets/Lenna_freelancer.png",
    "Faris": "Assets/Faris_freelancer.png",
    "Galuf/Krile": "Assets/Galuf_freelancer.png",
}


def randomize_jobs(
    seed: int | None = None,
    exclude_berserker: bool = False,
    allow_same_crystal_job: bool = False,
) -> dict:
    if seed is not None:
        random.seed(seed)

    result = {character: {} for character in CHARACTERS}
    for crystal, jobs in CRYSTALS.items():
        available_jobs = [job for job in jobs if not (exclude_berserker and job == "Berserker")]
        if allow_same_crystal_job:
            assignments = [random.choice(available_jobs) for _ in CHARACTERS]
        else:
            assignments = random.sample(available_jobs, k=4)

        for character, job in zip(CHARACTERS, assignments):
            result[character][crystal] = job
    return result


class FF5JobFiestaApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("FF5 4 Job Fiesta Randomizer")
        self.configure(bg="#0f162c")
        self.resizable(False, False)

        self.images: dict[str, tk.PhotoImage] = {}
        self.job_labels: dict[str, list[tk.Label]] = {}

        self._build_header()
        self._build_character_grid()
        self._build_footer()
        self.randomize_and_update()

    def _build_header(self) -> None:
        header_frame = tk.Frame(self, bg="#0f162c")
        header_frame.pack(padx=16, pady=(16, 8), fill="x")

        title = tk.Label(
            header_frame,
            text="Final Fantasy V 4 Job Fiesta",
            fg="#edf2ff",
            bg="#0f162c",
            font=("Segoe UI", 20, "bold"),
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            header_frame,
            text="Randomize one job from each crystal for Bartz, Lenna, Faris and Galuf/Krile.",
            fg="#bbc8ea",
            bg="#0f162c",
            font=("Segoe UI", 10),
        )
        subtitle.pack(anchor="w", pady=(4, 0))

    def _build_character_grid(self) -> None:
        grid_frame = tk.Frame(self, bg="#0f162c")
        grid_frame.pack(padx=16, pady=8)

        for index, character in enumerate(CHARACTERS):
            card = tk.Frame(
                grid_frame,
                bg="#18254c",
                bd=0,
                relief="flat",
                padx=12,
                pady=12,
                width=340,
                height=320,
            )
            card.grid(row=index // 2, column=index % 2, padx=12, pady=12, sticky="nsew")
            card.grid_propagate(False)

            sprite = self._load_character_image(character)
            sprite_label = tk.Label(card, image=sprite, bg="#18254c")
            sprite_label.image = sprite
            sprite_label.pack(pady=(0, 10))

            name_label = tk.Label(
                card,
                text=character,
                fg="#ffffff",
                bg="#18254c",
                font=("Segoe UI", 14, "bold"),
            )
            name_label.pack(pady=(0, 6))

            job_rows: list[tk.Label] = []
            for crystal in CRYSTALS:
                row = tk.Frame(card, bg="#1f305a")
                row.pack(fill="x", pady=4)

                crystal_label = tk.Label(
                    row,
                    text=f"{crystal}:",
                    fg="#a7b8dc",
                    bg="#1f305a",
                    font=("Segoe UI", 9, "bold"),
                    width=10,
                    anchor="w",
                )
                crystal_label.pack(side="left")

                job_label = tk.Label(
                    row,
                    text="-",
                    fg="#edf2ff",
                    bg="#1f305a",
                    font=("Segoe UI", 10),
                    anchor="w",
                    width=13,
                )
                job_label.pack(side="left", fill="x", expand=True)
                job_rows.append(job_label)

            self.job_labels[character] = job_rows

    def _build_footer(self) -> None:
        footer = tk.Frame(self, bg="#0f162c")
        footer.pack(padx=16, pady=(0, 16), fill="x")

        self.seed_var = tk.StringVar()
        seed_entry = tk.Entry(
            footer,
            textvariable=self.seed_var,
            width=16,
            font=("Segoe UI", 10),
            fg="#edf2ff",
            bg="#152246",
            insertbackground="#edf2ff",
            relief="flat",
        )
        seed_entry.pack(side="left", padx=(0, 10))
        seed_entry.insert(0, "Seed (optional)")
        seed_entry.bind("<FocusIn>", self._clear_seed_placeholder)

        options_button = tk.Button(
            footer,
            text="Options",
            command=self.toggle_options_menu,
            bg="#2f3c6b",
            fg="#edf2ff",
            activebackground="#3f4c7b",
            relief="flat",
            padx=10,
            pady=8,
            font=("Segoe UI", 10, "bold"),
        )
        options_button.pack(side="left", padx=(0, 14))

        randomize_button = tk.Button(
            footer,
            text="Randomize Jobs",
            command=self.randomize_and_update,
            bg="#5fc5ff",
            fg="#081222",
            activebackground="#7fd4ff",
            relief="flat",
            padx=12,
            pady=8,
            font=("Segoe UI", 10, "bold"),
        )
        randomize_button.pack(side="left")

        self._build_options_menu()

    def _clear_seed_placeholder(self, event: Any) -> None:
        if self.seed_var.get() == "Seed (optional)":
            self.seed_var.set("")

    def _build_options_menu(self) -> None:
        self.options_open = False
        self.exclude_berserker_var = tk.BooleanVar(value=False)
        self.allow_same_crystal_job_var = tk.BooleanVar(value=False)

        self.options_frame = tk.Frame(self, bg="#121b35", bd=1, relief="solid")
        self.options_frame.place_forget()

        title = tk.Label(
            self.options_frame,
            text="Options",
            fg="#edf2ff",
            bg="#121b35",
            font=("Segoe UI", 12, "bold"),
        )
        title.pack(padx=12, pady=(12, 6), anchor="w")

        berserker_check = tk.Checkbutton(
            self.options_frame,
            text="Exclude Berserker",
            variable=self.exclude_berserker_var,
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
        berserker_check.pack(fill="x", padx=12, pady=4)

        duplicate_check = tk.Checkbutton(
            self.options_frame,
            text="Allow same job in same crystal",
            variable=self.allow_same_crystal_job_var,
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
        duplicate_check.pack(fill="x", padx=12, pady=4)

        close_button = tk.Button(
            self.options_frame,
            text="Close",
            command=self.toggle_options_menu,
            bg="#5fc5ff",
            fg="#081222",
            relief="flat",
            padx=10,
            pady=6,
            font=("Segoe UI", 10, "bold"),
        )
        close_button.pack(padx=12, pady=(10, 12), anchor="e")

    def toggle_options_menu(self) -> None:
        if self.options_open:
            self.options_frame.place_forget()
            self.options_open = False
            return

        self.options_frame.place(relx=1.0, rely=0.0, x=-16, y=56, anchor="ne", width=260)
        self.options_open = True

    def _load_character_image(self, character: str) -> tk.PhotoImage:
        path = Path(__file__).parent / SPRITES[character]
        if not path.exists():
            raise FileNotFoundError(f"Sprite not found: {path}")
        image = tk.PhotoImage(file=str(path))
        self.images[character] = image
        return image

    def randomize_and_update(self) -> None:
        seed = None
        seed_text = self.seed_var.get()
        if seed_text and seed_text != "Seed (optional)":
            try:
                seed = int(seed_text)
            except ValueError:
                seed = None

        exclude_berserker = self.exclude_berserker_var.get()
        allow_same_crystal_job = self.allow_same_crystal_job_var.get()
        assignments = randomize_jobs(
            seed,
            exclude_berserker=exclude_berserker,
            allow_same_crystal_job=allow_same_crystal_job,
        )
        for character, labels in self.job_labels.items():
            for label, crystal in zip(labels, CRYSTALS):
                label.config(text=assignments[character][crystal])


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] in {"console", "print"}:
        assignments = randomize_jobs()
        for character, crystals in assignments.items():
            print(f"\n{character}:")
            for crystal, job in crystals.items():
                print(f"  {crystal}: {job}")
        return

    app = FF5JobFiestaApp()
    app.mainloop()


if __name__ == "__main__":
    main()
