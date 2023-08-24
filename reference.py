import signal
import tkinter as tk


def on_closing():
    print("Tkinter window is closing...")
    # Add your code here for actions to be performed before exiting
    root.destroy()  # Close the Tkinter window


def main():
    global root
    root = tk.Tk()
    root.title("Tkinter Window")

    # Set up the on_closing function to be called when the window is closed
    root.protocol("WM_DELETE_WINDOW", on_closing)

    label = tk.Label(root, text="Close this window using the 'X' button.")
    label.pack(padx=20, pady=20)

    root.mainloop()


if __name__ == "__main__":
    # Set up a signal handler to catch SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    main()
