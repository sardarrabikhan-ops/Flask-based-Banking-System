const sidebar = document.querySelector(".sidebar");
const menuBtn = document.querySelector("#menubtn");
const closeBtn = document.querySelector("#closebtn");

if (sidebar && menuBtn && closeBtn) {
    menuBtn.addEventListener("click", () => {
        sidebar.classList.add("active");
    });

    closeBtn.addEventListener("click", () => {
        sidebar.classList.remove("active");
    });
}


const userBtn = document.querySelector("#userbtn");
const menu = document.querySelector(".dropdown-menu");

if (userBtn && menu) {
    userBtn.addEventListener("click", () => {
        menu.classList.toggle("active");
    });
}


const validPassword = (password) => {
    let allowed = "!@#$%^&*()-_=+".split("");
    let passArr = password.value.split("");

    if (!(passArr.length > 8 && passArr.length < 18)) {
        passwordError.innerText = "Password must be 8-18 characters long!";
    } else if (!passArr.some(char => allowed.includes(char))) {
        passwordError.innerText = "Password must include at least one special character!";
    } else {
        passwordError.innerText = "";
    }
}


const password = document.querySelector("#password");
const passwordError = document.querySelector("#pass-error");

if (password) {
    password.addEventListener("input", () => {
        validPassword(password);
    });
}

const validConfirmPassword = (password, confirmPassword) => {
    if (password.value !== confirmPassword.value) {
        conPssError.innerText = "Passwords do not match!";
    } else {
        conPssError.innerText = "";
    }
}

const conPass = document.querySelector("#confirm-password");
const conPssError = document.querySelector("#con-pass-error");

if (password && conPass) {
    conPass.addEventListener("input", () => {
        validConfirmPassword(password, conPass);
    });
}

const flashMsgs = document.querySelectorAll(".flash-msg");

flashMsgs.forEach((flashMsg) => {
    if (flashMsg.innerText) {
        flashMsg.classList.add("active");
    };
});

const crosses = document.querySelectorAll(".cross");
crosses.forEach((cross) => {
    cross.addEventListener("click", () => {
        cross.parentElement.classList.remove("active");
    });
});


const amounts = document.querySelectorAll(".amount");

amounts.forEach(amount => {
    amount.addEventListener("input", () => {
        const value = Number(amount.value);

        const error = amount.parentElement.querySelector(".amount-error");

        if (Number.isNaN(value)) {
            error.innerText = "Please enter a valid number.";
        }
        else if (value <= 0) {
            error.innerText = "Amount must be more than zero.";
        }
        else {
            error.innerText = "";
        }
    });
});