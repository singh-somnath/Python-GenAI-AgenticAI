"""Document loading pipeline: parse -> normalize -> chunk -> enrich metadata."""

from __future__ import annotations

import hashlib
import logging
import re
import unicodedata
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from math import ceil
from pathlib import Path

from langchain_community.document_loaders import (
    BSHTMLLoader,
    CSVLoader,
    PyPDFLoader,
    TextLoader,
)
from langchain_core.documents import Document
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

logger = logging.getLogger(__name__)

MARKDOWN_EXTENSIONS = {".md", ".markdown"}

MARKDOWN_HEADERS = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
    ("####", "h4"),
    ("#####", "h5"),
    ("######", "h6"),
]

_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_INLINE_SPACES = re.compile(r"[^\S\n]+")
_MULTI_BLANK_LINES = re.compile(r"\n{3,}")
_HYPHEN_LINE_BREAK = re.compile(r"(?<=\w)-\n(?=\w)")


@dataclass(frozen=True)
class ChunkingConfig:
    """Knobs for the chunking stage."""

    chunk_size: int = 500
    chunk_overlap: int = 100
    min_chunk_chars: int = 40
    use_token_chunking: bool = True
    tiktoken_encoding: str = "cl100k_base"

    def __post_init__(self) -> None:
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")


# --------------------------------------------------------------------------- #
# Text cleaning
# --------------------------------------------------------------------------- #


def count_tokens(text: str) -> int:
    """Token count, falling back to word count when tiktoken is unavailable."""
    try:
        import tiktoken

        return len(tiktoken.get_encoding("cl100k_base").encode(text))
    except Exception:  # noqa: BLE001
        return len(text.split())


def normalize_text(text: str) -> str:
    """Fix unicode glitches, hyphenated line breaks and messy whitespace."""
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u00ad", "").replace("\u200b", "")
    text = _HYPHEN_LINE_BREAK.sub("", text)
    text = _CONTROL_CHARS.sub(" ", text)
    text = _INLINE_SPACES.sub(" ", text.replace("\t", " "))
    text = "\n".join(line.strip() for line in text.split("\n"))
    return _MULTI_BLANK_LINES.sub("\n\n", text).strip()


# --------------------------------------------------------------------------- #
# Parsers - one function per file type
# --------------------------------------------------------------------------- #


def load_text_file(path: Path) -> list[Document]:
    """Text files, with encoding auto-detection."""
    return TextLoader(str(path), encoding="utf-8", autodetect_encoding=True).load()


def load_pdf_file(path: Path) -> list[Document]:
    """One Document per page, with headers/footers repeated on almost every page removed."""
    pages = PyPDFLoader(str(path), mode="page").load()
    if len(pages) < 3:
        return pages

    line_counts = Counter(
        stripped
        for page in pages
        for stripped in {
            line.strip().casefold() for line in page.page_content.split("\n")
        }
        if 0 < len(stripped) <= 120
    )
    threshold = max(3, ceil(0.9 * len(pages)))
    repeated = {line for line, count in line_counts.items() if count >= threshold}

    kept_pages = []
    for page in pages:
        lines = [
            line
            for line in page.page_content.split("\n")
            if line.strip().casefold() not in repeated
        ]
        if "\n".join(lines).strip():
            page.page_content = "\n".join(lines)
            kept_pages.append(page)
    if repeated:
        logger.info("Removed %d repeated page lines from %s", len(repeated), path.name)
    return kept_pages


def load_markdown_file(path: Path) -> list[Document]:
    """Markdown is read as-is; headings are handled by the chunker."""
    return [
        Document(
            page_content=path.read_text(encoding="utf-8", errors="replace"),
            metadata={"source": str(path)},
        )
    ]


def load_html_file(path: Path) -> list[Document]:
    """HTML pages, keeping the parsed <title> in metadata."""
    return BSHTMLLoader(str(path), open_encoding="utf-8").load()


def load_csv_file(path: Path) -> list[Document]:
    """One Document per row, with column names inline."""
    return CSVLoader(str(path), autodetect_encoding=True).load()


PARSERS: dict[str, Callable[[Path], list[Document]]] = {
    ".txt": load_text_file,
    ".log": load_text_file,
    ".text": load_text_file,
    ".rst": load_text_file,
    ".md": load_markdown_file,
    ".markdown": load_markdown_file,
    ".html": load_html_file,
    ".htm": load_html_file,
    ".csv": load_csv_file,
    ".pdf": load_pdf_file,
}


# --------------------------------------------------------------------------- #
# Chunking
# --------------------------------------------------------------------------- #


def split_chunks(
    documents: list[Document],
    is_markdown: bool,
    config: ChunkingConfig,
) -> list[Document]:
    """Split documents on paragraph/sentence boundaries; markdown also splits on headings."""
    separators = ["\n\n", "\n", ". ", " ", ""]
    if config.use_token_chunking:
        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            encoding_name=config.tiktoken_encoding,
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=separators,
            add_start_index=True,
        )
    else:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=separators,
            add_start_index=True,
        )

    if not is_markdown:
        return splitter.split_documents(documents)

    heading_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=MARKDOWN_HEADERS,
        strip_headers=False,
    )
    chunks: list[Document] = []
    for doc in documents:
        for section in heading_splitter.split_text(doc.page_content):
            metadata = {**doc.metadata, **section.metadata}
            trail = [
                section.metadata[key]
                for _, key in MARKDOWN_HEADERS
                if section.metadata.get(key)
            ]
            if trail:
                metadata["section"] = " > ".join(trail)
            content = Document(page_content=section.page_content, metadata=metadata)
            chunks.extend(splitter.split_documents([content]))
    return chunks


# --------------------------------------------------------------------------- #
# Metadata
# --------------------------------------------------------------------------- #


def file_metadata(path: Path) -> dict:
    """Fingerprint of the source file, attached to every chunk of that file."""
    stat = path.stat()
    return {
        "source": str(path),
        "file_path": str(path.resolve()),
        "file_name": path.name,
        "file_ext": path.suffix.lower(),
        "file_size_bytes": stat.st_size,
        "file_hash": hashlib.sha256(path.read_bytes()).hexdigest()[:16],
        "doc_type": path.suffix.lower().lstrip("."),
        "title": re.sub(r"\s+", " ", re.sub(r"[_\-.]+", " ", path.stem)).strip(),
        "modified_at": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(
            timespec="seconds"
        ),
        "loaded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def enrich_chunks(chunks: list[Document], config: ChunkingConfig) -> list[Document]:
    """Number every chunk, add size metrics and drop tiny fragments."""
    per_doc_total = Counter(chunk.metadata["docID"] for chunk in chunks)
    per_doc_seen: Counter[int] = Counter()
    kept: list[Document] = []

    for chunk in chunks:
        content = chunk.page_content.strip()
        doc_id = chunk.metadata["docID"]
        # a document that never split yields one chunk - keep it even if short
        if len(content) < config.min_chunk_chars and per_doc_total[doc_id] > 1:
            continue

        per_doc_seen[doc_id] += 1
        chunk.page_content = content
        chunk.metadata["chunkID"] = f"{doc_id}_{per_doc_seen[doc_id]}"
        chunk.metadata["chunk_index"] = per_doc_seen[doc_id]
        chunk.metadata["chunk_count"] = per_doc_total[doc_id]
        chunk.metadata["chunk_seq"] = len(kept) + 1
        chunk.metadata["char_count"] = len(content)
        chunk.metadata["token_count"] = count_tokens(content)
        kept.append(chunk)

    return kept


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #


def getDocumentsChunks(
    data_dir: str | Path = "./data",
    config: ChunkingConfig | None = None,
) -> list[Document]:
    """Load every supported file in data_dir and return chunks ready for retrieval."""
    config = config or ChunkingConfig()
    root = Path(data_dir)
    if not root.is_dir():
        raise FileNotFoundError(f"data directory not found: {root}")

    files = sorted(
        p for p in root.iterdir() if p.is_file() and not p.name.startswith(".")
    )
    chunks: list[Document] = []
    doc_id = 0

    for path in files:
        parser = PARSERS.get(path.suffix.lower())
        if parser is None:
            logger.warning("Skipping unsupported file: %s", path)
            continue

        try:
            documents = []
            for doc in parser(path):
                doc.page_content = normalize_text(doc.page_content)
                if doc.page_content:
                    documents.append(doc)
        except Exception:  # noqa: BLE001 - one broken file must not stop ingestion
            logger.exception("Failed to load %s", path)
            continue

        if not documents:
            logger.warning("No usable content in %s", path)
            continue

        info = file_metadata(path)
        for doc in documents:
            doc_id += 1
            doc.metadata.update(info)
            doc.metadata["docID"] = doc_id
            if isinstance(doc.metadata.get("page"), int):
                doc.metadata["page_number"] = doc.metadata["page"] + 1

        is_markdown = path.suffix.lower() in MARKDOWN_EXTENSIONS
        chunks.extend(split_chunks(documents, is_markdown, config))

    enriched = enrich_chunks(chunks, config)
    logger.info(
        "Ingested %d chunks from %d documents in %s", len(enriched), doc_id, root
    )
    if not enriched:
        logger.warning("No chunks produced from %s", root)
    return enriched
