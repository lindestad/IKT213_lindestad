from pathlib import Path

import cv2
from numpy.typing import NDArray

ASSIGNMENT_1_PATH = Path(__file__).parent.parent
IRIS_IMAGE_PATH = ASSIGNMENT_1_PATH / "assets" / "iris-1.jpg"


def print_image_information(image: NDArray):
    (height, width, channels) = image.shape
    size = image.size
    dtype = image.dtype
    print(
        f"Iris-1.jpg image information:\nA: Height: {height}\nB: Width: {width}\nC: Channels: {channels}\nD: Size: {size}\nE: Data type: {dtype}"
    )


def main():
    iris = cv2.imread(IRIS_IMAGE_PATH)
    if iris is None:
        raise FileNotFoundError(
            f"File not at expected location in repo. Attempted to read from {IRIS_IMAGE_PATH}"
        )
    print_image_information(iris)


if __name__ == "__main__":
    main()
