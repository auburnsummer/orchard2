import { NavigationContext } from "@django-bridge/react"
import { useContext } from "react"

export function useNavigationContext() {
    return useContext(NavigationContext);
}