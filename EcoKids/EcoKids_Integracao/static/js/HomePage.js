let avatarRequest = null; 


function carregarAvatar() {
    
    fetch('/get_avatar_url/')
    .then(response => response.json())
    .then(data => {
        
        if (data.user_avatar_url) {
            
            document.getElementById('avatar_image').src = staticUrl + data.user_avatar_url + '?t=' + new Date().getTime();

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
                window.location.reload();
            }
        })
        .catch(error => console.error('Erro:', error));
}

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("logout_button").addEventListener("click", logout);
});



document.addEventListener("DOMContentLoaded", carregarAvatar);


  