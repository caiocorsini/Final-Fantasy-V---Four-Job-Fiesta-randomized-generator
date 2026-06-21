import random

CRYSTALS = {
    "Wind": ["Knight", "Monk", "Thief", "White Mage", "Black Mage", "Blue Mage"],
    "Water": ["Berserker", "Mystic Knight", "Time Mage", "Summoner", "Red Mage", "Mime"],
    "Fire": ["Geomancer", "Beastmaster", "Ninja", "Bard", "Ranger"],
    "Earth": ["Samurai", "Dancer", "Dragoon", "Chemist"],
}
CHARACTERS = ["Bartz", "Lenna", "Faris", "Galuf"]


def randomize_jobs(seed: int | None = None) -> dict:
    """Assign one random job from each crystal to each of the four characters."""
    if seed is not None:
        random.seed(seed)

    result = {character: {} for character in CHARACTERS}
    for crystal, jobs in CRYSTALS.items():
        assignments = random.sample(jobs, k=4) if len(jobs) >= 4 else [random.choice(jobs) for _ in range(4)]
        for character, job in zip(CHARACTERS, assignments):
            result[character][crystal] = job
    return result


def print_randomizer(assignments: dict) -> None:
    print("Final Fantasy V - 4 Job Fiesta Randomizer")
    print("========================================")
    for character, crystals in assignments.items():
        print(f"\n{character}:")
        for crystal, job in crystals.items():
            print(f"  {crystal} Crystal: {job}")


if __name__ == "__main__":
    randomizer = randomize_jobs()
    print_randomizer(randomizer)
