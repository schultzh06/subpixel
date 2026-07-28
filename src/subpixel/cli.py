import argparse
from pathlib import Path
import sys

from .errors import SubpixelError
from .stego import embed, extract

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="subpixel",
        description="Hide messages in the least-significant bits of an image.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    enc = sub.add_parser("encode", help="embed a message into a cover image")
    enc.add_argument("-i", "--image", type=Path, required=True, help="cover image to hide the message in")
    enc.add_argument("-m", "--message", required=True, help="message to embed")
    enc.add_argument("-o", "--output", type=Path, required=True, help="output PNG path")

    dec = sub.add_parser("decode", help="extract a hidden message from an image")
    dec.add_argument("-i", "--image", type=Path, required=True, help="image containing an embedded message")

    return parser

def main() -> None:
    args = build_parser().parse_args()
    try:
        if args.command == "encode":
            embed(args.image, args.message, args.output)
            print(f"embedded {len(args.message)} chars into {args.output}")
        elif args.command == "decode":
            print(extract(args.image))
    except FileNotFoundError as e:
        print(f"error: no such file: {e.filename}", file=sys.stderr)
        sys.exit(1)
    except SubpixelError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)