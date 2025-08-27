function menuShow() {
    let menuMobile = document.querySelector('.mobile-menu');
    if (menuMobile.classList.contains('open')) {
        menuMobile.classList.remove('open');
        document.querySelector('.icon').src = "assets/img/menu_white_36dp.svg";
    } else {
        menuMobile.classList.add('open');
        document.querySelector('.icon').src = "assets/img/close_white_36dp.svg";
    }
}

document.addEventListener("DOMContentLoaded", function () {
    fetch("/grafico_produtos_json")
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById("graficoProdutos").getContext("2d");
            new Chart(ctx, {
                type: "bar",
                data: {
                    labels: data.categorias,
                    datasets: [{
                        label: "Quantidade em Estoque",
                        data: data.quantidades,
                        backgroundColor: "blue",
                    }]
                }
            });
        });
});

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    
    form.addEventListener("submit", function (event) {
        event.preventDefault();  // Impede a página de subir

        const query = document.querySelector("input[name='query']").value;
        const url = new URL(window.location.href);
        url.searchParams.set("query", query);
        history.pushState(null, "", url);  // Atualiza a URL sem recarregar a página

        fetch(url)  // Faz a busca sem recarregar
            .then(response => response.text())
            .then(html => {
                document.body.innerHTML = html;  // Atualiza a página com os novos resultados
            })
            .catch(error => console.error("Erro ao buscar produtos:", error));
    });
});

function resetSearch() {
    document.getElementById("searchInput").value = "";  // Limpa o campo de pesquisa

        // Remove o parâmetro "query" da URL
        const url = new URL(window.location.href);
        url.searchParams.delete("query");

        // Recarrega a página sem o filtro
        window.location.href = url.toString();
}

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".div_alterar_produto form"); // Seleciona o formulário de busca

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Impede o recarregamento da página

        const formData = new FormData(form);
        const url = new URL(form.action, window.location.origin);
        url.search = new URLSearchParams(formData).toString(); // Atualiza a URL com a pesquisa

        fetch(url)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, "text/html");
                const novaTabela = doc.querySelector(".div_alterar_produto");
                
                if (novaTabela) {
                    document.querySelector(".div_alterar_produto").innerHTML = novaTabela.innerHTML;
                }
            })
            .catch(error => console.error("Erro ao buscar produtos:", error));
    });
});