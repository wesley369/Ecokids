document.addEventListener("DOMContentLoaded", function () {
    const formulario = document.getElementById("formulario-de-comentarios");
    const todosComentarios = document.getElementById("todos-os-comentarios");
    const mensagemInvalida = document.getElementById("mensagem-invalida");

    let palavrasSujas = ["palavra1", "palavra2", "palavra3"];

    // Função para carregar os últimos 10 comentários
    fetch('/AdicionarComentario/')
        .then(response => response.json())
        .then(data => {
            // Verificar se os dados recebidos são válidos
            if (Array.isArray(data) && data.length > 0) {
                // Processar os comentários recebidos
                data.forEach(comentario => {

                    const novoComentario = document.createElement("div");
                    novoComentario.classList.add("comentario");

                    const tituloElemento = document.createElement("h3");
                    tituloElemento.textContent = comentario.titulo;

                    const conteudoElemento = document.createElement("p");
                    conteudoElemento.textContent = comentario.comentario;

                    const dataHoraElemento = document.createElement("span");
                    dataHoraElemento.textContent = new Date(comentario.data_hora).toLocaleString();

                    novoComentario.appendChild(tituloElemento);
                    novoComentario.appendChild(conteudoElemento);
                    novoComentario.appendChild(dataHoraElemento);

                    // Adicionar o comentário à lista de comentários na página
                    todosComentarios.appendChild(novoComentario);
                });
            } else {
                console.error('Os dados recebidos não estão no formato esperado:', data);
            }
        })
        .catch(error => {
            console.error('Erro ao carregar comentários:', error);
        });

    formulario.addEventListener("submit", function (evento) {
        evento.preventDefault();

        const inputTitulo = document.getElementById("input-titulo");
        const inputForm = document.getElementById("input-formulario");
        const titulo = inputTitulo.value;
        const mensagem = inputForm.value;

        // Verificação de palavras sujas
        const contemPalavraSujaTitulo = palavrasSujas.some(palavra => titulo.toLowerCase().includes(palavra));
        const contemPalavraSujaComentario = palavrasSujas.some(palavra => mensagem.toLowerCase().includes(palavra));

        if (mensagem.trim() === "" || titulo.trim() === "") {
            inputForm.classList.add("comentario-invalido");
            inputTitulo.classList.add("comentario-invalido");
            mensagemInvalida.textContent = "Por favor, insira um título e um comentário";
            mensagemInvalida.classList.add("texto-invalido");
        } else if (contemPalavraSujaTitulo && contemPalavraSujaComentario) {
            mensagemInvalida.textContent = "O título e o comentário contêm palavras inapropriadas.";
            mensagemInvalida.classList.add("texto-invalido");
            // Limpar ambos os campos se palavras sujas forem detectadas em ambos
            inputTitulo.value = "";
            inputForm.value = "";
        } else if (contemPalavraSujaTitulo) {
            mensagemInvalida.textContent = "O título contém palavras inapropriadas.";
            mensagemInvalida.classList.add("texto-invalido");
            // Limpar apenas o campo do título se uma palavra suja for detectada nele
            inputTitulo.value = "";
        } else if (contemPalavraSujaComentario) {
            mensagemInvalida.textContent = "O comentário contém palavras inapropriadas.";
            mensagemInvalida.classList.add("texto-invalido");
            // Limpar apenas o campo do comentário se uma palavra suja for detectada nele
            inputForm.value = "";
        } else {
            mensagemInvalida.textContent = "";
            const novoComentario = document.createElement("div");
            novoComentario.classList.add("comentario");

            const tituloElemento = document.createElement("h3");
            tituloElemento.textContent = titulo;

            const conteudoElemento = document.createElement("p");
            conteudoElemento.textContent = mensagem;

            novoComentario.appendChild(tituloElemento);
            novoComentario.appendChild(conteudoElemento);

            todosComentarios.appendChild(novoComentario);

            inputForm.classList.remove("comentario-invalido");
            inputTitulo.classList.remove("comentario-invalido");
            formulario.reset();

            // Enviar os dados do formulário para a view do Django usando fetch
            submitComment(titulo, mensagem);
        }
    });

    // Função para enviar o comentário para a view do Django usando fetch
    function submitComment(titulo, comentario) {
        // Obter o token CSRF do cookie
        var csrftoken = getCookie('csrftoken');

        // Criar uma nova instância de XMLHttpRequest
        var xhr = new XMLHttpRequest();

        // Definir a URL e o método HTTP
        xhr.open("POST", "/AdicionarComentario/", true);

        // Definir os cabeçalhos da requisição
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);

        // Definir o manipulador de eventos para a mudança de estado da requisição
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    alert('Comentário enviado com sucesso!');
                    location.reload();
                } else if (xhr.status === 401) {
                    // Exibir alerta em caso de credenciais inválidas
                    alert("Credenciais inválidas. Por favor, tente novamente.");
                }
            }
        };

        // Enviar os dados do formulário no formato JSON
        xhr.send(JSON.stringify({ titulo: titulo, comentario: comentario }));
    }

    // Função para obter o token CSRF do cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }



});

function carregarAvatar() {
    // Verifica se o usuário está logado antes de carregar o avatar
    fetch('/get_avatar_url/')
    .then(response => response.json())
    .then(data => {
        // Verifica se o usuário está logado
        if (data.user_avatar_url) {
            // Atualiza a URL do avatar na imagem
            document.getElementById('avatar_image').src = staticUrl + data.user_avatar_url;
        } else {
            // Caso o usuário não esteja logado, define a URL do avatar padrão
            document.getElementById('avatar_image').src = staticUrl + 'img/avatar-rafael.png'; 
        }
    })
    .catch(error => console.log('Erro:', error));
}


// Chama a função para carregar o avatar assim que o DOM estiver pronto
document.addEventListener("DOMContentLoaded", carregarAvatar);