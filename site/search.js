"use strict";

const OPTIONS_HISTORY = window.OPTIONS_HISTORY || [];

const ENV_LABELS = {
    coreutils: "Coreutils",
    toybox: "Toybox",
    autre: "Autre",
};

const ENV_ALIASES = {
    coreutils: "coreutils",
    toybox: "toybox",
    autre: "autre",
    other: "autre",
};

const form = document.getElementById("search-form");
const programInput = document.getElementById("programme");
const environmentSelect = document.getElementById("environnement");
const versionSelect = document.getElementById("version");
const statusText = document.getElementById("search-status");
const resultPanel = document.getElementById("search-result");
const resultProgram = document.getElementById("result-programme");
const resultEnvironment = document.getElementById("result-environnement");
const resultVersion = document.getElementById("result-version");
const resultOptions = document.getElementById("result-options");

let selectedVersions = [];

function normalize(value) {
    return String(value || "").trim().toLowerCase();
}

function normalizeEnvironment(environment) {
    return ENV_ALIASES[normalize(environment)] || "";
}

function formatCount(value) {
    const number = Number(value);
    if (!Number.isFinite(number)) {
        return String(value);
    }
    return String(Math.trunc(number));
}

function entriesFor(programName, environment) {
    const wantedProgram = normalize(programName);
    const wantedEnvironment = normalizeEnvironment(environment);

    if (!wantedProgram || !wantedEnvironment) {
        return [];
    }

    return OPTIONS_HISTORY.filter((entry) => (
        entry.environment === wantedEnvironment
        && entry.aliases.includes(wantedProgram)
    ));
}

function versionEntries(programName, environment) {
    return entriesFor(programName, environment)
        .flatMap((entry) => (
            Object.entries(entry.versions).map(([version, options]) => ({
                environment: entry.environment,
                name: entry.name,
                options,
                version,
            }))
        ))
        .sort((left, right) => (
            Number(right.version) - Number(left.version)
            || left.name.localeCompare(right.name)
        ));
}

function getAvailableVersions(programName, environment) {
    const versions = versionEntries(programName, environment).map((entry) => entry.version);
    return Array.from(new Set(versions));
}

function getOptionCount(programName, environment, version) {
    const wantedVersion = String(version || "").trim();
    const entry = versionEntries(programName, environment)
        .find((candidate) => candidate.version === wantedVersion);

    if (!entry) {
        return null;
    }

    return entry.options;
}

function resetResult() {
    resultPanel.hidden = true;
    resultProgram.textContent = "";
    resultEnvironment.textContent = "";
    resultVersion.textContent = "";
    resultOptions.textContent = "";
}

function resetVersions(message) {
    selectedVersions = [];
    versionSelect.disabled = true;
    versionSelect.replaceChildren(new Option(message, ""));
    resetResult();
}

function updateVersions() {
    const programName = programInput.value.trim();
    const environment = environmentSelect.value;

    if (!programName) {
        resetVersions("Choisissez d'abord un programme");
        statusText.textContent = `${OPTIONS_HISTORY.length} programmes disponibles.`;
        return;
    }

    selectedVersions = versionEntries(programName, environment);

    if (selectedVersions.length === 0) {
        resetVersions("Aucune version disponible");
        statusText.textContent = `Aucune donnee trouvee pour "${programName}" dans ${ENV_LABELS[environment]}.`;
        return;
    }

    versionSelect.disabled = false;
    versionSelect.replaceChildren(
        new Option("Selectionner une version", ""),
        ...selectedVersions.map((entry, index) => (
            new Option(`${entry.version} - ${formatCount(entry.options)} options`, String(index))
        ))
    );
    resetResult();
    statusText.textContent = `${getAvailableVersions(programName, environment).length} version(s) disponible(s) pour "${programName}".`;
}

function showResult() {
    if (versionSelect.value === "") {
        resetResult();
        return;
    }

    const entry = selectedVersions[Number(versionSelect.value)];
    if (!entry) {
        resetResult();
        return;
    }

    resultProgram.textContent = entry.name;
    resultEnvironment.textContent = ENV_LABELS[entry.environment];
    resultVersion.textContent = entry.version;
    resultOptions.textContent = formatCount(entry.options);
    resultPanel.hidden = false;
}

window.getAvailableVersions = getAvailableVersions;
window.getOptionCount = getOptionCount;
window.versionsDisponibles = getAvailableVersions;
window.nombreOptions = getOptionCount;

form.addEventListener("submit", (event) => {
    event.preventDefault();
    updateVersions();
});

programInput.addEventListener("input", updateVersions);
environmentSelect.addEventListener("change", updateVersions);
versionSelect.addEventListener("change", showResult);

resetVersions("Choisissez d'abord un programme");
statusText.textContent = `${OPTIONS_HISTORY.length} programmes disponibles.`;
