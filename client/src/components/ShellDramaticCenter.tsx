import { Shell, ShellProps } from "./Shell/Shell";

import commonStyles from "@cafe/theme/commonPatterns.module.css";

import cc from "clsx";
import { Surface } from "./ui/Surface";

type ShellDramaticCenterProps = ShellProps;

export function ShellDramaticCenter({
  children,
  navbar,
}: ShellDramaticCenterProps) {
  return (
    <Shell navbar={navbar}>
      <div className={cc("relative min-h-screen w-full flex items-center justify-center", commonStyles.paperBg)} >
        <Surface className="p-6">
          {children}
        </Surface>
      </div>
    </Shell>
  );
}
