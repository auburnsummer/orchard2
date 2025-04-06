import { useAtomValue } from "jotai";
import { configAtom, currentRenderAtom } from "../atoms";

export function Outlet() {
    const currentRender = useAtomValue(currentRenderAtom);
    const config = useAtomValue(configAtom);
    if (!currentRender || !config) {
        return <></>;
    }
    const View = config.views[currentRender.view];
    if (!View) {
        return <p>Unknown view &apos;{currentRender.view}&apos;</p>;
    }

    return <View {...currentRender.props} />;
}