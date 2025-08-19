import os
from pathlib import Path
import cv2


def print_image_information(image):
    if image is None:
        raise ValueError("image is None")
    if len(image.shape) == 2:
        height, width = image.shape
        channels = 1
    else:
        height, width, channels = image.shape
    print(f"{'Height:':12} {height}")
    print(f"{'Width:':12} {width}")
    print(f"{'Channels:':12} {channels}")
    print(f"{'Size:':12} {image.size}")
    print(f"{'Data type:':12} {image.dtype}")


def save_camera_information_to_txt():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # fallback backend on Windows
    fps_val = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    fps = int(fps_val) if fps_val and fps_val > 0 else 0

    solutions_dir = Path(__file__).parent / "solutions"
    solutions_dir.mkdir(parents=True, exist_ok=True)
    out_path = solutions_dir / "camera_outputs.txt"
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"fps: {fps}\n")
        f.write(f"height: {height}\n")
        f.write(f"width: {width}\n")


def main():
    base_dir = os.path.dirname(__file__)
    p1 = os.path.join(base_dir, "assets", "img", "lena.png")
    img = cv2.imread(p1, cv2.IMREAD_UNCHANGED)
    print_image_information(img)
    save_camera_information_to_txt()


if __name__ == "__main__":
    main()
