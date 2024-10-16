console.log("register working");

const usernameField = document.querySelector('#usernameField')
const feedBackArea = document.querySelector('.invalid_feedback')
const emailField = document.querySelector('#emailField')
const emailFeedBackArea = document.querySelector('.emailFeedBackArea')
const showPasswordToggle = document.querySelector('.showPasswordToggle')
const passwordField = document.querySelector('#passwordField')
const submitBtn = document.querySelector(".submit-btn")

const handleToggleInput = (e) => {
    if (showPasswordToggle.textContent === "SHOW") {
        showPasswordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
    } else {
        showPasswordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
    }
};

// username Validation
usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;
    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display = 'none';

    if (usernameVal.length > 0) {
        fetch('/authentication/validate-username', {
            body: JSON.stringify({username: usernameVal}),
            method: "POST"
        })
            .then(res => res.json())
            .then(data => {
                if (data.username_error) {
                    submitBtn.disabled = true;
                    usernameField.classList.add("is-invalid");
                    feedBackArea.style.display = 'block';
                    feedBackArea.innerHTML = `<p>${data.username_error}</p>`
                }else{
                    submitBtn.removeAttribute('disabled')
                }
            });
    }
});

// email Validation
emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;
    emailField
        .classList
        .remove("is-invalid");
    emailFeedBackArea.style.display = 'none';

    if (emailVal.length > 0) {
        fetch('/authentication/validate-email', {
            body: JSON.stringify({email: emailVal}),
            method: "POST"
        })
            .then(res => res.json())
            .then(data => {
                console.log("data", data);
                if (data.email_error) {
                    submitBtn.disabled = true;
                    emailField.classList.add("is-invalid");
                    emailFeedBackArea.style.display = 'block';
                    emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`
                }else{
                    submitBtn.removeAttribute('disabled')
                }
            });
    }
});

// Show Password Toggle

showPasswordToggle.addEventListener("click", handleToggleInput);
