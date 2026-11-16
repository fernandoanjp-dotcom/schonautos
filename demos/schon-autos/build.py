#!/usr/bin/env python3
"""Publish the approved Schon Autos demos without changing their HTML bytes."""
from __future__ import annotations

import hashlib
import io
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "public"
ARCHIVE_SHA256 = "2be72f57e3c05edc8ff4e00254bb49f2cfe7ee2260a3a31393a5c309369ae6e5"
FILES = {
    "index.html": ("index.html", "453c614d0f5ac489a9dd744683f5406c5d4c2b3203889840c1df6f52a854abd3"),
    "editorial.html": ("editorial/index.html", "1f6ebda83679339569228b454939f9f166797e9292778063693e001f163b123b"),
    "ia.html": ("ia/index.html", "4eae674bf249ae1f39e3d122493e9a9befa53ba3de3542369bcfce71fd2a1c10"),
}


def main() -> None:
    parts = [ROOT / "source" / ("site.tar.xz.%02d" % i) for i in range(3)]
    archive = b"".join(part.read_bytes() for part in parts)
    if hashlib.sha256(archive).hexdigest() != ARCHIVE_SHA256:
        raise RuntimeError("Source archive integrity check failed")
    output_files = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:xz") as package:
        members = package.getmembers()
        if len(members) != len(FILES) or {m.name for m in members} != set(FILES):
            raise RuntimeError("Unexpected archive contents")
        for member in members:
            if not member.isfile():
                raise RuntimeError("Only regular HTML files are allowed")
            dest, expected = FILES[member.name]
            stream = package.extractfile(member)
            if stream is None:
                raise RuntimeError("Missing file in archive")
            content = stream.read()
            if hashlib.sha256(content).hexdigest() != expected:
                raise RuntimeError("HTML integrity check failed: " + member.name)
            if b'noindex,nofollow' not in content:
                raise RuntimeError("Demo indexing protection is missing")
            output_files[dest] = content
    output_files["robots.txt"] = b"User-agent: *\nDisallow: /\n"
    OUTPUT.mkdir(parents=True, exist_ok=True)
    existing = {str(p.relative_to(OUTPUT)) for p in OUTPUT.rglob("*") if p.is_file()}
    if existing - set(output_files):
        raise RuntimeError("Unexpected files in the isolated publish directory")
    for dest, content in output_files.items():
        path = OUTPUT / dest
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        print("Verified:", dest, len(content), "bytes", hashlib.sha256(content).hexdigest())
    print("Ready: comparator, editorial, IA. No other project files are published.")


if __name__ == "__main__":
    main()
