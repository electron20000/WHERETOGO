const VAR_MAP = {
  bg_color: "--bg-color",
  header_color: "--header-color",
  card_text: "--card-text",
  card_overlay: "--card-overlay",
  card_open_start: "--card-open-start",
  card_open_end: "--card-open-end",
  card_closed_start: "--card-closed-start",
  card_closed_end: "--card-closed-end",
  card_zone_start: "--card-zone-start",
  card_zone_end: "--card-zone-end",
  card_border: "--card-border",
  important_border: "--important-border",
  button_bg: "--button-bg",
  button_text: "--button-text",
  input_bg: "--input-bg",
  input_text: "--input-text",
};

function applyOrientation() {
  const orientationInput =
    document.querySelector('[name="orientation"]:checked') ||
    document.querySelector('[name="orientation"]');
  const orientation =
    orientationInput?.value || document.body.dataset.orientation || "landscape";
  document.body.dataset.orientation = orientation;
  const previewRoot = document.querySelector("[data-preview-root]");
  if (previewRoot) {
    previewRoot.dataset.orientation = orientation;
  }
}

function setupAutoRefresh() {
  const container = document.getElementById("cards-container");
  if (!container) return;
  const refreshUrl = container.dataset.refreshUrl;
  const lastUpdated = document.querySelector("#last-updated .timestamp-value");
  let timestamp = container.dataset.timestamp;

  async function pull() {
    try {
      const response = await fetch(refreshUrl, { headers: { "X-Requested-With": "XMLHttpRequest" } });
      const data = await response.json();
      if (data.timestamp !== timestamp) {
        container.innerHTML = data.html;
        timestamp = data.timestamp;
        container.dataset.timestamp = timestamp;
        if (lastUpdated) {
          lastUpdated.textContent = timestamp;
        }
      }
    } catch (err) {
      console.error("Nie udało się pobrać aktualizacji", err);
    }
  }

  setInterval(pull, 5000);
}

function setupFormsets() {
  document.querySelectorAll(".add-form").forEach((button) => {
    button.addEventListener("click", () => {
      const prefix = button.dataset.prefix;
      const formset = button.closest(".formset");
      const totalInput = formset.querySelector(`input[name="${prefix}-TOTAL_FORMS"]`);
      const currentIndex = parseInt(totalInput.value, 10);
      const emptyForm = formset.querySelector("template.empty-form");
      if (!emptyForm) return;

      const templateHtml = emptyForm.innerHTML.replace(/__prefix__/g, currentIndex);
      const newForm = document.createElement("div");
      newForm.className = "message-form";
      newForm.innerHTML = templateHtml;

      totalInput.value = currentIndex + 1;
      formset.insertBefore(newForm, button);
    });
  });
}

function applyColorsFromInputs() {
  Object.keys(VAR_MAP).forEach((key) => {
    const input = document.querySelector(`input[name="${key}"]`);
    if (input && input.value) {
      document.documentElement.style.setProperty(VAR_MAP[key], input.value);
    }
  });
}

function setupOrientationControls() {
  const orientationInputs = document.querySelectorAll('[name="orientation"]');
  if (!orientationInputs.length) {
    return applyOrientation();
  }
  orientationInputs.forEach((input) => {
    input.addEventListener("change", applyOrientation);
  });
  applyOrientation();
}

function setupAppearancePreview() {
  const previewButton = document.getElementById("open-preview");
  const previewArea = document.getElementById("preview-area");
  const colorModal = document.getElementById("color-modal");
  const modalPicker = document.getElementById("modal-color-picker");
  const closeModal = document.getElementById("close-color-modal");
  let activeTargets = [];

  if (!previewButton || !previewArea) return;

  previewButton.addEventListener("click", async () => {
    previewArea.hidden = false;
    if (!previewArea.dataset.loaded) {
      const url = previewArea.dataset.previewUrl;
      const response = await fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } });
      const data = await response.json();
      previewArea.innerHTML = data.html;
      previewArea.dataset.loaded = "true";
      applyOrientation();
    }
    applyColorsFromInputs();
  });

  previewArea.addEventListener("click", (event) => {
    const card = event.target.closest("[data-color-target]");
    if (!card) return;
    activeTargets = card.dataset.colorTarget.split(" ").filter(Boolean);
    if (!activeTargets.length) return;
    const first = document.querySelector(`input[name="${activeTargets[0]}"]`);
    if (first) {
      modalPicker.value = first.value || "#000000";
    }
    colorModal.hidden = false;
  });

  modalPicker.addEventListener("input", () => {
    activeTargets.forEach((target) => {
      const field = document.querySelector(`input[name="${target}"]`);
      if (field) {
        field.value = modalPicker.value;
        if (VAR_MAP[target]) {
          document.documentElement.style.setProperty(VAR_MAP[target], modalPicker.value);
        }
      }
    });
  });

  closeModal?.addEventListener("click", () => {
    colorModal.hidden = true;
  });
}

document.addEventListener("DOMContentLoaded", () => {
  setupAutoRefresh();
  setupFormsets();
  setupAppearancePreview();
  applyColorsFromInputs();
  setupOrientationControls();
});
