from multiprocessing import Value
from pathlib import Path

import cv2
import numpy as np

type CvImage = cv2.typing.MatLike

IRIS_PATH = Path(__file__).parent / "assets" / "iris.png"


# 1. A, B
def padding(image: CvImage, border_width) -> CvImage:
    return cv2.copyMakeBorder(
        image,
        border_width,
        border_width,
        border_width,
        border_width,
        cv2.BORDER_REFLECT,
    )


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


# 3. A, B
def resize(image: CvImage, width, height) -> CvImage:
    return cv2.resize(image, (width, height))


# 4. A, B
def copy(image, emptyPictureArray):
    emptyPictureArray[:, :, :] = image[:, :, :]


def main():
    iris: CvImage | None = cv2.imread(IRIS_PATH)
    assert iris is not None  # File loaded

    # 1. C, D
    iris_bordered = padding(iris, 200)
    cv2.imwrite("iris_bordered.jpg", iris_bordered)

    # 2. C, D
    iris_cropped = crop(iris, 200, 130, 200, 130)
    cv2.imwrite("iris_cropped.jpg", iris_cropped)

    # 3. C, D
    iris_resized = resize(iris, 200, 200)
    cv2.imwrite("iris_resized.jpg", iris_resized)

    # 4. C, D
    height, width, _ = iris.shape
    emptyPictureArray = np.zeros((height, width, 3), dtype=np.uint8)
    copy(
        iris, emptyPictureArray
    )  # Copies pixels over, emptyPictureArray no longer empty
    cv2.imwrite("iris_copied.jpg", emptyPictureArray)


if __name__ == "__main__":
    main()
