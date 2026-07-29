from pathlib import Path

import pytest

from subpixel import embed, extract
from subpixel.errors import MessageTooLargeError

FIXTURES = Path(__file__).parent / "fixtures"


def test_stego_round_trip(tmp_path):
    out = tmp_path / "out.png"
    embed(FIXTURES / "cover.png", "hello world".encode("utf-8"), out)
    assert extract(out).decode("utf-8") == "hello world"


def test_multibyte(tmp_path):
    msg = "héllo 😛😛😛😛😛😛"
    out = tmp_path / "out.png"
    embed(FIXTURES / "cover.png", msg.encode("utf-8"), out)
    assert extract(out).decode("utf-8") == msg


def test_image_actually_changes(tmp_path):
    out = tmp_path / "out.png"
    embed(FIXTURES / "cover.png", "hello world".encode("utf-8"), out)
    assert out.read_bytes() != (FIXTURES / "cover.png").read_bytes()


def test_too_large(tmp_path):
    with pytest.raises(MessageTooLargeError):
        embed(FIXTURES / "tiny.png", ("x" * 100_000).encode("utf-8"), tmp_path / "out.png")