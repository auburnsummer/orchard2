import { faCheck, faCopy } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { ActionIcon, CopyButton, Tooltip } from "@mantine/core";

type CopyIconButtonProps = {
  value: string;
};

export function CopyIconButton({ value }: CopyIconButtonProps) {
  return (
    <CopyButton value={value}>
      {({ copied, copy }) => (
        <Tooltip label={copied ? "Copied" : "Copy"} withArrow position="right">
          <ActionIcon
            color={copied ? "teal" : "gray"}
            variant="subtle"
            onClick={copy}
          >
            {copied ? (
              <FontAwesomeIcon icon={faCheck} />
            ) : (
              <FontAwesomeIcon icon={faCopy} />
            )}
          </ActionIcon>
        </Tooltip>
      )}
    </CopyButton>
  );
}
