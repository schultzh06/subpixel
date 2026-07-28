from pathlib import Path

import pytest

from subpixel import embed, extract
from subpixel.errors import MessageTooLargeError

FIXTURES = Path(__file__).parent / "fixtures"


def test_round_trip(tmp_path):
    out = tmp_path / "out.png"
    embed(FIXTURES / "cover.png", "hello world", out)
    assert extract(out) == "hello world"


def test_multibyte(tmp_path):
    msg = "héllo 😛😛😛😛😛😛"
    out = tmp_path / "out.png"
    embed(FIXTURES / "cover.png", msg, out)
    assert extract(out) == msg


def test_image_actually_changes(tmp_path):
    out = tmp_path / "out.png"
    embed(FIXTURES / "cover.png", "hello world", out)
    assert out.read_bytes() != (FIXTURES / "cover.png").read_bytes()


def test_too_large(tmp_path):
    with pytest.raises(MessageTooLargeError):
        embed(FIXTURES / "tiny.png", "x" * 100_000, tmp_path / "out.png")