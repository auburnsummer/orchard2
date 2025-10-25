import { Words } from "./Words";

type FieldsetProps = {
    legend: string;
    children: React.ReactNode;
}

const Fieldset: React.FC<FieldsetProps> = ({ legend, children }) => {
    return (
        <fieldset className="border border-gray-300 rounded-md p-4 mb-4">
            <Words as="legend">{legend}</Words>
            {children}
        </fieldset>
    );
};

export default Fieldset;
