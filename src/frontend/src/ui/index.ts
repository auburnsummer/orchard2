// for now just re-rexport shoelace components.
// if I need to I can add my own UI elements later.
// this is mostly for aesthetical reasons of being able to import from @orchard/ui lol

import SlSpinner from "@shoelace-style/shoelace/dist/react/spinner/index.js";
import SlButton from "@shoelace-style/shoelace/dist/react/button/index.js";
import SlIcon from "@shoelace-style/shoelace/dist/react/icon/index.js";
import SlSkeleton from "@shoelace-style/shoelace/dist/react/skeleton/index.js";
import SlAvatar from "@shoelace-style/shoelace/dist/react/avatar/index.js";
import SlDropdown from "@shoelace-style/shoelace/dist/react/dropdown/index.js";
import SlMenu from "@shoelace-style/shoelace/dist/react/menu/index.js";
import SlMenuItem from "@shoelace-style/shoelace/dist/react/menu-item/index.js";
import SlMenuLabel from "@shoelace-style/shoelace/dist/react/menu-label/index.js";
import SlDivider from "@shoelace-style/shoelace/dist/react/divider/index.js";

export const Spinner = SlSpinner;
export const Button = SlButton;
export const Icon = SlIcon;
export const Skeleton = SlSkeleton;
export const Avatar = SlAvatar;
export const Dropdown = SlDropdown;
export const Menu = SlMenu;
export const MenuItem = SlMenuItem;
export const MenuLabel = SlMenuLabel;
export const Divider = SlDivider;