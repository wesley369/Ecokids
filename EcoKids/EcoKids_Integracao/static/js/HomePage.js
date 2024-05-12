let avatarRequest = null; 


function carregarAvatar() {
    
    fetch('/get_avatar_url/')
    .then(response => response.json())
    .then(data => {
        
        if (data.user_avatar_url) {
            
            document.getElementById('avatar_image').src = staticUrl + data.user_avatar_url;
        } else {
            
            document.getElementById('avatar_image').src = staticUrl + 'img/avatar-rafael.png'; 
        }
    })
    .catch(error => console.log('Erro:', error));
}



document.addEventListener("DOMContentLoaded", carregarAvatar);


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
