const addButton = document.getElementById("addButton");
const formContainer = document.getElementById("formContainer");
const saveButton = document.getElementById("saveButton");
const tableBody = document.querySelector("#ideasTable tbody");


addButton.addEventListener("click", () => {
  formContainer.classList.toggle("hidden");
});

async function loadIdeas() {
  const res = await fetch("/items/all-items");
  const data = await res.json();

  tableBody.innerHTML = "";

  data.items.sort((a, b) => {
    if (!a.when) return 1;
    if (!b.when) return -1;
    return new Date(a.when) - new Date(b.when);
  });

  data.items.forEach(item => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td style="display:none;">${item.id}</td>
      <td>${item.what}</td>
      <td>${item.where || ""}</td>
      <td>${item.when || ""}</td>
      <td>${item.link ? `<a href="${item.link}" target="_blank">${item.link}</a>` : ""}</td>
      <td><button class="delete-btn" data-id="${item.id}">🗑️</button></td>
    `;
    tableBody.appendChild(row);
  });
}

tableBody.addEventListener("click", (event) => {
  if (event.target.classList.contains("delete-btn")) {
    const id = event.target.dataset.id;
    deleteIdea(id);
  }
});

async function deleteIdea(id) {
  await fetch(`/items/delete-item/${id}`, { method: "DELETE" });
  loadIdeas();
}

saveButton.addEventListener("click", async () => {
  const what = document.getElementById("what").value;
  const where = document.getElementById("where").value;
  const when = document.getElementById("when").value;
  const link = document.getElementById("link").value;

  if (!what) {
    alert("Bitte mindestens 'Was?' ausfüllen.");
    return;
  }

  await fetch("/items/add-item", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ what, where, when, link })
  });

  formContainer.classList.add("hidden");
  document.getElementById("what").value = "";
  document.getElementById("where").value = "";
  document.getElementById("when").value = "";
  document.getElementById("link").value = "";

  loadIdeas();
});

loadIdeas();
