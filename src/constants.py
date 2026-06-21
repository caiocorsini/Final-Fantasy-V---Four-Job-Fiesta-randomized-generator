from pathlib import Path

CRYSTALS = {
    "Wind": ["Knight", "Monk", "Thief", "White Mage", "Black Mage", "Blue Mage"],
    "Water": ["Berserker", "Mystic Knight", "Time Mage", "Summoner", "Red Mage"],
    "Fire": ["Geomancer", "Beastmaster", "Ninja", "Bard", "Ranger"],
    "Earth": ["Samurai", "Dancer", "Dragoon", "Chemist"],
}
CHARACTERS = ["Bartz", "Lenna", "Faris", "Galuf/Krile"]
SPRITES = {
    "Bartz": "Bartz_feelancer.png",
    "Lenna": "Lenna_freelancer.png",
    "Faris": "Faris_freelancer.png",
    "Galuf/Krile": "Galuf_freelancer.png",
}
ASSETS_DIR = Path(__file__).parent.parent / "Assets"
