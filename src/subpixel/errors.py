class SubpixelError(Exception):
    """Base class for all subpixel errors."""


class MessageTooLargeError(SubpixelError):
    """Payload exceeds the cover image's capacity."""


class CorruptPayloadError(SubpixelError):
    """Bit stream ended mid-payload, or the header is invalid."""