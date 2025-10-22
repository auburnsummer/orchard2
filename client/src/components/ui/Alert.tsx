import { IconDefinition } from "@fortawesome/fontawesome-svg-core";
import { faCheckCircle, faInfoCircle, faWarning, faXmarkCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import cc from "clsx";

type Variant = "info" | "warning" | "error" | "success";

const commonStyles = "rounded-lg p-4";

const variantStyles: Record<Variant, string> = {
    info: "bg-blue-100 text-blue-800",
    warning: "bg-yellow-100 text-yellow-800",
    error: "bg-red-100 text-red-800",
    success: "bg-green-100  text-green-800",
};

const variantIcons : Record<Variant, React.ReactNode> = {
    info: <FontAwesomeIcon icon={faInfoCircle} className="text-blue-950 bg-blue-100" />,
    warning: <FontAwesomeIcon icon={faWarning} className="text-yellow-950 bg-yellow-100" />,
    error: <FontAwesomeIcon icon={faXmarkCircle} className="text-red-950 bg-red-100" />,
    success: <FontAwesomeIcon icon={faCheckCircle} className="text-green-950 bg-green-100" />,
};

type AlertProps = {
    children?: React.ReactNode;
    variant?: Variant;
    className?: string;
};

export function Alert({children, variant, className}: AlertProps) {
    const styles = variantStyles[variant || "info"];
    return (
        <div className={cc(styles, commonStyles, className)}>
            <div className="flex flex-row items-start justify-start">
                <div className="shrink-0">
                    {variantIcons[variant || "info"]}
                </div>
                <div className="ml-3">
                    {children}
                </div>
            </div>
        </div>
    );
}