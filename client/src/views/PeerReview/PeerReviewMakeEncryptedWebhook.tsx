
import { Button } from "@cafe/components/ui/Button";
import { TextInput } from "@cafe/components/ui/TextInput";
import { CopyIconButton } from "@cafe/components/CopyIconButton";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { Form } from "@cafe/minibridge/components/Form";
import { PeerReviewShell } from "./PeerReviewShell";
import { RDLevel } from "@cafe/types/rdLevelBase";
import { Surface } from "@cafe/components/ui/Surface";
import { Words } from "@cafe/components/ui/Words";
import { Alert } from "@cafe/components/ui/Alert";

type PeerReviewMakeEncryptedWebhookProps = {
    encrypted_url: string | null;
    levels: RDLevel[];
};

export function PeerReviewMakeEncryptedWebhook({
    encrypted_url,
    levels
}: PeerReviewMakeEncryptedWebhookProps) {
    const csrfInput = useCSRFTokenInput();

    const fullUrl = new URL(encrypted_url || "", window.location.origin).toString();

    return (
        <PeerReviewShell pendingLevels={levels}>
            <Surface className="mt-4 p-4">
                {
                    encrypted_url && (
                        <Alert variant="success">
                            <Words className="font-semibold">Here is the webhook</Words>
                            <div className="flex flex-row gap-2 items-baseline">
                                <TextInput
                                    onFocus={(e) => e.target.select()}
                                    disabled={false}
                                    value={fullUrl}
                                    readOnly
                                    className="flex-grow"
                                />
                                <CopyIconButton
                                    value={fullUrl}
                                />
                            </div>
                        </Alert>
                    )
                }
                <Words variant="header">
                    Generate Encrypted Webhook URL
                </Words>
                <Words as="p">
                    This tool is used to generate encrypted webhooks.
                </Words>
                <Words as="p">
                    An encrypted webhook can only be used by active peer reviewers.
                </Words>
                <Form method="POST" className="mt-4 space-y-4">
                    {csrfInput}
                    <TextInput
                        label="Webhook URL"
                        name="webhook_url"
                        type="url"
                        required
                        placeholder="https://example.com/webhook"
                    />
                    <Button type="submit">
                        Generate Encrypted Webhook
                    </Button>
                </Form>
            </Surface>

        </PeerReviewShell>
    );
}