function carregarAvatar() {
    
    fetch('/get_avatar_url/')
    .then(response => response.json())
    .then(data => {
        
        if (data.user_avatar_url) {
            
            document.getElementById('avatar_image').src = staticUrl + data.user_avatar_url;

        } else {
            
            document.getElementById('avatar_image').src = staticUrl + 'img/avatar-default.avif';
        }
    })
    .catch(error => console.log('Erro:', error));
}



function logout() {
    
    if (avatarRequest) {
        avatarRequest.abort();
    }
    
    
    fetch('/logout/')
        .then(response => response.json())
        .then(data => {
            
            if (data.logout) {
                
                window.location.href = '/'; 
            }
        })
        .catch(error => console.error('Erro:', error));
}

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("logout_button").addEventListener("click", logout);
});

document.addEventListener("DOMContentLoaded", carregarAvatar);



document.addEventListener("DOMContentLoaded", function () {
    const formulario = document.getElementById("formulario-de-comentarios");
    const todosComentarios = document.getElementById("todos-os-comentarios");

});


document.addEventListener("DOMContentLoaded", function () {
    const formulario = document.getElementById("formulario-de-comentarios");
    const todosComentarios = document.getElementById("todos-os-comentarios");
    const mensagemInvalida = document.getElementById("mensagem-invalida");

    let palavrasSujas = ["palavra1", "palavra2", "palavra3"];

    
    fetch('/AdicionarComentario/')
        .then(response => response.json())
        .then(data => {
            
            if (Array.isArray(data) && data.length > 0) {
                
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
            
            inputTitulo.value = "";
            inputForm.value = "";
        } else if (contemPalavraSujaTitulo) {
            mensagemInvalida.textContent = "O título contém palavras inapropriadas.";
            mensagemInvalida.classList.add("texto-invalido");
           
            inputTitulo.value = "";
        } else if (contemPalavraSujaComentario) {
            mensagemInvalida.textContent = "O comentário contém palavras inapropriadas.";
            mensagemInvalida.classList.add("texto-invalido");
           
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

            
            submitComment(titulo, mensagem);
        }
    });

    
    function submitComment(titulo, comentario) {
        
        var csrftoken = getCookie('csrftoken');

        
        var xhr = new XMLHttpRequest();

        
        xhr.open("POST", "/AdicionarComentario/", true);

        
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);

        
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    alert('Comentário enviado com sucesso!');
                    location.reload();
                } else if (xhr.status === 401) {
                    
                    alert("Credenciais inválidas. Por favor, tente novamente.");
                }
            }
        };

        
        xhr.send(JSON.stringify({ titulo: titulo, comentario: comentario }));
    }

    
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
