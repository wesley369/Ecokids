function onChangeEmail() {
    toggleButtonsDisable();
    toggleEmailErrors();
}

function onChangePassword() {
    toggleButtonsDisable();
    togglePasswordErrors();
}

function isEmailValid() {
    const email = form.email().value;
    if (!email) {
        return false;
    }
    return validateEmail(email);
}

function toggleEmailErrors() {
    const email = form.email().value;
    form.emailRequiredError().style.display = email ? "none" : "block";

    form.emailInvalidError().style.display = validateEmail(email) ? "none" : "block";
}

function togglePasswordErrors() {
    const password = form.password().value;

    form.passwordRequiredError().style.display = password ? "none" : "block";
}

function toggleButtonsDisable() { 
    const emailValid = isEmailValid();
    form.recoverPassword().disabled = !emailValid;

    const passwordValid = isPasswordValid();
    form.loginButton().disabled = !emailValid || !passwordValid;
}

function isPasswordValid() {
    const password = form.password().value;
    if (!password) {
        return false;
    }
    return true;
}

const form = {
    email: () => document.getElementById('email'),
    emailInvalidError: () => document.getElementById('email-invalid-error'),
    emailRequiredError: () => document.getElementById('email-required-error'),
    loginButton: () => document.getElementById('login-button'),
    password: () => document.getElementById('password'),
    passwordRequiredError: () => document.getElementById('password-required-error'),
    recoverPassword: () => document.getElementById('recover-password-button')
}

const Login_btn = document.querySelector("#Login-btn");
const Inscrever_se_btn = document.querySelector("#Inscrever-se-btn");
const container = document.querySelector(".container");

Inscrever_se_btn.addEventListener('click', () => {
    container.classList.add("Inscrever-se-mode");
});

Login_btn.addEventListener('click', () => {
    container.classList.remove("Inscrever-se-mode");
});

//function login() {
    //window.location.href = "/home.html";
//}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
          
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function login() {
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;


    if (!email || !password) {
        alert("Por favor, preencha todos os campos.");
        return; 
    }

    var csrftoken = getCookie('csrftoken');

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/login2/", true); 
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                
                var homepageUrl = document.getElementById("login-button").getAttribute("data-homepage-url");
                window.location.href = homepageUrl;
            } else if (xhr.status === 401) {
                
                alert("Credenciais inválidas. Por favor, tente novamente.");
            }
        }
    };
    xhr.send(JSON.stringify({ email: email, password: password }));
}


document.getElementById("btn").addEventListener("click", function(event) {
    event.preventDefault(); // Evita o envio padrão do formulário
    
    // Obter o token CSRF do cookie
    var csrftoken = getCookie('csrftoken');

    // Coletar os valores do formulário
    var nome = document.getElementById("nome").value;
    var email = document.getElementById("email2").value;
    var senha = document.getElementById("senha2").value;

    // Criar um objeto FormData e adicionar os valores do formulário
    var formData = new FormData();
    formData.append("nome", nome);
    formData.append("email", email);
    formData.append("senha", senha);
    
    // Envie a solicitação para o endpoint de registro (signup), incluindo o token CSRF
    fetch('/signup/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Exibe a mensagem de resposta do servidor
        if (data.success) {
            // Redireciona para a página inicial
            window.location.href = '/Personagem'; // Redireciona para a HomePage.html
        }
    })
    .catch(error => {
        console.error('Erro ao enviar solicitação:', error);
    });
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
          
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

