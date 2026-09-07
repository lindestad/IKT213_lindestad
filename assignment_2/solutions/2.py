from multiprocessing import Value
from pathlib import Path

import cv2
import numpy as np

type CvImage = cv2.typing.MatLike

IRIS_PATH = Path(__file__).parent / "assets" / "iris.png"


def padding(image: CvImage, border_width) -> CvImage:
    pass


# 2. A, B
def crop(image: CvImage, x_0, x_1, y_0, y_1) -> CvImage:
    """
    Crop image:
    x_0: crop left side towards the right
    x_1: crop right side towards the left
    y_0: crop top towards bottom
    y_1: crop bottom towards top
    """
    try:
        assert x_0 >= 0 and x_1 >= 0 and y_0 >= 0 and y_1 >= 0
    except AssertionError:
        raise ValueError("Crop arguments must be 0 or positive")

    # Can do more validation like checking that you don't crop than by more than the
    # size of the image (image.shape)

    return image[y_0 : (image.shape[0] - y_1), x_0 : (image.shape[1] - x_1), :]


def main():
    iris: CvImage | None = cv2.imread(IRIS_PATH)
    assert iris is not None  # File loaded

    # 2. C, D
    iris_cropped = crop(iris, 200, 130, 200, 130)
    cv2.imwrite("iris_cropped.jpg", iris_cropped)


if __name__ == "__main__":
    main()
