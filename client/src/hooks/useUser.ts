import React from "react";

type UnauthenticatedUser = {
    authenticated: false;
}

type AuthenticatedUser = {
    authenticated: true;
    id: string;
    displayName: string;
    avatarURL: string | null;
}

export type User = UnauthenticatedUser | AuthenticatedUser;

export const UserContext = React.createContext<User | null>(null);

export const useUser = () => {
    const user = React.useContext(UserContext);
    if (user === null) {
        throw new Error("User not found");
    }
    return user;
}

export const useLoggedInUser = () => {
    const user = useUser();
    if (!user.authenticated) {
        throw new Error("User is not authenticated");
    }
    return user;
}