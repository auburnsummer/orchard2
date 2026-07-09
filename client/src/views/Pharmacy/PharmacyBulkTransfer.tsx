import { Words } from "@cafe/components/ui/Words";
import { useCSRFTokenInput } from "@cafe/hooks/useCSRFToken";
import { PharmacyShell } from "./PharmacyShell";
import { Form } from "@cafe/minibridge/components/Form";
import Textarea from "@cafe/components/ui/Textarea";
import { TextInput } from "@cafe/components/ui/TextInput";
import { Button } from "@cafe/components/ui/Button";

export function PharmacyBulkTransfer() {
    const csrfInput = useCSRFTokenInput();

    return (
        <PharmacyShell>
            <title>Bulk Transfer | Rhythm Café</title>
            <Words variant="header" className="mb-4">
                Bulk Transfer
            </Words>
            <Words as="p">
                This is a tool to transfer the submitter of level(s) from one user to another.
            </Words>
            <Form method="POST">
                <Textarea
                    name="level_ids"
                    label="Level IDs"
                    description="Each level ID should be on its own line"
                ></Textarea>

                <TextInput name="user_id" label="New Submitter User ID"></TextInput>

                <Button type="submit" className="mt-4" variant="primary">
                    Transfer Levels
                </Button>
                {csrfInput}
            </Form>
        </PharmacyShell>
    )
}