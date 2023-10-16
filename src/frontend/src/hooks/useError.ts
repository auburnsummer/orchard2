import { HTTPError } from "ky";
import { useErrorBoundary } from "preact/hooks";

const UNKNOWN_ERROR = "An unknown mysterious error. You should never see this, if you see this, ping auburn!";

// export function useErrorBoundaryMessage() {
//     const [error] = useErrorBoundary();

//     if (error === undefined) {
//         return [false, ""];
//     }

//     if (!(error instanceof Error)) {
//         return [true, UNKNOWN_ERROR];
//     }

//     if (error instanceof HTTPError) {
//         const resp = 
//     }

//     return [true, error.message];

// }