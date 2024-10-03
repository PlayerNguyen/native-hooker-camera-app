import argparse
from capture import Capture
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Video processing application")

    # Add arguments
    parser.add_argument(
        "--video-source",
        type=str,
        default="0",
        help="Video source, can be a file path or camera index",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=400,
        help="Cropped width preprocess before recognition stage",
    )
    parser.add_argument(
        "--detector", type=str, default="yolov8", help="Object detector model to use"
    )
    parser.add_argument(
        "--recognition", type=str, default="Facenet512", help="Recognition model to use"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0,
        help="The delay between recognition, in seconds",
    )
    parser.add_argument(
        "--hide-preview", type=bool, default=False, help="Hide preview window"
    )
    parser.add_argument(
        "--recognition-level",
        type=float,
        default=0.67,
        help="Recognition level for searching who is it. The range is from 0 to 1. The lower the value got, the less accurate the search level remain.",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Access the values
    print(f"Video Source: {args.video_source}")
    print(f"Width: {args.width}")
    print(f"Detector: {args.detector}")
    print(f"Recognition: {args.recognition}")
    print(f"Delay: {args.delay}")
    print(f"Hide Preview: {args.hide_preview}")
    print(f"Recognition level: {args.recognition_level}")

    # Create an instance of the Capture class with the parsed arguments
    capture = Capture(
        video_source=args.video_source,
        width=args.width,
        detector=args.detector,
        recognition=args.recognition,
        delay=args.delay,
        hide_preview=args.hide_preview,
        recognition_level=args.recognition_level,
    )

    # Start application
    capture.start_application()


if __name__ == "__main__":
    main()
