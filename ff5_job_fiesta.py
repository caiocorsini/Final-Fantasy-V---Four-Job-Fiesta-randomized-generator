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


class JobRandomizer:
    def __init__(self, crystals: dict[str, list[str]], characters: list[str]) -> None:
        self.crystals = crystals
        self.characters = characters

    def randomize(
        self,
        seed: int | None = None,
        exclude_berserker: bool = False,
        allow_same_crystal_job: bool = False,
        include_previous_crystals: bool = False,
    ) -> dict:
        if seed is not None:
            random.seed(seed)

        result = {character: {} for character in self.characters}
        crystal_names = list(self.crystals.keys())

        for crystal_index, crystal in enumerate(crystal_names):
            jobs = self.crystals[crystal]
            if include_previous_crystals and crystal_index > 0:
                previous_jobs = [
                    job
                    for previous_crystal in crystal_names[:crystal_index]
                    for job in self.crystals[previous_crystal]
                ]
                jobs = previous_jobs + jobs

            available_jobs = [
                job for job in jobs if not (exclude_berserker and job == "Berserker")
            ]
            if allow_same_crystal_job:
                assignments = [random.choice(available_jobs) for _ in self.characters]
            else:
                assignments = random.sample(available_jobs, k=len(self.characters))

            for character, job in zip(self.characters, assignments):
                result[character][crystal] = job

        return result


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

        self._build_checkbutton(
            "Exclude Berserker", self.exclude_berserker_var
        )
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

    def _build_checkbutton(
        self, label: str, variable: tk.BooleanVar
    ) -> None:
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


class CharacterCard:
    def __init__(
        self,
        parent: tk.Widget,
        character: str,
        sprite_path: str,
        row: int,
        column: int,
        on_toggle_sprite: None | callable = None,
    ) -> None:
        self.character = character
        self.sprite_path = Path(__file__).parent / sprite_path
        self.on_toggle_sprite = on_toggle_sprite
        self.image = self._load_image(self.sprite_path)
        self.job_labels: list[tk.Label] = []
        self.sprite_button: tk.Button | None = None

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

        if self.on_toggle_sprite:
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

        name_label = tk.Label(
            self.frame,
            text=self.character,
            fg="#ffffff",
            bg="#18254c",
            font=("Segoe UI", 14, "bold"),
        )
        name_label.pack(pady=(0, 6))

        for crystal in CRYSTALS:
            row = tk.Frame(self.frame, bg="#1f305a")
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

            label = tk.Label(
                row,
                text="-",
                fg="#edf2ff",
                bg="#1f305a",
                font=("Segoe UI", 10),
                anchor="w",
                width=13,
            )
            label.pack(side="left", fill="x", expand=True)
            self.job_labels.append(label)

    def _load_image(self, path: Path) -> tk.PhotoImage:
        if not path.exists():
            raise FileNotFoundError(f"Sprite not found: {path}")
        return tk.PhotoImage(file=str(path))

    def update_jobs(self, assignments: dict[str, str]) -> None:
        for label, (crystal, job) in zip(self.job_labels, assignments.items()):
            label.config(text=job)

    def update_sprite(self, path: Path, button_text: str) -> None:
        self.image = self._load_image(path)
        self.sprite_label.configure(image=self.image)
        self.sprite_label.image = self.image
        if self.sprite_button:
            self.sprite_button.configure(text=button_text)


class FF5JobFiestaApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("FF5 4 Job Fiesta Randomizer")
        self.configure(bg="#0f162c")
        self.geometry("720x620")
        self.minsize(720, 580)
        self.resizable(False, False)

        self.randomizer = JobRandomizer(CRYSTALS, CHARACTERS)
        self.cards: dict[str, CharacterCard] = {}
        self.galuf_is_krile = False
        self.fullscreen_button: tk.Button | None = None

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
            sprite_path = SPRITES[character]
            on_toggle = self.toggle_galuf_krile_sprite if character == "Galuf/Krile" else None
            card = CharacterCard(
                grid_frame,
                character,
                sprite_path,
                row=index // 2,
                column=index % 2,
                on_toggle_sprite=on_toggle,
            )
            self.cards[character] = card

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

        self.fullscreen_button = tk.Button(
            footer,
            text="Full Screen",
            command=self.toggle_fullscreen,
            bg="#2f3c6b",
            fg="#edf2ff",
            activebackground="#3f4c7b",
            relief="flat",
            padx=10,
            pady=8,
            font=("Segoe UI", 10, "bold"),
        )
        self.fullscreen_button.pack(side="left", padx=(0, 14))
        self.bind("<Escape>", self._handle_escape)

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

        self.options_panel = OptionsPanel(self)

    def _clear_seed_placeholder(self, event: Any) -> None:
        if self.seed_var.get() == "Seed (optional)":
            self.seed_var.set("")

    def toggle_options_menu(self) -> None:
        self.options_panel.toggle()

    def toggle_fullscreen(self) -> None:
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)
        if self.fullscreen_button:
            self.fullscreen_button.configure(
                text="Windowed" if self.is_fullscreen else "Full Screen"
            )

    def _handle_escape(self, event: Any) -> None:
        if self.is_fullscreen:
            self.toggle_fullscreen()

    def toggle_galuf_krile_sprite(self) -> None:
        self.galuf_is_krile = not self.galuf_is_krile
        sprite_file = (
            "Assets/Krile_freelancer.png"
            if self.galuf_is_krile
            else "Assets/Galuf_freelancer.png"
        )
        card = self.cards.get("Galuf/Krile")
        if card:
            button_text = "Krile" if self.galuf_is_krile else "Galuf"
            card.update_sprite(Path(__file__).parent / sprite_file, button_text)

    def randomize_and_update(self) -> None:
        seed = None
        seed_text = self.seed_var.get()
        if seed_text and seed_text != "Seed (optional)":
            try:
                seed = int(seed_text)
            except ValueError:
                seed = None

        exclude_berserker, allow_same_crystal_job, include_previous_crystals = (
            self.options_panel.get_settings()
        )
        assignments = self.randomizer.randomize(
            seed,
            exclude_berserker=exclude_berserker,
            allow_same_crystal_job=allow_same_crystal_job,
            include_previous_crystals=include_previous_crystals,
        )

        for character, card in self.cards.items():
            card.update_jobs(assignments[character])


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] in {"console", "print"}:
        randomizer = JobRandomizer(CRYSTALS, CHARACTERS)
        assignments = randomizer.randomize()
        for character, crystals in assignments.items():
            print(f"\n{character}:")
            for crystal, job in crystals.items():
                print(f"  {crystal}: {job}")
        return

    app = FF5JobFiestaApp()
    app.mainloop()


if __name__ == "__main__":
    main()
