import React from "react";

type ThemePreference = "light" | "dark" | "system";

type SearchDefaultPeerReviewPreference = "approved" | "pending" | "rejected" | "all";

type CommonUserFields = {
  theme_preference: ThemePreference;
  default_pr_preference: SearchDefaultPeerReviewPreference;
  show_rddirect: boolean;
};

export type UnauthenticatedUser = {
  authenticated: false;
} & CommonUserFields;

export type AuthenticatedUser = {
  authenticated: true;
  id: string;
  displayName: string;
  avatarURL: string | null;
  is_superuser: boolean;
  is_peer_reviewer: boolean;
} & CommonUserFields;

export type User = UnauthenticatedUser | AuthenticatedUser;

export const UserContext = React.createContext<User | null>(null);

export const useUser = () => {
  const user = React.useContext(UserContext);
  if (user === null) {
    throw new Error("User not found");
  }
  return user;
};

export const useLoggedInUser = () => {
  const user = useUser();
  if (!user.authenticated) {
    throw new Error("User is not authenticated");
  }
  return user;
};
