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

document.addEventListener("DOMContentLoaded", carregarAvatar);


document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('.checkbox-item input[type="checkbox"]');
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (!user_id) {
                alert("Por favor, faça login para marcar tarefas.");
                this.checked = !this.checked;  // Desfazer a alteração
                return;
            }
            const tarefaId = this.id.split('_')[1];
            fetch(`/marcar-tarefa-realizada/${tarefaId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            }).then(response => response.json()).then(data => {
                if (data.success) {
                    console.log('Tarefa marcada como realizada');
                } else {
                    console.error('Erro ao marcar tarefa');
                }
            });
        });
    });

    iniciarContador();
});

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

function iniciarContador() {
    fetch('/get_tempo_restante/')
        .then(response => response.json())
        .then(data => {
            if (data.tempo_restante) {
                let tempo_restante = data.tempo_restante;

                const intervalo = setInterval(() => {
                    if (tempo_restante <= 0) {
                        clearInterval(intervalo);
                        location.reload();
                    } else {
                        tempo_restante--;
                        const horas = Math.floor(tempo_restante / 3600);
                        const minutos = Math.floor((tempo_restante % 3600) / 60);
                        const segundos = tempo_restante % 60;

                        document.getElementById('tempo_restante').textContent =
                            `${horas}h ${minutos}m ${segundos}s`;
                    }
                }, 1000);
            }
        });
}
