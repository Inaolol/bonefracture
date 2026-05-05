"""Environment smoke test for the notebook-first fracture project."""

from __future__ import annotations


def main() -> None:
    import cv2
    import ultralytics

    print("YOLOv8 fracture detection environment is ready.")
    print(f"ultralytics={ultralytics.__version__}")
    print(f"opencv={cv2.__version__}")


if __name__ == "__main__":
    main()
