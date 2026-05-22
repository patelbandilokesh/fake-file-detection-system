import os
import hashlib

EXTENSION_MAP = {
    "jpeg": [".jpg", ".jpeg"],
    "png": [".png"],
    "gif": [".gif"],
    "pdf": [".pdf"],
    "zip": [".zip", ".docx", ".pptx", ".xlsx"],
    "exe": [".exe"],
    "elf": [".elf"],
    "mp3": [".mp3"],
}


# -------------------------
# HASH
# -------------------------
def sha512_file(path):
    h = hashlib.sha512()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)

    return h.hexdigest()


# -------------------------
# STREAM
# -------------------------
def read_stream(path):

    with open(path, "rb") as f:
        while True:
            data = f.read(4096)

            if not data:
                break

            yield data


# -------------------------
# MAIN ANALYZER
# -------------------------
def analyze_file(filepath):

    result = {}

    # 🔐 HASH
    file_hash = sha512_file(filepath)
    result["hash"] = file_hash

    # 📂 EXTENSION
    ext = os.path.splitext(filepath)[1].lower()
    result["extension"] = ext

    # 🔍 MIME
    mime = "unknown"

    if ext in [".jpg", ".jpeg"]:
        mime = "jpeg"

    elif ext == ".png":
        mime = "png"

    elif ext == ".gif":
        mime = "gif"

    elif ext == ".pdf":
        mime = "pdf"

    elif ext in [".zip", ".docx", ".pptx", ".xlsx"]:
        mime = "zip"

    elif ext == ".mp3":
        mime = "mp3"

    result["mime"] = mime

    # 📄 HEADER
    with open(filepath, "rb") as f:
        header = f.read(16)

    # -------------------------
    # 🔴 HARMFUL
    # -------------------------
    if header.startswith(b"MZ") or header.startswith(b"\x7fELF"):
        result["status"] = "Harmful"
        return result

    if ext in [".bat", ".cmd", ".ps1", ".sh", ".js"]:
        result["status"] = "Harmful"
        return result

    # -------------------------
    # FILE TYPE
    # -------------------------
    file_type = "unknown"

    if header.startswith(b"\xff\xd8\xff"):
        file_type = "jpeg"

    elif header.startswith(b"\x89PNG"):
        file_type = "png"

    elif header.startswith(b"GIF"):
        file_type = "gif"

    elif header.startswith(b"%PDF"):
        file_type = "pdf"

    elif header.startswith(b"PK\x03\x04"):
        file_type = "zip"

    elif header.startswith(b"ID3"):
        file_type = "mp3"

    else:
        result["status"] = "Fake"
        return result

    result["file_type"] = file_type

    # -------------------------
    # PDF VALIDATION
    # -------------------------
    if file_type == "pdf":

        obj = 0
        xref = False
        trailer = False
        eof = False
        malicious = False

        for chunk in read_stream(filepath):

            low = chunk.lower()

            obj += low.count(b"obj")

            if b"xref" in low:
                xref = True

            if b"trailer" in low:
                trailer = True

            if b"%%eof" in low:
                eof = True

            if b"/javascript" in low or b"/launch" in low:
                malicious = True

        if not (xref and trailer and eof) or obj < 3:
            result["status"] = "Fake"
            return result

        if malicious:
            result["status"] = "Harmful"
            return result

    # -------------------------
    # EXTENSION CHECK
    # -------------------------
    if ext not in EXTENSION_MAP.get(file_type, []):
        result["status"] = "Fake"
        return result

    # -------------------------
    # MIME CHECK
    # -------------------------
    if file_type != mime:
        result["status"] = "Fake"
        return result

    # -------------------------
    # CONTENT SCAN
    # -------------------------
    suspicious = [
        b"powershell",
        b"cmd.exe",
        b"/bin/bash",
        b"<script>",
        b"eval("
    ]

    for chunk in read_stream(filepath):

        if any(s in chunk.lower() for s in suspicious):
            result["status"] = "Harmful"
            return result

    # -------------------------
    # FINAL
    # -------------------------
    result["status"] = "Genuine"

    return result
