import { Words } from "./Words";

import cc from "clsx";

type FieldsetProps = {
    legend: string;
    children: React.ReactNode;
    className?: string;
}

const Fieldset: React.FC<FieldsetProps> = ({ legend, children, className }) => {
    return (
        <fieldset className={cc("border border-gray-300 rounded-md p-4 mb-4", className)}>
            <Words as="legend">{legend}</Words>
            <div className="-mt-3">
                {children}
            </div>
        </fieldset>
    );
};

export default Fieldset;
