from pathlib import Path

import cv2
import numpy as np

type CvImage = cv2.typing.MatLike

SOLUTIONS_PATH = Path(__file__).resolve().parent
ASSETS_PATH = SOLUTIONS_PATH.parent / "assets"
REFERENCE_PATH = ASSETS_PATH / "reference_img.png"
ALIGN_PATH = ASSETS_PATH / "align_this.jpg"


# 1. A, B
def harris_corner_detection(reference_image: CvImage) -> CvImage:
    grayscale = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)
    corners = cv2.cornerHarris(grayscale.astype(np.float32), 2, 3, 0.04)
    kernel = np.ones((3, 3), dtype=np.uint8)
    corners = cv2.dilate(corners, kernel)

    marked_image = reference_image.copy()
    marked_image[corners > 0.01 * corners.max()] = [0, 0, 255]
    return marked_image


# 2. A, B
def align_images(
    image_to_align: CvImage, reference_image: CvImage, max_features, good_match_precent
) -> tuple[CvImage, CvImage]:
    # In the SIFT example, 10 is the minimum match count, not a keypoint limit.
    if max_features < 4:
        raise ValueError("At least four matches are needed to align the images")
    if not 0 < good_match_precent < 1:
        raise ValueError("Good match percent must be between 0 and 1")

    grayscale = cv2.cvtColor(image_to_align, cv2.COLOR_BGR2GRAY)
    reference_grayscale = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT.create()
    keypoints, descriptors = sift.detectAndCompute(grayscale, None)
    reference_keypoints, reference_descriptors = sift.detectAndCompute(
        reference_grayscale, None
    )
    if descriptors is None or reference_descriptors is None:
        raise ValueError("No features found in one of the images")
    if len(reference_descriptors) < 2:
        raise ValueError("Not enough reference features for matching")

    matcher = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=50))
    matches = matcher.knnMatch(descriptors, reference_descriptors, k=2)
    good_matches = []
    for match, second_match in matches:
        if match.distance < good_match_precent * second_match.distance:
            good_matches.append(match)
    if len(good_matches) < max_features:
        raise ValueError(f"Not enough good matches: {len(good_matches)}")

    points = np.array(
        [keypoints[match.queryIdx].pt for match in good_matches], dtype=np.float32
    )
    reference_points = np.array(
        [reference_keypoints[match.trainIdx].pt for match in good_matches],
        dtype=np.float32,
    )
    homography, inliers = cv2.findHomography(points, reference_points, cv2.RANSAC, 5.0)
    if homography is None or inliers is None or np.count_nonzero(inliers) < 4:
        raise ValueError("Could not find a reliable alignment")

    height, width = reference_image.shape[:2]
    aligned = cv2.warpPerspective(image_to_align, homography, (width, height))

    # Only draw matches which agree with the alignment.
    inlier_matches = []
    for match, inlier in zip(good_matches, inliers.ravel()):
        if inlier:
            inlier_matches.append(match)

    # Make room for both images side by side.
    image_height, image_width = image_to_align.shape[:2]
    matched_image = np.zeros(
        (max(image_height, height), image_width + width, 3), dtype=np.uint8
    )
    matched_image = cv2.drawMatches(
        image_to_align,
        keypoints,
        reference_image,
        reference_keypoints,
        inlier_matches,
        matched_image,
        matchColor=(0, 255, 0),
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )
    return aligned, matched_image


def main():
    reference_image: CvImage | None = cv2.imread(REFERENCE_PATH)
    image_to_align: CvImage | None = cv2.imread(ALIGN_PATH)
    assert reference_image is not None  # File loaded
    assert image_to_align is not None

    # 1. C
    harris = harris_corner_detection(reference_image)
    cv2.imwrite(SOLUTIONS_PATH / "harris.png", harris)

    # 2. B, C
    aligned, matches = align_images(image_to_align, reference_image, 10, 0.7)
    cv2.imwrite(SOLUTIONS_PATH / "aligned.png", aligned)
    cv2.imwrite(SOLUTIONS_PATH / "matches.png", matches)


if __name__ == "__main__":
    main()
