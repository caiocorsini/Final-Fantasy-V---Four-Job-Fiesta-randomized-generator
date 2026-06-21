const endpoint = "/randomize";
const button = document.getElementById("randomizeButton");
const cardsContainer = document.getElementById("cards");

const characters = [
  { id: "Bartz", name: "Bartz", sprite: "Assets/Bartz_freelancer.png" },
  { id: "Lenna", name: "Lenna", sprite: "Assets/Lenna_freelancer.png" },
  { id: "Faris", name: "Faris", sprite: "Assets/Faris_freelancer.png" },
  { id: "Galuf-Krile", name: "Galuf/Krile", sprite: "Assets/Galuf_freelancer.png" },
];

function buildCards() {
  cardsContainer.innerHTML = characters
    .map(
      (character) => `
        <article class="card" id="card-${character.name}">
          <img src="${character.sprite}" alt="${character.name} sprite" />
          <div>
            <h2>${character.name}</h2>
            <p class="subtitle">Waiting for a random job set...</p>
          </div>
          <ul class="job-list"></ul>
        </article>
      `
    )
    .join("");
}

async function refreshJobs() {
  try {
    button.disabled = true;
    button.textContent = "Randomizing...";
    const response = await fetch(endpoint);
    const assignments = await response.json();

    characters.forEach((character) => {
      const card = document.getElementById(`card-${character.id}`);
      const jobList = card.querySelector(".job-list");
      const subtitle = card.querySelector(".subtitle");

      jobList.innerHTML = Object.entries(assignments[character.name])
        .map(
          ([crystal, job]) =>
            `<li><span>${crystal} Crystal</span><strong>${job}</strong></li>`
        )
        .join("");

      subtitle.textContent = "Ready for battle";
    });
  } catch (error) {
    console.error(error);
    alert("Unable to fetch random jobs. Make sure the Python server is running.");
  } finally {
    button.disabled = false;
    button.textContent = "Randomize Jobs";
  }
}

button.addEventListener("click", refreshJobs);

buildCards();
