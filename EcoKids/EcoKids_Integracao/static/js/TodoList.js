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


