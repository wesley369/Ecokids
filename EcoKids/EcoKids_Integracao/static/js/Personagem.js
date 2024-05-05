document.addEventListener("DOMContentLoaded", function() {
    // Adiciona ou remove a classe 'selected' quando uma imagem é clicada
    var avatarImages = document.querySelectorAll('.center .carrousel-itens img');
    avatarImages.forEach(function(img) {
        img.addEventListener('click', function() {
            // Remove a classe 'selected' de todas as imagens
            avatarImages.forEach(function(img) {
                img.classList.remove('selected');
            });
            // Adiciona a classe 'selected' à imagem clicada
            this.classList.add('selected');
        });
    });

    // Event listener para o clique no botão de envio do formulário
    document.querySelector('.botao button').addEventListener('click', function(e) {
        e.preventDefault(); // Impede o envio padrão do formulário
        
        // Verifica se algum avatar está selecionado
        var selectedAvatar = document.querySelector('.center .carrousel-itens img.selected');
        if (!selectedAvatar) {
            // Mostra uma mensagem de alerta ao usuário
            alert('Por favor, selecione um avatar antes de enviar o formulário.');
            return; // Impede o envio do formulário se nenhum avatar estiver selecionado
        }

        // Obtém o ID do avatar selecionado
        var avatarId = selectedAvatar.getAttribute('id');
        
        // Obtém o nome do personagem
        var nomePersonagem = document.querySelector('input[name="nome_personagem"]').value;

        // Verifica se o nome do personagem está vazio
        if (nomePersonagem.trim() === "") {
            // Mostra uma mensagem de alerta ao usuário
            alert('Por favor, insira um nome para o seu personagem.');
            return; // Impede o envio do formulário se o nome do personagem estiver vazio
        }
        
        // Obtém o token CSRF
        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        
        // Envia os dados para o servidor usando AJAX
        var formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrfToken);
        formData.append('avatar_id', avatarId);
        formData.append('nome_personagem', nomePersonagem);
        
        // Enviar os dados usando AJAX
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/Personagem/', true);
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
        xhr.onload = function() {
            if (xhr.status === 200) {
                try {
                    // Tenta analisar a resposta como JSON
                    var responseData = JSON.parse(xhr.responseText);
                    // Verifica se a resposta contém a URL do avatar
                    if (responseData.avatar_url) {
                        // Atualiza o avatar no template
                        var avatarUrl = responseData.avatar_url;
                        //document.getElementById('avatar_url_placeholder').innerText = 'A URL do avatar é: ' + avatarUrl;
                        document.getElementById('avatar_image').src = staticUrl + avatarUrl;
                        // Redireciona para a página inicial após o envio do formulário
                        window.location.href = '/'; // Redireciona para a página de Personagem
                    } else {
                        console.log('Resposta inválida: não há URL do avatar');
                    }
                } catch (error) {
                    console.log('Erro ao analisar resposta JSON:', error);
                }
            } else {
                // Manipula erros de requisição, se necessário
                console.log('Erro:', xhr.statusText);
            }
        };
        
        xhr.onerror = function() {
            // Manipula erros de requisição, se necessário
            console.log('Erro de rede');
        };
        xhr.send(formData);
    });
});
