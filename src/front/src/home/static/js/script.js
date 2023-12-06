
isDarkMode = false;

function switchMode() {
    if (!isDarkMode) {
        document.querySelector("body").setAttribute("data-bs-theme", "dark");
        document.querySelector("#switch-btn").classList.remove("btn-outline-dark");
        document.querySelector("#switch-btn").setAttribute("class", "btn btn-outline-light")
        isDarkMode = true;
    }
    else {
        document.querySelector("body").setAttribute("data-bs-theme", "light");
        document.querySelector("#switch-btn").classList.remove("btn-outline-light");
        document.querySelector("#switch-btn").setAttribute("class", "btn btn-outline-dark")
        isDarkMode = false;
    }
}

async function loginRoute() {
    url = "http://127.0.0.1:8000/signup"
    try {
        const response = await fetch(url);

        if (!response.ok) {
          throw new Error('La requête a échoué');
        }

        const html = await response.text();
        console.log(html);
        document.open(); // Ouvre un nouveau document
        document.write(html); // Écrit le contenu HTML récupéré
        document.close(); // Ferme le document en cours de traitemen
        // const contenuDiv = document.getElementById('contenu');
        // contenuDiv.innerHTML = html; // Remplace le contenu de la div avec le HTML reçu
    } catch (error) {
        console.error('Erreur :', error);
    }
}
