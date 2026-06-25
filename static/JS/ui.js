import { DOM } from "./dom.js";

export const initSidebar = () => {
    if (!DOM.sidebar || !DOM.menuBtn || !DOM.closeBtn) return;

    DOM.menuBtn.addEventListener("click", () => {
        DOM.sidebar.classList.toggle("active");
    });

    DOM.closeBtn.addEventListener("click", () => {
        DOM.sidebar.classList.remove("active");
    });
};


export const initDropdown = () => {
    if (!DOM.userBtn || !DOM.dropdownMenu) return;

    DOM.userBtn.addEventListener("click", () => {
        DOM.dropdownMenu.classList.toggle("active");
    });
};

export const initFlashMessages = () => {
    DOM.crosses.forEach((cross) => {
        cross.addEventListener("click", () => {
            cross.closest(".flash-msg").remove();
        });
    });
};