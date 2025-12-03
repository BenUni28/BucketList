const addButton = document.getElementById("addButton");
const formContainer = document.getElementById("formContainer");
const saveButton = document.getElementById("saveButton");
const tableBody = document.querySelector("#ideasTable tbody");

let currentEditId = null;

addButton.addEventListener("click", () => {
  currentEditId = null;
  formContainer.classList.toggle("hidden");

  document.getElementById("what").value = "";
  document.getElementById("where").value = "";
  document.getElementById("when").value = "";
  document.getElementById("link").value = "";
});

async function loadIdeas() {
  const res = await fetch("/items/all-items");
  const data = await res.json();

  tableBody.innerHTML = "";

  data.items.forEach(item => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td style="display:none;">${item.id}</td>
      <td>${item.what}</td>
      <td>${item.where || ""}</td>
      <td>${item.when || ""}</td>
      <td>${item.link ? `<a href="${item.link}" target="_blank">${item.link}</a>` : ""}</td>
      <td>
        <button class="edit-btn" data-id="${item.id}">✏️</button>
        <button class="delete-btn" data-id="${item.id}">🗑️</button>
      </td>
    `;
    tableBody.appendChild(row);
  });
}


tableBody.addEventListener("click", (event) => {
  if (event.target.classList.contains("delete-btn")) {
    const id = event.target.dataset.id;
    deleteIdea(id);
  }

  if (event.target.classList.contains("edit-btn")){
    loadIdeaIntoForm(event.target.dataset.id);
  }
});

async function loadIdeaIntoForm(id) {
  const res = await fetch(`/items/get-item/${id}`);
  const data = await res.json();

  const item = data.item;

  document.getElementById("what").value = item.what;
  document.getElementById("where").value = item.where || "";
  document.getElementById("when").value = item.when || "";
  document.getElementById("link").value = item.link || "";

  currentEditId = id;

  formContainer.classList.remove("hidden");
}

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

  const body = { what, where, when, link };

  if (currentEditId) {
    const res = await fetch(`/items/update-item/${currentEditId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      console.error("Update fehlgeschlagen");
      return;
    }

    await res.json();
  }

  else {
    await fetch("/items/add-item", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
  }

  formContainer.classList.add("hidden");

  loadIdeas();
});


loadIdeas();
