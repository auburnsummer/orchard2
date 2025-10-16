import { Center } from "@mantine/core";
import { Shell, ShellProps } from "../Shell/Shell";

import styles from "./ShellDramaticCenter.module.css";
import commonStyles from "@cafe/theme/commonPatterns.module.css";

import cc from "clsx";

type ShellDramaticCenterProps = ShellProps;

export function ShellDramaticCenter({
  children,
  navbar,
}: ShellDramaticCenterProps) {
  return (
    <Shell navbar={navbar}>
      <Center className={cc(styles.base, commonStyles.paperBg)}>
        {children}
      </Center>
    </Shell>
  );
}
