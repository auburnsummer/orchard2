
export function useTheme() {
    const theme = document.documentElement.getAttribute("data-theme");
    if (theme === "dark") {
        return "dark";
    } else {
        return "light";
    }
}