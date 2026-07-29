# subpixel

Python CLI that hides encrypted messages in an image's least-significant bits.

> **Status:** v1.0.0. LSB embed/extract, AES-256-GCM encryption with
> Argon2id key derivation, and CLI error handling are all in place.

## Install

    git clone https://github.com/<you>/subpixel
    cd subpixel
    python3 -m venv .venv && source .venv/bin/activate
    pip install -e .

## Usage

    subpixel encode -i cover.png -m "meet at noon" -o out.png
    subpixel decode -i out.png

Both commands prompt for a password interactively (never passed as a flag,
so it never ends up in shell history or `ps aux` output). The same password
used to encode must be used to decode.

Output is always PNG. Lossy formats (JPEG) destroy the embedded bits.

## How it works

**Embedding.** Each RGB channel is one byte. Overwriting its least-significant
bit shifts the value by at most 1 — imperceptible to the eye, but it gives
you one bit of storage per channel, so three bits per pixel.

**Encryption.** Before embedding, the message is encrypted with AES-256-GCM.
The key is derived from your password with Argon2id (memory-hard, resistant
to GPU/ASIC brute-forcing) and a fresh random salt on every run — same
password, different ciphertext every time. GCM also produces an authentication
tag, so any tampering with the embedded data — or a wrong password — is
detected and rejected outright rather than silently decrypting to garbage.

The encrypted blob is laid out as:

    salt (16 bytes) || nonce (12 bytes) || ciphertext || tag (16 bytes)

That blob is what actually gets embedded, using a 4-byte big-endian length
header followed by the blob itself. The decoder reads the header first,
which tells it exactly how many more bits to pull — no delimiter needed,
so the scheme stays safe for arbitrary binary payloads.

## Limitations

- Hides data from casual inspection only. Sequential LSB embedding is
  detectable by standard steganalysis (chi-square, RS analysis) — this tool
  protects message *confidentiality* via encryption, not the *existence* of
  a hidden message.
- Requires a lossless cover format.
- Capacity is bounded by cover image size (3 bits/pixel); oversized messages
  are rejected with a clear error before embedding is attempted.

## Development

    pip install -e ".[dev]"
    pytest -v