import { ShellDramaticCenter } from "@cafe/components/ShellDramaticCenter";
import { navigateAtom } from "@cafe/minibridge/atoms";
import { djangoGet } from "@cafe/minibridge/fetch";
import { RDLevelPrefill } from "@cafe/types/rdLevelPrefill";
import { useSetAtom } from "jotai";
import { useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCircleNotch } from "@fortawesome/free-solid-svg-icons";
import { Words } from "@cafe/components/ui/Words";
import { Alert } from "@cafe/components/ui/Alert";

type PrefillLoadingProps = {
  error: string;
  prefillType: "update" | "new";
};

export function PrefillLoading({ error, prefillType }: PrefillLoadingProps) {
  const navigate = useSetAtom(navigateAtom);

  useEffect(() => {
    const interval = setInterval(async () => {
      if (error !== "") {
        return;
      }
      const url = `${window.location.origin}${window.location.pathname}?_cache=${Math.random()}`;
      const resp = await djangoGet(url);
      if (resp.action === "render") {
        const props = resp.props.prefill as RDLevelPrefill;
        if (props.ready || props.errors) {
          clearInterval(interval);
          navigate(new URL(window.location.href), true);
        }
      }
    }, 500);
    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    <ShellDramaticCenter>
      {error === "" ? (
        <div className="flex flex-col items-center gap-4">
          <FontAwesomeIcon icon={faCircleNotch} className="animate-spin text-violet-700 dark:text-violet-300" size="2x"/>
          {prefillType === "update" ? (
            <Words>Uploading level...</Words>
          ) : (
            <Words>Analysing level...</Words>
          )}
        </div>
      ) : (
        <div className="flex flex-col gap-4">
          <Words>An error occurred while attempting to load this level:</Words>
          <Alert
            variant="error"
          >
            <pre>{error}</pre>
          </Alert>
          <Words>
            Please try the command again. If it still doesn't work, let Auburn
            know, thanks
          </Words>
        </div>
      )}
    </ShellDramaticCenter>
  );
}
