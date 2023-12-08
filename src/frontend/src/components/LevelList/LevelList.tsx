import { useEffect } from "preact/hooks";
import "./LevelList.css";
import { search } from "@orchard/api/levels/levels";

export function LevelList() {
    useEffect(() => {
        (async () => {
            const test = await search({});
            console.log(test);
        })();
    }, []);

    return (
        <p>level list</p>
    )
}