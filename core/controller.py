import logging
import time

import pyperclip
from pynput import keyboard
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import QApplication
from utils import cmd_v, get_current_process_id, get_focused_text, put_app_in_focus, return_app_in_focus

from core.model import Model
from core.views.floating_window import FloatingWindow
from core.views.system_tray import SystemTray
from core.views.text_processing import TextWindow

LOG = logging.getLogger(__name__)


class Controller:
    def __init__(self, model: Model, view: QApplication):
        self.view = view
        self.model = model
        self.option_key = False
        self.last_time = 0.0
        self.floating_window_open = False
        self.text_window_open = False
        self.focused_process_id = ""
        self.focused_text = ""
        self.processed_text = ""
        self.cmd_pressed = False
        self.option_pressed = False
        self.this_process_id = get_current_process_id()
        self.setup_windows()
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def get_window_tabs_items(self) -> dict[str, list[str]]:
        return self.model.sections

    def update_floating_window_status(self, statue: bool):
        self.floating_window_open = statue

    def update_text_window_status(self, status: bool):
        self.text_window_open = status

    def setup_event_handlers(self):
        self.view.floating_window.custom_signal.connect(self.process_text)
        self.view.floating_window.event_put_app_focus.connect(self.put_this_app_in_focus)
        self.view.text_window.event_put_app_focus.connect(self.put_this_app_in_focus)

        self.view.floating_window.windows_event.connect(self.update_floating_window_status)
        self.view.text_window.windows_event.connect(self.update_text_window_status)

    def recreate_text_window(self):
        LOG.debug("Recreating text window")
        self.view.text_window = TextWindow(
            processing_text=self.focused_text, functions_list=self.model.get_all_functions_flattened()
        )
        LOG.debug("Text window recreated")

    def setup_windows(self) -> None:
        self.view.main_window = SystemTray()

        # Create the system tray icon
        self.view.main_window.show()

        # Create the floating window, passing the key listener to it
        tabs = self.get_window_tabs_items()

        self.view.floating_window = FloatingWindow(tabs)
        self.recreate_text_window()
        self.setup_event_handlers()

    def get_focused_text(self) -> None:
        self.focused_text = get_focused_text()

    def return_app_in_focus(self) -> None:
        self.focused_process_id = return_app_in_focus()

    def put_previous_app_in_focus(self) -> None:
        return put_app_in_focus(self.focused_process_id)

    def put_this_app_in_focus(self) -> None:
        return put_app_in_focus(self.this_process_id)

    def set_processed_text(self, section: str, item: str, **kwargs) -> str:
        processed_text = self.model.process_text(section, item, self.focused_text, **{})
        pyperclip.copy(processed_text)
        self.put_previous_app_in_focus()
        time.sleep(0.3)
        cmd_v()
        return self.processed_text

    def process_text(self, section: str, item: str) -> None:
        QTimer.singleShot(0, lambda: self.set_processed_text(section, item))

    def on_press(self, key: keyboard.Key) -> None:
        try:
            # Detect if the pressed key is Cmd or Option (Alt)
            if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                self.option_pressed = True
            elif key == keyboard.Key.cmd_l or key == keyboard.Key.cmd_r:
                self.cmd_pressed = True

            # If both Cmd and Option keys are pressed simultaneously, open another window
            if self.cmd_pressed and self.option_pressed:
                if not self.text_window_open:
                    self.open_text_window()
                    self.text_window_open = True
                self.cmd_pressed = False  # Reset after action to avoid repeated detection
                self.option_pressed = False

            # If only the Option key is pressed, follow the original logic
            elif self.option_pressed:
                current_time = time.time()

                # If two presses are detected within 1 second, open the window
                if current_time - self.last_time < 0.8:
                    if self.floating_window_open:
                        self.close_floating_window()
                    else:
                        self.open_floating_window()
                self.last_time = current_time
                self.option_pressed = False  # Reset after action

        except AttributeError as e:
            LOG.debug(f"AttributeError: {e}")
            pass

    def _open_text_window(self) -> None:
        LOG.debug("Opening text window")
        self.recreate_text_window()

    def open_text_window(self) -> None:
        pass  # This is still unreliable

    def open_floating_window(self) -> None:
        self.get_focused_text()
        self.return_app_in_focus()
        QTimer.singleShot(0, self.view.floating_window.show)
        self.floating_window_open = True

    def close_floating_window(self) -> None:
        QTimer.singleShot(0, self.view.floating_window.close)
        self.put_previous_app_in_focus()
        self.floating_window_open = False

    def on_release(self, key: keyboard.Key) -> None:
        # Reset flags when keys are released
        if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            self.option_pressed = False
        elif key == keyboard.Key.cmd_l or key == keyboard.Key.cmd_r:
            self.cmd_pressed = False
