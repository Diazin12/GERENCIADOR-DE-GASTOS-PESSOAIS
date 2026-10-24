const signupForm = document.getElementById("formCadastro");

if (signupForm) {
    const password = document.getElementById("senha");
    const confirmation = document.getElementById("confirmar-senha");

    function validatePasswords() {
        if (confirmation.value && confirmation.value !== password.value) {
            confirmation.setCustomValidity("As senhas não são iguais.");
        } else {
            confirmation.setCustomValidity("");
        }
    }

    password.addEventListener("input", validatePasswords);
    confirmation.addEventListener("input", validatePasswords);
    signupForm.addEventListener("submit", validatePasswords);
}
