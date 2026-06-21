# FF5 4 Job Fiesta Randomizer

A small Python/Tkinter app for randomizing one job per crystal for the characters in Final Fantasy V.

## Project structure

- `main.py` - application entrypoint
- `src/` - application modules
  - `src/main_app.py` - main Tkinter app and UI layout
  - `src/character_card.py` - character card UI and sprite handling
  - `src/options_panel.py` - options menu and toggles
  - `src/job_randomizer.py` - randomization logic
  - `src/constants.py` - shared crystals, characters, sprites, and assets path
- `Assets/` - sprite image assets used by the app

## Requirements

- Python 3.10+ (or newer)

## Run

From the project root:

```bash
python main.py
```

## How to use

1. Launch the app with `python main.py`.
2. Enter an optional numeric seed in the seed field to reproduce the same randomization.
3. Click `Randomize Jobs` to generate one job for each crystal per character.
4. Open `Options` to toggle:
   - `Exclude Berserker`
   - `Allow same job in same crystal`
   - `Include previous crystal jobs`
5. Click `Full Screen` to enlarge the window, or press `Esc` to exit fullscreen.
6. For the Galuf/Krile card, click the small sprite button to swap between Galuf and Krile.

## Notes

- `.gitignore` is included for Python cache files and common editor/OS artifacts.
- The app supports a resizeable window and configurable randomizer options.
