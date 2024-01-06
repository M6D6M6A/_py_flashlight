import tkinter as tk
from screeninfo import get_monitors

class FlashlightApp:
    """
    A simple app to turn all connected monitors into a full-screen white display,
    effectively creating a flashlight effect. This app has been tested only on Windows 11.

    The app can be toggled on and off using a specified hotkey (default is F11).
    A separate hotkey (default F12) is provided to terminate the application.
    While active, the app creates a full-screen white window on each monitor,
    and the mouse cursor is hidden when it is over these windows.

    Attributes:
        root (tk.Tk): The root Tkinter window, hidden during operation.
        windows (list): A list of currently active full-screen windows.
        is_fullscreen (bool): Flag to indicate whether the app is currently active.
    """

    def __init__(self, hotkey='<F11>', terminate='<F12>'):
        """
        Initializes the FlashlightApp with specified hotkeys.

        Args:
            hotkey (str, optional): The keyboard hotkey to toggle the flashlight. Defaults to '<F11>'.
            terminate (str, optional): The keyboard hotkey to terminate the app. Defaults to '<F12>'.
        """
        self.root = tk.Tk()
        self.root.withdraw()
        self.windows = []
        self.is_fullscreen = False
        self.root.bind(hotkey, self.toggle_fullscreen)
        self.root.bind(terminate, self.terminate)

    def create_flashlight_window(self, monitor):
        """
        Creates a full-screen white window for a given monitor.

        Args:
            monitor (screeninfo.Monitor): The monitor on which to create the window.

        Returns:
            tk.Toplevel: The created Tkinter Toplevel window.
        """
        window = tk.Toplevel()
        window.configure(background='white', cursor='none')
        window.overrideredirect(1)  # Bypass the window manager
        window.attributes('-topmost', True)  # Keep window always on top

        # Adjust the geometry slightly if needed
        x = monitor.x + 1 if monitor.x >= 0 else monitor.x
        y = monitor.y + 1 if monitor.y >= 0 else monitor.y
        geometry = f"{monitor.width}x{monitor.height}+{x}+{y}"
        window.geometry(geometry)
        return window

    def toggle_fullscreen(self, event=None):
        """
        Toggles the full-screen flashlight mode on or off.
        """
        if self.is_fullscreen:
            self._destroy_windows()
        else:
            self.windows = [self.create_flashlight_window(monitor) for monitor in get_monitors()]
        self.is_fullscreen = not self.is_fullscreen

    def _destroy_windows(self):
        """
        Destroys all currently active full-screen windows and clears the windows list.
        """
        for window in self.windows:
            window.destroy()
        self.windows = []

    def terminate(self, event=None):
        """
        Terminates the application, closing any active windows and exiting the main event loop.
        """
        if self.is_fullscreen:
            self._destroy_windows()
        self.root.quit()

    def run(self):
        """
        Runs the app, entering the main event loop.
        """
        self.root.mainloop()


# Create and run the flashlight app
if __name__ == "__main__":
    app = FlashlightApp()
    app.run()
