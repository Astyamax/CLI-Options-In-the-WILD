"use strict";

const CSV_PATHS = [
    "data/history.csv",
    "./data/history.csv",
    "../data/history.csv",
    "site/data/history.csv",
];

const ENV_LABELS = {
    coreutils: "Coreutils",
    toybox: "Toybox",
    autre: "Autre",
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

let records = [];
let years = [];
let selectedVersions = [];
let loadedCsvPath = "";
let csvIsLoaded = false;
const FETCH_TIMEOUT_MS = 1200;

function splitCsv(text) {
    const rows = [];
    let row = [];
    let cell = "";
    let quoted = false;

    for (let index = 0; index < text.length; index += 1) {
        const char = text[index];
        const next = text[index + 1];

        if (char === '"' && quoted && next === '"') {
            cell += '"';
            index += 1;
        } else if (char === '"') {
            quoted = !quoted;
        } else if (char === "," && !quoted) {
            row.push(cell);
            cell = "";
        } else if ((char === "\n" || char === "\r") && !quoted) {
            if (char === "\r" && next === "\n") {
                index += 1;
            }
            row.push(cell);
            if (row.some((value) => value.trim() !== "")) {
                rows.push(row);
            }
            row = [];
            cell = "";
        } else {
            cell += char;
        }
    }

    if (cell !== "" || row.length > 0) {
        row.push(cell);
        rows.push(row);
    }

    return rows;
}

function normalize(value) {
    return String(value || "").trim().toLowerCase();
}

function cleanCommandName(value) {
    let name = String(value || "").trim();

    if (name.startsWith("./")) {
        name = name.slice(2);
    }
    if (name.startsWith("toybox ")) {
        name = name.slice("toybox ".length);
    }

    return name.trim();
}

function environmentFromProgramme(programme) {
    const value = normalize(programme);

    if (value === "coreutils") {
        return "coreutils";
    }
    if (value === "toybox") {
        return "toybox";
    }
    return "autre";
}

function namesFor(programme, command) {
    const rawProgramme = String(programme || "").trim();
    const rawCommand = String(command || "").trim();
    const cleanedCommand = cleanCommandName(rawCommand);

    return Array.from(new Set([
        rawProgramme,
        rawCommand,
        cleanedCommand,
    ].map(normalize).filter(Boolean)));
}

function parseHistoryCsv(text) {
    const rows = splitCsv(text);
    const headers = rows[0] || [];
    const programmeIndex = headers.indexOf("programme");
    const commandIndex = headers.indexOf("commande");

    years = headers.filter((header) => /^\d{4}$/.test(header));

    if (programmeIndex === -1 || commandIndex === -1 || years.length === 0) {
        throw new Error("Invalid history CSV");
    }

    return rows.slice(1).map((row) => {
        const programme = row[programmeIndex] || "";
        const command = row[commandIndex] || "";
        const valuesByYear = {};

        years.forEach((year) => {
            const yearIndex = headers.indexOf(year);
            valuesByYear[year] = row[yearIndex] || "";
        });

        return {
            programme,
            command,
            displayName: cleanCommandName(command) || programme,
            environment: environmentFromProgramme(programme),
            names: namesFor(programme, command),
            valuesByYear,
        };
    });
}

function loadCsvText(sourceName, text) {
    const parsedRecords = parseHistoryCsv(text);

    records = parsedRecords;
    loadedCsvPath = sourceName;
    csvIsLoaded = true;
    statusText.textContent = `${records.length} lignes chargees depuis ${loadedCsvPath}.`;

    updateVersions();
}

async function fetchCsv(path) {
    const separator = path.includes("?") ? "&" : "?";
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);

    try {
        const response = await fetch(`${path}${separator}v=${Date.now()}`, {
            cache: "no-store",
            signal: controller.signal,
        });

        if (!response.ok) {
            throw new Error(`${path}: HTTP ${response.status}`);
        }

        return {
            path,
            text: await response.text(),
        };
    } finally {
        clearTimeout(timeout);
    }
}

async function fetchFirstAvailableCsv() {
    const attempts = CSV_PATHS.map(async (path) => {
        try {
            return await fetchCsv(path);
        } catch (error) {
            return null;
        }
    });

    const results = await Promise.all(attempts);
    return results.find((result) => result !== null) || null;
}

async function loadCsv() {
    const source = await fetchFirstAvailableCsv();
    if (source) {
        loadCsvText(source.path, source.text);
        return;
    }

    if (
        typeof window !== "undefined"
        && typeof window.HISTORY_CSV_DATA === "string"
        && window.HISTORY_CSV_DATA.trim() !== ""
    ) {
        loadCsvText("history-data.js", window.HISTORY_CSV_DATA);
        return;
    }

    records = [];
    csvIsLoaded = false;
    resetVersions("Historique indisponible");
    statusText.textContent = "Impossible de charger history.csv ou history-data.js.";
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

function formatCount(value) {
    const number = Number(value);
    if (!Number.isFinite(number)) {
        return String(value);
    }
    return String(Math.trunc(number));
}

function findRecords() {
    const wantedProgram = normalize(programInput.value);
    const wantedEnvironment = environmentSelect.value;

    if (!wantedProgram) {
        return [];
    }

    return records.filter((record) => (
        record.environment === wantedEnvironment
        && record.names.includes(wantedProgram)
    ));
}

function buildVersions(matches) {
    return matches.flatMap((record) => (
        years
            .filter((year) => record.valuesByYear[year] !== "")
            .map((year) => ({
                record,
                year,
                options: record.valuesByYear[year],
            }))
    )).sort((left, right) => Number(right.year) - Number(left.year));
}

function updateVersions() {
    const programName = programInput.value.trim();

    if (!csvIsLoaded) {
        resetVersions("Chargement du CSV...");
        statusText.textContent = "Chargement du CSV en cours.";
        return;
    }

    if (!programName) {
        resetVersions("Choisissez d'abord un programme");
        statusText.textContent = `${records.length} lignes chargees depuis ${loadedCsvPath}.`;
        return;
    }

    const matches = findRecords();
    selectedVersions = buildVersions(matches);

    if (selectedVersions.length === 0) {
        resetVersions("Aucune version disponible");
        statusText.textContent = `Aucune donnee trouvee pour "${programName}" dans ${ENV_LABELS[environmentSelect.value]}. CSV: ${loadedCsvPath}.`;
        return;
    }

    versionSelect.disabled = false;
    versionSelect.replaceChildren(
        new Option("Selectionner une version", ""),
        ...selectedVersions.map((entry, index) => (
            new Option(`${entry.year} - ${formatCount(entry.options)} options`, String(index))
        ))
    );
    resetResult();
    statusText.textContent = `${selectedVersions.length} version(s) disponible(s) pour "${programName}". CSV: ${loadedCsvPath}.`;
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

    resultProgram.textContent = entry.record.displayName;
    resultEnvironment.textContent = ENV_LABELS[entry.record.environment];
    resultVersion.textContent = entry.year;
    resultOptions.textContent = formatCount(entry.options);
    resultPanel.hidden = false;
}

form.addEventListener("submit", (event) => {
    event.preventDefault();
    updateVersions();
});

programInput.addEventListener("input", updateVersions);
environmentSelect.addEventListener("change", updateVersions);
versionSelect.addEventListener("change", showResult);

loadCsv();
