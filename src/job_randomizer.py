import random
from typing import Dict


class JobRandomizer:
    def __init__(self, crystals: Dict[str, list[str]], characters: list[str]) -> None:
        self.crystals = crystals
        self.characters = characters

    def randomize(
        self,
        seed: int | None = None,
        exclude_berserker: bool = False,
        allow_same_crystal_job: bool = False,
        include_previous_crystals: bool = False,
        selected_jobs: set[str] | None = None,
    ) -> dict:
        if seed is not None:
            random.seed(seed)

        if selected_jobs is None:
            selected_jobs = {
                job for job_list in self.crystals.values() for job in job_list
            }

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
                job
                for job in jobs
                if job in selected_jobs and not (exclude_berserker and job == "Berserker")
            ]
            if not available_jobs:
                raise ValueError(
                    f"No selectable jobs available for crystal '{crystal}'. "
                    "Adjust the Deep Customization selection."
                )

            if allow_same_crystal_job or len(available_jobs) < len(self.characters):
                assignments = [random.choice(available_jobs) for _ in self.characters]
            else:
                assignments = random.sample(available_jobs, k=len(self.characters))

            for character, job in zip(self.characters, assignments):
                result[character][crystal] = job

        return result
