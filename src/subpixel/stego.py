from PIL import Image
from typing import Iterator
from itertools import chain

LENGTH_HEADER_BYTES = 4 # payload length as 4-byte big-endian int

def bytes_to_bits(data: bytes) -> Iterator[int]:
    for byte in data:
        for i in range(7,-1,-1):
            yield (byte >> i) & 1


def bits_to_bytes(bits) -> bytes:
    pass

def embed(cover_path: str, message: str, out_path: str) -> None:

    msg_bytes = message.encode("utf-8")
    payload = len(msg_bytes).to_bytes(LENGTH_HEADER_BYTES, "big") + msg_bytes

    # Open cover image
    with Image.open(cover_path) as img:

        img.convert("RGB")

        # Flatten image channels
        width, height = img.size
        flat = list(chain.from_iterable(img.get_flattened_data()))

        capacity_bits = len(flat)   # one bit per channel — width * height * 3
        if len(payload) * 8 > capacity_bits:
            raise ValueError("Message too large")

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



def extract(image_path: str) -> str:
    pass

if __name__ == "__main__":
    embed("../tests/fixtures/cover.png", "hello world", "../tests/fixtures/out.png")
    #assert extract("out.png") == "hello world"
    print("round-trip ok")