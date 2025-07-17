import { useSetAtom } from "jotai";
import { formDataToSearchParams, makeCanonicalURL } from "../utils";
import { formSubmitAtom, navigateAtom } from "../atoms";

type FormProps = React.FormHTMLAttributes<HTMLFormElement> & {
    action?: string;
    ref?: React.Ref<HTMLFormElement>;
}

export function Form(props: FormProps) {
    const { action, onSubmit: _onSubmit, method, ref, ...rest } = props;

    const isOrchardURL = action === undefined || makeCanonicalURL(action).origin === document.location.origin;

    const submitForm = useSetAtom(formSubmitAtom);
    const navigate = useSetAtom(navigateAtom);

    if (!isOrchardURL) {
        return (
            <form {...props} />
        );
    }

    const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        if (_onSubmit) {
            _onSubmit(e);
            if (e.defaultPrevented) {
                return;
            }
        }
        e.preventDefault();

        if (e.target instanceof HTMLFormElement) {
            const data = new FormData(e.target);
            if (e.target.method === "post") {
                const target = action !== undefined
                    ? makeCanonicalURL(action)
                    : makeCanonicalURL(window.location.href)
                submitForm(target, data);
            }
            else if (e.target.method === "get") {
                let target = action !== undefined
                    ? makeCanonicalURL(action)
                    : makeCanonicalURL(window.location.href);
                const params = formDataToSearchParams(data);
                target = new URL(`${target.origin}${target.pathname}?${params.toString()}`);
                navigate(target);
            }
        }

    };

    return (
        <form
            onSubmit={onSubmit}
            action={action}
            method={method}
            ref={ref}
            {...rest}
        />
    )
}