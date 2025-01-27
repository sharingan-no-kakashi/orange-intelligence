import logging

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCloseEvent, QHideEvent, QKeyEvent, QShowEvent
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QTabWidget, QVBoxLayout, QWidget

from core.views.styling.floating_window_style import FloatingWindowStyleOptions

LOG = logging.getLogger(__name__)


class FloatingWindow(QWidget):
    custom_signal = pyqtSignal(str, str)
    windows_event = pyqtSignal(bool)
    process_text_event = pyqtSignal(str, str, str)
    event_put_app_focus = pyqtSignal()

    def __init__(self, tab_sections: dict):
        super().__init__()
        # Set macOS-style window appearance
        self.setWindowTitle(FloatingWindowStyleOptions.title)
        self.setGeometry(200, 200, 400, 300)
        self.setStyleSheet(FloatingWindowStyleOptions.base)

        self.tab_widget = QTabWidget()
        self.tab_scroll_positions = {}
        self.set_up_tab_widget(tab_sections)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        current_index = self.tab_widget.currentIndex()
        current_widget = self.tab_widget.currentWidget()

        if event.key() == Qt.Key.Key_Escape:
            self.close()

        # Retrieve the QListWidget inside the current tab
        if current_widget:
            list_widget = current_widget.findChild(QListWidget)
            if list_widget and isinstance(list_widget, QListWidget):
                # If the current tab contains a QListWidget
                if event.key() == Qt.Key.Key_Up:
                    current_row = list_widget.currentRow()
                    new_row = max(0, current_row - 1)
                    list_widget.setCurrentRow(new_row)
                elif event.key() == Qt.Key.Key_Down:
                    current_row = list_widget.currentRow()
                    new_row = min(list_widget.count() - 1, current_row + 1)
                    list_widget.setCurrentRow(new_row)

                if event.key() == Qt.Key.Key_Return:
                    # Handle Enter key
                    current_item = list_widget.currentItem()  # Get the currently selected item
                    if current_item:
                        tab_name = self.tab_widget.tabText(current_index)
                        row_text = current_item.text()
                        self.handle_enter_key(tab_name, row_text, current_index)

                    else:
                        LOG.debug("No item selected in the current list.")
            else:
                LOG.debug("Current tab does not contain a QListWidget.")
        else:
            LOG.debug("No current widget in the tab.")

        # Handle Left and Right arrow keys to switch tabs
        if event.key() == Qt.Key.Key_Right:
            next_index = (current_index + 1) % self.tab_widget.count()
            self.tab_widget.setCurrentIndex(next_index)
        elif event.key() == Qt.Key.Key_Left:
            previous_index = (current_index - 1) % self.tab_widget.count()
            self.tab_widget.setCurrentIndex(previous_index)
        else:
            # Pass other key events to the parent class
            super().keyPressEvent(event)

    def set_up_tab_widget(self, tab_sections: dict) -> None:
        # Create the tab widget
        self.tab_widget.setTabsClosable(False)
        self.tab_widget.setStyleSheet(FloatingWindowStyleOptions.tab_widget)

        # Create tabs
        self.create_tabs(tab_sections)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)

        # Initialize scroll positions for all tabs
        for i in range(self.tab_widget.count()):
            self.tab_scroll_positions[i] = 0

    def create_tabs(self, tab_sections: dict) -> None:
        for section_name, tab_section in tab_sections.items():
            tab = QWidget()
            tab_layout = QVBoxLayout()

            list_widget = QListWidget()
            list_widget.setStyleSheet(FloatingWindowStyleOptions.list_widget)
            tab_layout.addWidget(list_widget)

            for key in tab_section:
                item = QListWidgetItem(key)
                list_widget.addItem(item)
            list_widget.setCurrentRow(0)  # Set the current row to the first item

            tab.setLayout(tab_layout)  # Set layout for the tab
            self.tab_widget.addTab(tab, section_name)  # Add the tab

    def handle_enter_key(self, tab_name: str, text_item: str, tab_index: int) -> None:
        """Close the window and trigger the processText function."""
        self.custom_signal.emit(tab_name, text_item)
        self.close()  # Close the window

    def closeEvent(self, event: QCloseEvent) -> None:
        # Hide the window instead of closing it to prevent application shutdown
        event.ignore()
        self.hide()
        # Update the key listener state when the window is hidden
        self.windows_event.emit(False)

    def hideEvent(self, event: QHideEvent) -> None:
        # Ensure the key listener flag is updated when the window is hidden
        self.windows_event.emit(False)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        # Ensure the window is focused when shown
        self.raise_()  # Raise the window to the top
        self.activateWindow()  # Make the window active (focused)

        self.windows_event.emit(True)

        self.event_put_app_focus.emit()
