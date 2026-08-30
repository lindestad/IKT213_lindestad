from pathlib import Path

import cv2


def main():
    # Open the default camera
    cam = cv2.VideoCapture(0)

    # Guard clause
    if not cam.isOpened():
        raise RuntimeError("Failed to open webcam.")

    try:
        fps = cam.get(cv2.CAP_PROP_FPS)
        height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))

        output_path = Path(__file__).with_name("camera_outputs.txt")
        content = f"fps: {fps:g}\nheight: {height}\nwidth: {width}\n"
        output_path.write_text(
            content,
            encoding="utf-8",
        )
        print(f"Wrote:\n{content}\n\nWritten to {output_path}.")
    finally:
        cam.release()


if __name__ == "__main__":
    main()
