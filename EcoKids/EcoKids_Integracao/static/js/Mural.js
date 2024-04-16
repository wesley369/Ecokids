let formulario = document.getElementById("formulario-de-comentarios")
let todosComentarios = document.getElementById("todos-os-comentarios")
let mensagemInvalida = document.getElementById("mensagem-invalida")

formulario.addEventListener("submit", function(evento){
    //preventDefault() - previne ações default do submit (que é um evento) que é recarregar a página
    evento.preventDefault()

    let inputForm = document.getElementById("input-formulario")
    let mensagem = inputForm.value // pegar valor do input
    
    if (mensagem.trim() === ""){
        // metrodo.trim() serve para remover todo o espaço das pontas anterior e posterior da frase
        inputForm.classList.add("comentario-invalido")
        mensagemInvalida.textContent = "Por favor, insira um comentário"
        mensagemInvalida.classList.add("texto-invalido")
    } else {
        mensagemInvalida.textContent = ""
        let comentarios = document.createElement("p")
        comentarios.textContent = mensagem        
        todosComentarios.appendChild(comentarios)    
        comentarios.classList.add("comentario")    
        formulario.reset() 
        // resetar o formulario - resetar o input ao estado inicial        
    }
})