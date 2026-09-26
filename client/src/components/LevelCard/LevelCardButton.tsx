import { IconDefinition } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

type LevelCardButtonBaseProps = {
    icon: IconDefinition;
}

type LevelCardButtonProps<T extends React.ElementType = 'button'> = LevelCardButtonBaseProps & {
    as?: T;
} & Omit<React.ComponentPropsWithoutRef<T>, keyof LevelCardButtonBaseProps | 'as'>;


export function LevelCardButton<T extends React.ElementType = 'button'>({
    icon,
    as,
    ...rest
}: LevelCardButtonProps<T>) {
    const Component = as || 'button';
    return (
        <Component
            className="w-8 border border-white p-2 rounded flex items-center justify-center bg-transparent text-white hover:bg-violet-400 hover:cursor-pointer"
            {...rest}
        >
            <FontAwesomeIcon icon={icon} className="w-4 h-4" />
        </Component>
    )
}