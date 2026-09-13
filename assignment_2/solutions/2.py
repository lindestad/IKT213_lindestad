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


# 5. A, B
def grayscale(image: CvImage) -> CvImage:
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# 6. A, B
def hsv(image: CvImage) -> CvImage:
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


# 7. A, B
def hue_shifted(image, emptyPictureArray, hue):
    # Convert before adding so uint8 values don't wrap around at 255.
    # Keep the shifted values between 0 and 255.
    emptyPictureArray[:, :, :] = np.clip(image.astype(np.int32) + hue, 0, 255)


# 8. A, B
def smoothing(image: CvImage) -> CvImage:
    return cv2.GaussianBlur(image, (15, 15), 0, borderType=cv2.BORDER_DEFAULT)


# 9. A, B
def rotation(image: CvImage, rotation_angle) -> CvImage:
    if rotation_angle == 90:
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    if rotation_angle == 180:
        return cv2.rotate(image, cv2.ROTATE_180)
    raise ValueError("Rotation angle must be 90 or 180")


def main():
    iris: CvImage | None = cv2.imread(IRIS_PATH)
    assert iris is not None  # File loaded

    # 1. C, D
    iris_bordered = padding(iris, 100)
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

    # 5. C, D
    iris_grayscale = grayscale(iris)
    cv2.imwrite("iris_grayscale.jpg", iris_grayscale)

    # 6. C, D
    iris_hsv = hsv(iris)
    cv2.imwrite("iris_hsv.jpg", iris_hsv)

    # 7. C, D
    emptyPictureArray = np.zeros((height, width, 3), dtype=np.uint8)
    hue_shifted(iris, emptyPictureArray, 50)
    cv2.imwrite("iris_hue_shifted.jpg", emptyPictureArray)

    # 8. C, D
    iris_smoothed = smoothing(iris)
    cv2.imwrite("iris_smoothed.jpg", iris_smoothed)

    # 9. C, D
    iris_rotated = rotation(iris, 180)
    cv2.imwrite("iris_rotated.jpg", iris_rotated)


if __name__ == "__main__":
    main()
