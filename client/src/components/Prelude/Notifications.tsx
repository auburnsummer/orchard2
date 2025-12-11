import { useEffect, useState } from "react";

import { useMessages } from "@cafe/minibridge/hooks";
import { Transition } from "@headlessui/react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheckCircle, faWarning, faXmark } from "@fortawesome/free-solid-svg-icons";
import { MessageLevel } from "@cafe/minibridge/fetch";

const MESSAGE_ELEMENTS: Record<MessageLevel, React.ReactNode> = {
  info: <FontAwesomeIcon icon={faCheckCircle} aria-hidden="true" className="size-6 text-blue-400" />,
  success: <FontAwesomeIcon icon={faCheckCircle} aria-hidden="true" className="size-6 text-green-400" />,
  warning: <FontAwesomeIcon icon={faWarning} aria-hidden="true" className="size-6 text-yellow-400" />,
  error: <FontAwesomeIcon icon={faXmark} aria-hidden="true" className="size-6 text-red-400" />,
}

// 7 seconds
const MESSAGE_TIMEOUT = 7000;

export function Notifications() {
  // set by minibridge
  const [messages, setMessages] = useMessages();

  const [showMessage, setShowMessage] = useState(true);

  useEffect(() => {
    if (messages.length > 0) {
      const timeout = setTimeout(() => {
        setShowMessage(false);
        setTimeout(() => {
          setMessages((prev) => prev.slice(1));
          setShowMessage(true);
        }, 100);
      }, MESSAGE_TIMEOUT);
      return () => clearTimeout(timeout);
    }
  }, [messages]);

  const displayedMessage = messages.at(0);

  return (
    <>
      {/* Global notification live region, render this permanently at the end of the document */}
      <div
        aria-live="assertive"
        className="pointer-events-none fixed inset-0 top-12 flex items-end px-4 py-6 sm:items-start sm:p-6 z-50"
      >
        <div className="flex w-full flex-col items-center space-y-4 sm:items-end">
          {/* Notification panel, dynamically insert this into the live region when it needs to be displayed */}
          <Transition show={displayedMessage !== undefined && showMessage}>
            <div className="pointer-events-auto w-full max-w-sm rounded-lg bg-white shadow-lg outline-1 outline-black/5 transition data-closed:opacity-0 data-enter:transform data-enter:duration-300 data-enter:ease-out data-closed:data-enter:translate-y-2 data-leave:duration-100 data-leave:ease-in data-closed:data-enter:sm:translate-x-2 data-closed:data-enter:sm:translate-y-0 dark:bg-gray-800 dark:-outline-offset-1 dark:outline-white/10">
              <div className="p-4">
                <div className="flex items-start">
                  <div className="shrink-0">
                    {MESSAGE_ELEMENTS[displayedMessage?.level || "info"]}
                  </div>
                  <div className="ml-3 w-0 flex-1 pt-0.5">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">{displayedMessage?.html}</p>
                  </div>
                  <div className="ml-4 flex shrink-0 pt-0.5">
                    <button
                      type="button"
                      onClick={() => {
                        setShowMessage(false);
                        setTimeout(() => {
                          setMessages((prev) => prev.slice(1));
                          setShowMessage(true);
                        }, 100);
                      }}
                      className="inline-flex rounded-md p-2 -m-2 text-gray-400 hover:text-gray-500 focus:outline-2 focus:outline-offset-2 focus:outline-indigo-600 dark:hover:text-white dark:focus:outline-indigo-500"
                    >
                      <span className="sr-only">Close</span>
                      <FontAwesomeIcon icon={faXmark} aria-hidden="true" className="size-5" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </Transition>
        </div>
      </div>
    </>
  )
}
