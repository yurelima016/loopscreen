// Switch inputs Logic

const radioUrl = document.getElementById("URL");
const radioFile = document.getElementById("File");
const containerUrl = document.getElementById("container-url");
const containerFile = document.getElementById("container-file");

function switchIputs() {
  if (radioUrl.checked) {
    containerUrl.style.display = "block";
    containerFile.style.display = "none";
  } else if (radioFile.checked) {
    containerUrl.style.display = "none";
    containerFile.style.display = "block";
  }
}

radioUrl.addEventListener("change", switchIputs);
radioFile.addEventListener("change", switchIputs);

const btnBrowse = document.getElementById("btn-browse-file");
const inputFile = document.getElementById("input-file");

btnBrowse.addEventListener("click", () => {
  pywebview.api.choose_file().then((caminhoReal) => {
    if (caminhoReal) {
      inputFile.value = caminhoReal;
    }
  });
});

// -----------------------------------------------------------------

// Add new screen Logic
const screensContainer = document.getElementById("screens-wrapper");
const addScreenButton = document.getElementById("add-screen-bt");

addScreenButton.addEventListener("click", () => {
  const screenName = document.getElementById("screen-name").value.trim();
  const screenDuration = document.getElementById("display-time").value.trim();

  const isUrlSelected = document.getElementById("URL").checked;
  const isFileSelected = document.getElementById("File").checked;

  let mediaValue = "";
  let mediaType = "";

  if (isUrlSelected) {
    mediaValue = document.getElementById("input-url").value.trim();
    mediaType = "URL";
  } else if (isFileSelected) {
    mediaValue = document.getElementById("input-file").value;
    mediaType = "File";
  }

  if (!screenName || !screenDuration || !mediaValue) {
    alert("Por favor, preencha todos os campos obrigatórios!");
    return;
  }

  const emptyTitle = screensContainer.querySelector("h3");
  if (emptyTitle) {
    emptyTitle.remove();
  }

  const newScreen = document.createElement("div");
  newScreen.classList.add("screens");

  newScreen.dataset.type = isUrlSelected ? "url" : "file";
  newScreen.dataset.value = mediaValue;
  newScreen.dataset.duration = screenDuration;

  newScreen.innerHTML = `
  <h4>${screenName}</h4>
  <p>Duration: ${screenDuration}s</p>
  <p>Source (${mediaType}): ${mediaValue}</p>
  <button class="delete-btn" title="Excluir tela"><i class="bi bi-trash3-fill"></i></button>
`;
  screensContainer.appendChild(newScreen);

  const deleteBtn = newScreen.querySelector(".delete-btn");
  deleteBtn.addEventListener("click", () => {
    newScreen.remove();
  });

  document.getElementById("screen-name").value = "";
  document.getElementById("display-time").value = "";
  document.getElementById("input-url").value = "";
  document.getElementById("input-file").value = "";
});

// -----------------------------------------------------------------

// Theme toggle Logic
const button = document.getElementById("theme-toggle");
const icon = document.getElementById("theme-icon");
const body = document.body;
const savedTheme = localStorage.getItem("theme");

// Default theme: Light
body.dataset.theme = savedTheme ?? "light";

function syncThemeAndIcon() {
  const isLight = body.dataset.theme === "light";

  icon.classList.remove("bi-brightness-high", "bi-moon");
  icon.classList.add(isLight ? "bi-moon" : "bi-brightness-high");
}

syncThemeAndIcon();

button.addEventListener("click", () => {
  body.dataset.theme = body.dataset.theme === "light" ? "dark" : "light";
  syncThemeAndIcon();
  localStorage.setItem("theme", body.dataset.theme);
});

// ---------------------------------------------------------------------

// Start System Logic

const startButton = document.getElementById("start-button");

startButton.addEventListener("click", () => {
  let playlist = [];

  const addedScreens = document.querySelectorAll(".screens");

  addedScreens.forEach((screen) => {
    playlist.push({
      type: screen.dataset.type,
      value: screen.dataset.value,
      duration: parseInt(screen.dataset.duration),
    });
  });

  if (playlist.length < 2) {
    alert("Por favor, adicione pelo menos 2 telas para iniciar o LoopScreen!");
    return;
  }

  pywebview.api.start_system(playlist);
});

// -----------------------------------------------------------------

// Window Controls Logic

document.getElementById("btn-minimize").addEventListener("click", () => {
  pywebview.api.minimize_window();
});

const btnMaximize = document.getElementById("btn-maximize");
const iconMaximize = btnMaximize.querySelector("i");

btnMaximize.addEventListener("click", async () => {
  const isMaximized = await pywebview.api.maximize_window();

  if (isMaximized) {
    iconMaximize.classList.remove("bi-square");
    iconMaximize.classList.add("bi-window-stack");
    btnMaximize.title = "Restaurar";
  } else {
    iconMaximize.classList.remove("bi-window-stack");
    iconMaximize.classList.add("bi-square");
    btnMaximize.title = "Maximizar";
  }
});

document.getElementById("btn-close").addEventListener("click", () => {
  pywebview.api.close_window();
});
