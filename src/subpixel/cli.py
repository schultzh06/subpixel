import argparse
import sys

from .errors import SubpixelError
from .stego import embed, extract


def main() -> None:
    p = argparse.ArgumentParser(prog="subpixel", description=...)
    s = p.add_subparsers(dest="command", required=True)

    # TODO: encode subparser — args: -i/--image, -m/--message, -o/--output
    # TODO: decode subparser — args: -i/--image

    args = p.parse_args()

    try:
        pass
    except SubpixelError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)