const dropArea = document.getElementById("drop-area");
const fileElem = document.getElementById("fileElem");

dropArea.addEventListener("click", () => fileElem.click());

fileElem.addEventListener("change", e => {
    uploadFile(e.target.files[0]);
});

dropArea.addEventListener("dragover", e => {
    e.preventDefault();
    dropArea.classList.add("highlight");
});

dropArea.addEventListener("dragleave", () => {
    dropArea.classList.remove("highlight");
});

dropArea.addEventListener("drop", e => {
    e.preventDefault();
    dropArea.classList.remove("highlight");
    uploadFile(e.dataTransfer.files[0]);
});


async function uploadFile(file) {
    const formData = new FormData();
    formData.append("file", file);

    document.getElementById("loader").classList.remove("hidden");

    try {
        const res = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        document.getElementById("loader").classList.add("hidden");

        if (data.error) {
            document.getElementById("status").innerText = data.error;
            return;
        }

        document.getElementById("status").innerText = data.message;
        document.getElementById("sqlBox").innerText = data.sql;

        renderTable(data.preview);

        // ✅ show chat
        document.getElementById("chatBox").classList.remove("hidden");

    } catch {
        document.getElementById("status").innerText = "Upload failed";
    }
}


function renderTable(data) {
    const table = document.getElementById("previewTable");
    table.innerHTML = "";

    if (!data.length) return;

    const headers = Object.keys(data[0]);

    let headerRow = "<tr>";
    headers.forEach(h => headerRow += `<th>${h}</th>`);
    headerRow += "</tr>";

    table.innerHTML += headerRow;

    data.forEach(row => {
        let r = "<tr>";
        headers.forEach(h => r += `<td>${row[h]}</td>`);
        r += "</tr>";
        table.innerHTML += r;
    });
}


async function sendQuery() {
    const query = document.getElementById("queryInput").value;

    document.getElementById("chatSQL").innerText = "Loading...";

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(query)
        });

        const data = await res.json();

        if (data.error) {
            document.getElementById("chatSQL").innerText = data.error;
            return;
        }

        document.getElementById("chatSQL").innerText = data.sql;

        renderChatTable(data.results);

    } catch {
        document.getElementById("chatSQL").innerText = "Error";
    }
}


function renderChatTable(data) {
    const table = document.getElementById("chatResult");
    table.innerHTML = "";

    if (!data.length) {
        table.innerHTML = "<tr><td>No results</td></tr>";
        return;
    }

    const headers = Object.keys(data[0]);

    let headerRow = "<tr>";
    headers.forEach(h => headerRow += `<th>${h}</th>`);
    headerRow += "</tr>";

    table.innerHTML += headerRow;

    data.forEach(row => {
        let r = "<tr>";
        headers.forEach(h => r += `<td>${row[h]}</td>`);
        r += "</tr>";
        table.innerHTML += r;
    });
}
