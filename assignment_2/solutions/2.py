from pathlib import Path

import cv2

IRIS_PATH = Path(__file__).parent / "assets" / "iris.png"


def padding(image, border_width):
    pass


def main():
    iris = cv2.imread(IRIS_PATH)


if __name__ == "__main__":
    main()
