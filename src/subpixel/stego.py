from PIL import Image
from typing import Iterator
from itertools import chain
from pathlib import Path

from .errors import MessageTooLargeError, DecryptionError

FIXTURES = Path(__file__).resolve().parents[1] / "tests" / "fixtures"

LENGTH_HEADER_BYTES = 4 # payload length as 4-byte big-endian int

def bytes_to_bits(data: bytes) -> Iterator[int]:
    """Yield each bit of each byte, most-significant bit first.

    MSB-first is a protocol choice, not a requirement: bits_to_bytes
    must reassemble in the same order.
    """
    for byte in data:
        for i in range(7,-1,-1):
            yield (byte >> i) & 1

def bits_to_bytes(bits: Iterator[int], count: int) -> bytes:
    """Return constructed bytes given iterator bits collection

    Length of bytes must be provided, will not process header
    """
    out = bytearray()
    for _ in range(count):
        byte = 0x0
        for _ in range(8):
            byte = (byte << 1) | next(bits)
        out.append(byte)
    return bytes(out)
        


def embed(cover_path: str, blob: bytes, out_path: str) -> None:
    """Embed a UTF-8 message in the LSBs of a cover image.

    The payload is a 4-byte big-endian length header followed by the
    encoded message. Output is always written as PNG; lossy formats
    would destroy the embedded bits.

    Raises:
        ValueError: if the message exceeds the cover image's capacity.
    """

    payload = len(blob).to_bytes(LENGTH_HEADER_BYTES, "big") + blob

    # Open cover image
    with Image.open(cover_path) as img:

        img = img.convert("RGB")

        # Flatten image channels
        flat = list(chain.from_iterable(img.get_flattened_data()))

        capacity_bits = len(flat)   # one bit per channel — width * height * 3
        if len(payload) * 8 > capacity_bits:
            raise MessageTooLargeError("Message too large")

        # Iterate and embed bits in flat
        bit_iter = bytes_to_bits(payload)
        for idx, channel in enumerate(flat):
            bit = next(bit_iter, None)
            if bit is None:
                break
            flat[idx] = (channel & 0xFE) | bit

        # Regroup pixels
        pixels = list(zip(*[iter(flat)] * 3)) # Zip channels into tuples by 3

        img.putdata(pixels)
        img.save(out_path, "PNG")

def extract(image_path: str) -> bytes:
    """Takes path to image and reads back embedded steganography data

    Reads length from steganography header
    """
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        flat = list(chain.from_iterable(img.get_flattened_data()))
        bit_stream = (channel & 1 for channel in flat)
        length = int.from_bytes(bits_to_bytes(bit_stream, LENGTH_HEADER_BYTES), "big")
        payload = bits_to_bytes(bit_stream, length)
        return payload

if __name__ == "__main__":
    embed(FIXTURES / "cover.png", "hello world", FIXTURES / "out.png")
    res = extract(FIXTURES / "out.png")
    assert res == "hello world"
    print("round-trip ok")
    print(res)