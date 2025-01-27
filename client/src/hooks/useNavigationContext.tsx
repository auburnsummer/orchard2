import { NavigationContext } from "@django-bridge/react"
import { useContext } from "react"

export function useNavigationContext() {
    return useContext(NavigationContext);
}

export function usePathName() { 
    const { path } = useNavigationContext();
    return new URL(path, window.location.origin).pathname;
}

export function useSearchParams() {
    const { path } = useNavigationContext();
    return new URL(path, window.location.origin).searchParams;
}