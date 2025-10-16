import { useSetAtom } from "jotai";
import { navigateAtom } from "../atoms";
import { makeCanonicalURL } from "../utils";

export function Link(props: React.HTMLProps<HTMLAnchorElement>) {
  const { href, onClick: _onClick, ...rest } = props;
  const isOrchardURL =
    href && makeCanonicalURL(href).origin == window.location.origin;

  const navigate = useSetAtom(navigateAtom);
  if (!isOrchardURL) {
    // plain anchor to the external URL
    return <a {...props}></a>;
  }
  // otherwise it should go through internal routing
  const onClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    if (_onClick) {
      _onClick(e);
    }
    void navigate(makeCanonicalURL(href));
  };
  return <a onClick={onClick} href={href} {...rest} />;
}
