import {
  DialogProps as BaseDialogProps,
  Dialog as BaseDialog,
  DialogBackdrop,
  DialogPanel
} from "@headlessui/react";
import cc from "clsx";

export type DialogProps = BaseDialogProps;

export function Dialog({ className, children, ...rest }: DialogProps) {
  return (
    <BaseDialog {...rest} className={cc("relative z-10", className)}>
      <DialogBackdrop
        transition
        className="fixed inset-0 bg-gray-500/75 backdrop-blur-[1px] transition-opacity data-closed:opacity-0 data-enter:duration-300 data-enter:ease-out data-leave:duration-200 data-leave:ease-in dark:bg-gray-900/50"
      />
        <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
          <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
            <DialogPanel
              transition
              className="relative transform overflow-hidden rounded-lg bg-white px-4 pt-5 pb-4 text-left shadow-xl transition-all data-closed:translate-y-4 data-closed:opacity-0 data-enter:duration-300 data-enter:ease-out data-leave:duration-200 data-leave:ease-in sm:my-8 sm:w-full sm:max-w-sm sm:p-6 data-closed:sm:translate-y-0 data-closed:sm:scale-95 dark:bg-gray-800 dark:outline dark:-outline-offset-1 dark:outline-white/10"
            >
              {children}
            </DialogPanel>
          </div>
        </div>
    </BaseDialog>
  );
}
