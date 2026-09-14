from pathlib import Path

import cv2
import numpy as np

type CvImage = cv2.typing.MatLike

ASSETS_PATH = Path(__file__).parent.parent / "assets"
LAMBO_PATH = ASSETS_PATH / "lambo.png"
SHAPES_PATH = ASSETS_PATH / "shapes.png"
TEMPLATE_PATH = ASSETS_PATH / "shapes_template.jpg"


# 1. A, B
def sobel_edge_detection(image: CvImage) -> CvImage:
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayscale, (3, 3), 0)
    edges = cv2.Sobel(blurred, cv2.CV_16S, dx=1, dy=1, ksize=1)
    # Take the absolute values before converting to uint8 to keep negative edges.
    return cv2.convertScaleAbs(edges)


# 2. A, B
def canny_edge_detection(image: CvImage, threshold_1, threshold_2) -> CvImage:
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayscale, (3, 3), 0)
    return cv2.Canny(blurred, threshold_1, threshold_2)


# 3. A, B
def template_match(image: CvImage, template: CvImage) -> CvImage:
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template_grayscale = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    matches = cv2.matchTemplate(grayscale, template_grayscale, cv2.TM_CCOEFF_NORMED)
    locations = np.where(matches >= 0.9)

    height, width = template_grayscale.shape
    matched_image = image.copy()
    for y, x in zip(*locations):
        cv2.rectangle(matched_image, (x, y), (x + width, y + height), (0, 0, 255), 2)
    return matched_image


# 4. A, B
def resize(image: CvImage, scale_factor: int, up_or_down: str) -> CvImage:
    """Resize by a power of two using image pyramids, e.g. 2, 4 or 8."""
    if scale_factor < 1 or scale_factor & (scale_factor - 1):
        raise ValueError("Scale factor must be a positive power of two")
    if up_or_down not in ("up", "down"):
        raise ValueError("Resize direction must be up or down")

    # Each pyramid step doubles or halves the image dimensions.
    while scale_factor > 1:
        if up_or_down == "up":
            image = cv2.pyrUp(image)
        else:
            image = cv2.pyrDown(image)
        scale_factor //= 2
    return image


def main():
    lambo: CvImage | None = cv2.imread(LAMBO_PATH)
    shapes: CvImage | None = cv2.imread(SHAPES_PATH)
    template: CvImage | None = cv2.imread(TEMPLATE_PATH)
    assert lambo is not None  # File loaded
    assert shapes is not None
    assert template is not None

    # 1. C, D, E
    lambo_sobel = sobel_edge_detection(lambo)
    cv2.imwrite("lambo_sobel.png", lambo_sobel)

    # 2. C, D, E
    lambo_canny = canny_edge_detection(lambo, 50, 50)
    cv2.imwrite("lambo_canny.png", lambo_canny)

    # 3. C, D
    shapes_matched = template_match(shapes, template)
    cv2.imwrite("shapes_matched.png", shapes_matched)

    # 4. C, D, E
    lambo_up = resize(lambo, 2, "up")
    cv2.imwrite("lambo_up.png", lambo_up)

    lambo_down = resize(lambo, 2, "down")
    cv2.imwrite("lambo_down.png", lambo_down)


if __name__ == "__main__":
    main()
