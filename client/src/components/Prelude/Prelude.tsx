import { ReactNode, useEffect } from "react";
import { Notifications } from "./Notifications";
import { useUser } from "@cafe/hooks/useUser";
import { LoadingBarContainer } from "react-top-loading-bar";
import { LoadingBar } from "./LoadingBar";

export function Prelude({ children }: { children: ReactNode }) {
  const user = useUser();
  const theme = user.authenticated ? user.theme_preference : "light";

  useEffect(() => {
    if (theme === "dark") {
      document.documentElement.setAttribute("data-theme", "dark");
    }
    if (theme === "light") {
      document.documentElement.removeAttribute("data-theme");
    }
    if (theme === "system") {
      const mql = window.matchMedia("(prefers-color-scheme: dark)");
      const systemThemeChangeHandler = (e: MediaQueryListEvent) => {
        if (e.matches) {
          document.documentElement.setAttribute("data-theme", "dark");
        } else {
          document.documentElement.removeAttribute("data-theme");
        }
      };
      if (mql.matches) {
        document.documentElement.setAttribute("data-theme", "dark");
      } else {
        document.documentElement.removeAttribute("data-theme");
      }
      mql.addEventListener("change", systemThemeChangeHandler);
      return () => {
        mql.removeEventListener("change", systemThemeChangeHandler);
      };
    }
  }, [theme]);

  return (
    <>
      <LoadingBarContainer>
        <LoadingBar />
        {children}
        <Notifications />
      </LoadingBarContainer>
    </>
  );
}
