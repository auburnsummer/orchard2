import { Shell } from "@cafe/components/Shell";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { ProfileNavbar } from "./ProfileNavbar";
import { Button } from "@cafe/components/ui/Button";
import { Alert } from "@cafe/components/ui/Alert";
import { Form } from "@cafe/minibridge/components/Form";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { CopyIconButton } from "@cafe/components/CopyIconButton";
import { TextInput } from "@cafe/components/ui/TextInput";


type ProfileApiKeyView = {
    has_api_key: boolean;
    api_key?: string;
}

export function ProfileApiKeyView({ has_api_key, api_key }: ProfileApiKeyView) {
    const csrfInput = useCSRFTokenInput();

    return (
        <Shell navbar={<ProfileNavbar />}>
            <Surface className="m-3 p-6 flex-grow flex flex-col gap-4">
                {
                    api_key && (
                        <Alert variant="success" className="mb-4">
                            <Words>
                                Your new API key is:
                            </Words>
                            <div className="flex flex-row items-end gap-1">
                                <TextInput
                                onFocus={(e) => e.target.select()}
                                disabled={false}
                                value={api_key}
                                readOnly
                                className="flex-grow"
                                />
                                <CopyIconButton value={api_key} className="pb-0.5" />
                            </div>
                            <Words>
                                Please copy and store it securely now. You won't be able to see it again!
                            </Words>
                            
                        </Alert>
                    )
                }
                <Words as="h2" variant="header">API Key Management</Words>
                <Form method="POST">
                    {csrfInput}
                    <Button>{has_api_key ? "Regenerate API Key" : "Generate API Key"}</Button>
                </Form>
                <Words>
                    Regenerating your API key will invalidate your previous key.
                </Words>
            </Surface>
        </Shell>
    );
}