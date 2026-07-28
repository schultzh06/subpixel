"""Generate PNG fixtures for tests.

Run manually:
    python tests/make_fixture.py 400 300 -o tests/fixtures/cover.png
    python tests/make_fixture.py 4 4 -o tests/fixtures/tiny.png
"""

import argparse
import os
import random
from pathlib import Path

from PIL import Image


def make_image(width: int, height: int, pattern: str, seed: int | None) -> Image.Image:
    """Build an RGB image of the given size using the named pattern."""
    n = width * height * 3

    if pattern == "noise":
        if seed is None:
            data = os.urandom(n)
        else:
            rng = random.Random(seed)
            data = bytes(rng.randrange(256) for _ in range(n))
        return Image.frombytes("RGB", (width, height), data)

    if pattern == "flat":
        return Image.new("RGB", (width, height), (128, 128, 128))

    if pattern == "gradient":
        img = Image.new("RGB", (width, height))
        px = img.load()
        for y in range(height):
            for x in range(width):
                px[x, y] = (
                    int(255 * x / max(width - 1, 1)),
                    int(255 * y / max(height - 1, 1)),
                    128,
                )
        return img

    raise ValueError(f"unknown pattern: {pattern}")


def main() -> None:
    p = argparse.ArgumentParser(description="Generate a PNG test fixture.")
    p.add_argument("width", type=int)
    p.add_argument("height", type=int)
    p.add_argument("-o", "--output", type=Path, required=True)
    p.add_argument(
        "-p", "--pattern",
        choices=["noise", "flat", "gradient"],
        default="noise",
        help="noise: random pixels (default). flat: solid grey. gradient: smooth ramp.",
    )
    p.add_argument(
        "-s", "--seed", type=int,
        help="seed for reproducible noise; omit for os.urandom",
    )
    args = p.parse_args()

    img = make_image(args.width, args.height, args.pattern, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    img.save(args.output, "PNG")

    capacity = (args.width * args.height * 3) // 8
    print(f"wrote {args.output}  {args.width}x{args.height}  {args.pattern}")
    print(f"capacity: {capacity:,} bytes ({capacity - 4:,} usable after header)")


if __name__ == "__main__":
    main()