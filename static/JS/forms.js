import {
    validateFirstName,
    validateLastName,
    validateEmail,
    validatePassword,
    validateConfirmPassword,
    validateAmount,
    isSignupFormValid,
    validatePhone
} from "./validators.js";

import { DOM } from "./dom.js";

export const updateConfirmPasswordError = () => {
    if (
        !DOM.password ||
        !DOM.confirmPassword ||
        !DOM.confirmPasswordError
    ) return;

    DOM.confirmPasswordError.innerText =
        validateConfirmPassword(
            DOM.password.value,
            DOM.confirmPassword.value
        )
};

export const initFirstNameValidation = () => {
    if (!DOM.firstName || !DOM.firstNameError) return;

    DOM.firstName.addEventListener("input", () => {
        DOM.firstNameError.innerText =
            validateFirstName(DOM.firstName.value);
    });
};

export const initLastNameValidation = () => {
    if (!DOM.lastName || !DOM.lastNameError) return;

    DOM.lastName.addEventListener("input", () => {
        DOM.lastNameError.innerText =
            validateLastName(DOM.lastName.value);
    });
};

export const initEmailValidation = () => {
    if (!DOM.email || !DOM.emailError) return;

    DOM.email.addEventListener("input", () => {
        DOM.emailError.innerText =
            validateEmail(DOM.email.value);
    });
};

export const initPhoneValidation = () => {
    if (!DOM.phone || !DOM.phoneError) return;

    DOM.phone.addEventListener("input", () => {
        DOM.phoneError.innerText =
            validatePhone(DOM.phone.value);
    });
};

export const initPasswordValidation = () => {
    if (!DOM.password || !DOM.passwordError) return;

    DOM.password.addEventListener("input", () => {
        updateConfirmPasswordError();
        DOM.passwordError.innerText =
            validatePassword(DOM.password.value);
    });
};


export const initConfirmPasswordValidation = () => {
    if (
        !DOM.password ||
        !DOM.confirmPassword ||
        !DOM.confirmPasswordError
    ) return;

    DOM.confirmPassword.addEventListener("input", updateConfirmPasswordError);
};


export const initAmountValidation = () => {
    DOM.amounts.forEach(amount => {
        const error = amount.parentElement.querySelector(".amount-error");

        amount.addEventListener("input", () => {
            error.innerText = validateAmount(amount.value);
        });
    });
};

export const initSignupFormValidation = () => {
    if (!DOM.signupForm) return;

    DOM.signupForm.addEventListener("submit", (event) => {
        const result = isSignupFormValid(
            DOM.firstName.value,
            DOM.lastName.value,
            DOM.email.value,
            DOM.phone.value,
            DOM.password.value,
            DOM.confirmPassword.value
        );

        if (!result.isValid) {
            event.preventDefault();
            DOM.signupBtn.disabled = true;
            DOM.firstNameError.innerText = result.firstNameError;
            DOM.lastNameError.innerText = result.lastNameError;
            DOM.emailError.innerText = result.emailError;
            DOM.phoneError.innerText = result.phoneError;
            DOM.confirmPasswordError.innerText = result.confirmPasswordError;
            DOM.passwordError.innerText = result.passwordError;
        };
    });
};