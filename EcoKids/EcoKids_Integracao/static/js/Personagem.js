document.addEventListener("DOMContentLoaded", function() {
    var avatarImages = document.querySelectorAll('.center .carrousel-itens img');
    avatarImages.forEach(function(img) {
        img.addEventListener('click', function() {
            avatarImages.forEach(function(img) {
                img.classList.remove('selected');
            });
            this.classList.add('selected');
        });
    });

    
    document.querySelector('.botao button').addEventListener('click', function(e) {
        e.preventDefault();
        
        var selectedAvatar = document.querySelector('.center .carrousel-itens img.selected');
        if (!selectedAvatar) {
            alert('Por favor, selecione um avatar antes de enviar o formulário.');
            return; 
        }

        
        var avatarId = selectedAvatar.getAttribute('id');
        
        
        var nomePersonagem = document.querySelector('input[name="nome_personagem"]').value;


        if (nomePersonagem.trim() === "") {
            alert('Por favor, insira um nome para o seu personagem.');
            return; 
        }
        
        
        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        
        
        var formData = new FormData();
        formData.append('csrfmiddlewaretoken', csrfToken);
        formData.append('avatar_id', avatarId);
        formData.append('nome_personagem', nomePersonagem);
        
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/Personagem/', true);
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
        xhr.onload = function() {
            if (xhr.status === 200) {
                try {
                    var responseData = JSON.parse(xhr.responseText);
                    if (responseData.avatar_url) {
                        var avatarUrl = responseData.avatar_url;
                        document.getElementById('avatar_image').src = staticUrl + avatarUrl;
                        window.location.href = '/'; 
                    } else {
                        console.log('Resposta inválida: não há URL do avatar');
                    }
                } catch (error) {
                    console.log('Erro ao analisar resposta JSON:', error);
                }
            } else {
                console.log('Erro:', xhr.statusText);
            }
        };
        
        xhr.onerror = function() {
            console.log('Erro de rede');
        };
        xhr.send(formData);
    });
});
