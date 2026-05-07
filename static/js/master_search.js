document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("masterSearchInput");
    const dropdown = document.getElementById("masterSearchDropdown");

    if (!input || !dropdown) return;

    let debounceTimer = null;
    let lastQuery = "";

    function hideDropdown() {
        dropdown.style.display = "none";
        dropdown.innerHTML = "";
    }

    function showLoading() {
        dropdown.innerHTML = `
            <div class="search-empty">
                Searching...
            </div>
        `;
        dropdown.style.display = "block";
    }

    function renderResults(results) {
        if (!results || results.length === 0) {
            dropdown.innerHTML = `
                <div class="search-empty">
                    No result found.
                </div>
            `;
            dropdown.style.display = "block";
            return;
        }

        dropdown.innerHTML = results.map(item => `
            <a href="${item.url}" class="search-result-item">
                <div class="search-result-icon">${item.icon || "🔎"}</div>
                <div class="search-result-content">
                    <div class="search-result-type">${item.type}</div>
                    <div class="search-result-title">${item.title}</div>
                    <div class="search-result-desc">${item.description || ""}</div>
                </div>
            </a>
        `).join("");

        dropdown.style.display = "block";
    }

    async function performSearch(query) {
        if (query.length < 2) {
            hideDropdown();
            return;
        }

        if (query === lastQuery) return;

        lastQuery = query;
        showLoading();

        try {
            const response = await fetch(`/search/live/?q=${encodeURIComponent(query)}`, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            if (!response.ok) {
                throw new Error("Search request failed");
            }

            const data = await response.json();
            renderResults(data.results);
        } catch (error) {
            dropdown.innerHTML = `
                <div class="search-empty search-error">
                    Search failed. Please try again.
                </div>
            `;
            dropdown.style.display = "block";
        }
    }

    input.addEventListener("input", function () {
        const query = input.value.trim();

        clearTimeout(debounceTimer);

        if (query.length < 2) {
            hideDropdown();
            return;
        }

        debounceTimer = setTimeout(function () {
            performSearch(query);
        }, 300);
    });

    input.addEventListener("keyup", function () {
        const query = input.value.trim();

        clearTimeout(debounceTimer);

        if (query.length < 2) {
            hideDropdown();
            return;
        }

        debounceTimer = setTimeout(function () {
            performSearch(query);
        }, 300);
    });

    input.addEventListener("focus", function () {
        const query = input.value.trim();

        if (query.length >= 2 && dropdown.innerHTML.trim() !== "") {
            dropdown.style.display = "block";
        }
    });

    document.addEventListener("click", function (event) {
        if (!dropdown.contains(event.target) && event.target !== input) {
            dropdown.style.display = "none";
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            hideDropdown();
        }
    });
});