import { useSetAtom } from "jotai";
import { navigateAtom } from "../atoms";

function makeCanonicalURL(path: string) {
    return new URL(path, window.document.baseURI);
}

export function Link(props: React.HTMLProps<HTMLAnchorElement>) {
    const {href, onClick: _onClick, ...rest} = props;
    const isOrchardURL = href && makeCanonicalURL(href).origin == window.location.origin;

    const navigate = useSetAtom(navigateAtom);
    if (!isOrchardURL) {
        // plain anchor to the external URL
        return (
            <a {...props}></a>
        )
    }
    const onClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
        e.preventDefault();
        if (_onClick) {
            _onClick(e);
        }
        void navigate(makeCanonicalURL(href));
    }

    return (
        <a onClick={onClick} href={href} {...rest} />
    )
}