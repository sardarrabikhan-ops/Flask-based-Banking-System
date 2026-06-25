export const validateFirstName = (firstName) => {
    if (firstName.length < 3 || firstName.length > 15) return "First name must be 3-15 characters long!";
    if (!/^[a-zA-Z\s]+$/.test(firstName)) return "First name must contain only letters and spaces!";
    return "";
};

export const validateLastName = (lastName) => {
    if (lastName.length < 3 || lastName.length > 15) return "Last name must be 3-15 characters long!";
    if (!/^[a-zA-Z\s]+$/.test(lastName)) return "Last name must contain only letters and spaces!";
    return "";
};

export const validateEmail = (email) => {
    const pattern = /^[a-zA-Z0-9_.%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!pattern.test(email)) return "Please enter a valid email address!";
    return "";
};

export const validatePhone = (phone) => {
    if (!/^\+92\d{10}$/.test(phone)) return "Please enter a valid Pakistani phone number in +92XXXXXXXXXX format.";
    return "";
};

const ALLOWED_SPECIALS = new Set("!@#$%^&*()-_=+");

export const validatePassword = (value) => {

    if (value.length < 8 || value.length > 18) return "Password must be 8-18 characters long!";
    if (![...value].some(char => ALLOWED_SPECIALS.has(char))) return "Password must include at least one special character!";
    if (!/\d/.test(value)) return "Password must include at least one number!";
    if (!/[a-zA-Z]/.test(value)) return "Password must include at least one letter!";
    return "";
};

export const validateConfirmPassword = (passwordVal, confirmPasswordVal) => {
    if (passwordVal === confirmPasswordVal) return "";
    return "Passwords do not match!";
};

export const validateAmount = (value) => {
    value = Number(value);

    if (Number.isNaN(value)) return "Please enter a valid number.";
    if (value <= 0) return "Amount must be more than zero.";
    return "";
};

export const isSignupFormValid = (
    firstNameVal,
    lastNameVal,
    emailVal,
    phoneVal,
    passwordVal,
    confirmPasswordVal
) => {

    const firstNameError =
        validateFirstName(firstNameVal);

    const lastNameError =
        validateLastName(lastNameVal);

    const passwordError =
        validatePassword(passwordVal);

    const emailError =
        validateEmail(emailVal);

    const phoneError =
        validatePhone(phoneVal);

    const confirmPasswordError =
        validateConfirmPassword(
            passwordVal,
            confirmPasswordVal
        );

    return {
        firstNameError,
        lastNameError,
        emailError,
        phoneError,
        passwordError,
        confirmPasswordError,
        isValid:
            !firstNameError &&
            !lastNameError &&
            !emailError &&
            !phoneError &&
            !passwordError &&
            !confirmPasswordError
    };
};