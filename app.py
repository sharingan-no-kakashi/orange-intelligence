import logging.config
import sys

from config import CONFIG
from PyQt6.QtWidgets import QApplication
from utils import avoid_dock_macos_icon

from core.controller import Controller
from core.model import Model


def main():
    logging.config.dictConfig(CONFIG["logging"])

    app = QApplication(sys.argv)

    avoid_dock_macos_icon()

    model = Model()

    controller = Controller(model=model, view=app)

    # Run the event loop
    sys.exit(controller.view.exec())


if __name__ == "__main__":
    main()
