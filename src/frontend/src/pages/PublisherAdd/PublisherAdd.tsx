import { Header } from "@orchard/components/Header";

import "./PublisherAdd.css";
import { Button, Input } from "@orchard/ui";
import { atom } from "jotai";


export function PublisherAdd() {
    return (
        <div class="pa">
            <Header />
            <main class="pa_main">
                <form class="pa_form">
                    <Input
                        required
                        label="Name the publisher"
                        helpText="This is typically the name of the Discord server. You can change this later."
                    />
                    <Button variant="primary" type="submit">Submit</Button>
                </form>
            </main>
        </div>
    )
}