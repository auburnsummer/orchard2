import { Link as DJLink } from "@django-bridge/react";

type LinkProps = Parameters<typeof DJLink>[0];

/**
 * Small wrapper around django-bridge Link to avoid passing through an onClick handler.
 * mantine passes an onClick handler if you use Link as a polymorphic component, but this
 * breaks django-bridge's handling.
 */
export function Link(props: LinkProps) {
    const {onClick, ...rest} = props;
    return <DJLink {...rest} />
}