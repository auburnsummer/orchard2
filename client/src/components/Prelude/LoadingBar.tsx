import { useTheme } from "@cafe/hooks/useTheme";
import { useCurrentRequestId, useIsLoading } from "@cafe/minibridge/hooks";
import { useState, useEffect } from "react";
import { useLoadingBar } from "react-top-loading-bar";

export function LoadingBar() {
  const pageLoading = useIsLoading();
  const currentRequestId = useCurrentRequestId();
  const [barStarted, setBarStarted] = useState(false);

  const theme = useTheme();

  const { start, complete } = useLoadingBar({ color: theme === "dark" ? "var(--color-blue-400)" : "var(--color-blue-500)", height: 2 });

  useEffect(() => {
    if (pageLoading && !barStarted) {
      setBarStarted(true);
      start("continuous");
    } else if (!pageLoading && barStarted) {
      setBarStarted(false);
      complete();
    }
  }, [pageLoading, barStarted]);

  useEffect(() => {
    if (barStarted) {
      // if the request id changes, we should restart the bar
      // because it means they clicked something else while the bar was still loading
      start("continuous");
    }
  }, [currentRequestId]);

  return null;
}
