let avatarRequest = null; // Variável para armazenar a requisição do avatar

// Função para carregar o avatar do usuário
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

// Função para efetuar o logout do usuário
function logout() {
    // Cancela a requisição do avatar, se estiver pendente
    if (avatarRequest) {
        avatarRequest.abort();
    }
    
    // Envia uma requisição para a view de logout
    fetch('/logout/')
        .then(response => response.json())
        .then(data => {
            // Verifica se o logout foi bem-sucedido
            if (data.logout) {
                // Redireciona para a página inicial se o logout for bem-sucedido
                window.location.href = '/'; // Altere o caminho conforme necessário
            }
        })
        .catch(error => console.error('Erro:', error));
}
