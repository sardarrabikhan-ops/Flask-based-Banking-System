import {
    initFirstNameValidation,
    initLastNameValidation,
    initEmailValidation,
    initPhoneValidation,
    initPasswordValidation,
    initConfirmPasswordValidation,
    initAmountValidation,
    initSignupFormValidation
} from "./forms.js";

import {
    initSidebar,
    initDropdown,
    initFlashMessages
} from "./ui.js";

initFirstNameValidation();
initLastNameValidation();
initEmailValidation();
initPhoneValidation();
initPasswordValidation();
initConfirmPasswordValidation();
initSignupFormValidation();

initAmountValidation();

initSidebar();
initDropdown();
initFlashMessages();