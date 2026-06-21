import random
import tkinter as tk
from pathlib import Path
from typing import Any

from .character_card import CharacterCard
from .constants import ASSETS_DIR, CHARACTERS, CRYSTALS, SPRITES
from .job_randomizer import JobRandomizer
from .options_panel import OptionsPanel


class FF5JobFiestaApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("FF5 4 Job Fiesta Randomizer")
        self.configure(bg="#0f162c")
        self.geometry("720x760")
        self.minsize(720, 760)
        self.resizable(True, True)

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
            sprite_path = ASSETS_DIR / SPRITES[character]
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
        seed_entry.bind("<FocusOut>", self._restore_seed_placeholder)

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

        self.seed_info_label = tk.Label(
            footer,
            text="",
            fg="#bbc8ea",
            bg="#0f162c",
            font=("Segoe UI", 10),
        )
        self.seed_info_label.pack(side="left", padx=(14, 0))

        copy_seed_button = tk.Button(
            footer,
            text="Copy Seed",
            command=self.copy_seed_to_clipboard,
            bg="#2f3c6b",
            fg="#edf2ff",
            activebackground="#3f4c7b",
            relief="flat",
            padx=10,
            pady=8,
            font=("Segoe UI", 10, "bold"),
        )
        copy_seed_button.pack(side="left", padx=(10, 0))

        self.options_panel = OptionsPanel(self)

    def _clear_seed_placeholder(self, event: Any) -> None:
        if self.seed_var.get() == "Seed (optional)":
            self.seed_var.set("")

    def _restore_seed_placeholder(self, event: Any) -> None:
        if not self.seed_var.get().strip():
            self.seed_var.set("Seed (optional)")

    def toggle_options_menu(self) -> None:
        self.options_panel.toggle()

    def toggle_fullscreen(self) -> None:
        self.attributes("-fullscreen", not self.attributes("-fullscreen"))
        is_fullscreen = self.attributes("-fullscreen")
        if self.fullscreen_button:
            self.fullscreen_button.configure(
                text="Windowed" if is_fullscreen else "Full Screen"
            )

    def _handle_escape(self, event: Any) -> None:
        if self.attributes("-fullscreen"):
            self.toggle_fullscreen()

    def toggle_galuf_krile_sprite(self) -> None:
        self.galuf_is_krile = not self.galuf_is_krile
        sprite_file = (
            "Krile_freelancer.png"
            if self.galuf_is_krile
            else "Galuf_freelancer.png"
        )
        card = self.cards.get("Galuf/Krile")
        if card:
            button_text = "Krile" if self.galuf_is_krile else "Galuf"
            card.update_sprite(ASSETS_DIR / sprite_file, button_text)

    def copy_seed_to_clipboard(self) -> None:
        seed_text = self.seed_info_label.cget("text")
        if seed_text.startswith("Share this seed:"):
            seed = seed_text.split(":", 1)[1].strip()
            self.clipboard_clear()
            self.clipboard_append(seed)
            self.seed_info_label.configure(text=f"Seed copied: {seed}")

    def randomize_and_update(self) -> None:
        seed = None
        seed_text = self.seed_var.get()
        if seed_text and seed_text != "Seed (optional)":
            try:
                seed = int(seed_text)
            except ValueError:
                seed = None

        if seed is None:
            seed = random.randint(0, 2**31 - 1)

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

        self.seed_info_label.configure(text=f"Share this seed: {seed}")
