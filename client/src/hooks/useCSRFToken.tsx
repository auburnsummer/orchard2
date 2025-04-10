import React from "react";

export const CSRFTokenContext = React.createContext<string | null>(null);

export const useCSRFToken = () => {
    const csrfToken = React.useContext(CSRFTokenContext);
    if (csrfToken === null) {
        throw new Error("CSRF token not found");
    }
    return csrfToken;
}

export const useCSRFTokenInput = () => {
    const csrfToken = useCSRFToken();
    return <input type="hidden" name="csrfmiddlewaretoken" value={csrfToken} />;
}