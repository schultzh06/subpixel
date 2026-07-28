# subpixel

Python CLI that hides messages in an image's least-significant bits.

> **Status:** early. LSB embed/extract works; encryption is not implemented yet.

## Install

    git clone https://github.com/<you>/subpixel
    cd subpixel
    python3 -m venv .venv && source .venv/bin/activate
    pip install -e .

## Usage

    subpixel encode -i cover.png -m "meet at noon" -o out.png
    subpixel decode -i out.png

Output is always PNG. Lossy formats (JPEG) destroy the embedded bits.

## How it works

Each RGB channel is one byte. Overwriting its least-significant bit shifts
the value by at most 1 — imperceptible to the eye, but it gives you one bit
of storage per channel, so three bits per pixel.

The payload is a 4-byte big-endian length header followed by the UTF-8
message. The decoder reads the header first, which tells it exactly how many
more bits to pull — no delimiter needed, so the scheme stays safe for
arbitrary binary payloads.

## Limitations

- Hides data from casual inspection only. Sequential LSB embedding is
  detectable by standard steganalysis (chi-square, RS analysis).
- No encryption yet — anyone who knows the scheme can read the message.
- Requires a lossless cover format.

## Development

    pip install -e ".[dev]"
    pytest