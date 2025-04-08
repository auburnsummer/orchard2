import { useSetAtom } from "jotai";
import { makeCanonicalURL } from "../utils";
import { formSubmitAtom } from "../atoms";


export function Form(props: React.HTMLProps<HTMLFormElement>) {
    const { action, onSubmit: _onSubmit, method, ...rest } = props;

    const isOrchardURL = action === undefined || makeCanonicalURL(action).origin === document.location.origin;

    const submitForm = useSetAtom(formSubmitAtom);

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
        }

    };

    return (
        <form
            onSubmit={onSubmit}
            action={action}
            method={method}
            {...rest}
        />
    )
}