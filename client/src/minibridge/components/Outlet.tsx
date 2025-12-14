import { useAtomValue } from "jotai";
import { configAtom, currentRenderAtom, isLoadingAtom } from "../atoms";
import { Suspense, useState, useTransition, useEffect } from "react";

export function Outlet() {
  const currentRender = useAtomValue(currentRenderAtom);
  const config = useAtomValue(configAtom);
  const isLoading = useAtomValue(isLoadingAtom);
  const [isPending, startTransition] = useTransition();
  const [displayRender, setDisplayRender] = useState(currentRender);

  useEffect(() => {
    if (currentRender) {
      startTransition(() => {
        setDisplayRender(currentRender);
      });
    }
  }, [currentRender]);

  if (!displayRender || !config) {
    return <></>;
  }
  const View = config.views[displayRender.view];
  if (!View) {
    return <p>Unknown view &apos;{displayRender.view}&apos;</p>;
  }

  return (
    <div style={{ position: "relative" }}>
      {(isLoading || isPending) && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            height: "3px",
            background: "linear-gradient(90deg, transparent, #3b82f6, transparent)",
            animation: "shimmer 1.5s infinite",
            zIndex: 9999,
          }}
        />
      )}
      <Suspense fallback={null}>
        <View {...displayRender.props} />
      </Suspense>
    </div>
  );
}
