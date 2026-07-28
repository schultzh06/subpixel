"""subpixel: hide messages in the least-significant bits of images."""

from .stego import embed, extract

__all__ = ["embed", "extract"]
__version__ = "0.1.0"