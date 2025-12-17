# mypy: ignore-errors

import pytest

from langchain_core.documents import Document

from app.injestion import (
    embed_chunks_and_Vector_storage,
    ingestion_process,
    load_pdf_files,
    split_text_into_chunks,
)


# ---------------------------------------------------------------------------
# Fixtures for load_pdf_files
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_listdir(monkeypatch):
    def _apply(files):
        monkeypatch.setattr("app.injestion.os.listdir", lambda _: files)
    return _apply


@pytest.fixture
def mock_join(monkeypatch):
    monkeypatch.setattr(
        "app.injestion.os.path.join",
        lambda path, file: f"{path}/{file}",
    )


@pytest.fixture
def mock_pdf_loader(monkeypatch):
    created_loaders = []

    class FakeLoader:
        def __init__(self, path):
            self.path = path
            created_loaders.append(self)

        def load(self):
            return [
                Document(
                    page_content="Test content",
                    metadata={"source": self.path},
                )
            ]

    monkeypatch.setattr("app.injestion.PyPDFLoader", FakeLoader)
    return created_loaders


# ---------------------------------------------------------------------------
# Tests: load_pdf_files
# ---------------------------------------------------------------------------

def test_load_pdf_files_single_pdf(mock_listdir, mock_join, mock_pdf_loader):
    mock_listdir(["document1.pdf"])

    result = load_pdf_files("/test/path")

    assert len(result) == 1
    assert result[0].page_content == "Test content"
    assert len(mock_pdf_loader) == 1


def test_load_pdf_files_multiple_pdfs(mock_listdir, mock_join, mock_pdf_loader):
    mock_listdir(["doc1.pdf", "doc2.pdf", "doc3.pdf"])

    result = load_pdf_files("/test/path")

    assert len(result) == 3
    assert len(mock_pdf_loader) == 3


def test_load_pdf_files_filters_non_pdf_files(mock_listdir, mock_join, mock_pdf_loader):
    mock_listdir(["doc1.pdf", "doc2.txt", "doc3.PDF", "doc4.pdf"])

    result = load_pdf_files("/test/path")

    assert len(result) == 3
    assert len(mock_pdf_loader) == 3


def test_load_pdf_files_empty_directory(mock_listdir):
    mock_listdir([])

    result = load_pdf_files("/test/path")

    assert result == []


# ---------------------------------------------------------------------------
# Fixtures for split_text_into_chunks
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_text_splitter(monkeypatch):
    class FakeSplitter:
        def __init__(self, chunk_size, chunk_overlap):
            self.chunk_size = chunk_size
            self.chunk_overlap = chunk_overlap

        def split_documents(self, docs):
            return docs

    monkeypatch.setattr(
        "app.injestion.RecursiveCharacterTextSplitter",
        FakeSplitter,
    )


# ---------------------------------------------------------------------------
# Tests: split_text_into_chunks
# ---------------------------------------------------------------------------

def test_split_text_into_chunks_single_document(mock_text_splitter):
    docs = [Document(page_content="Test content", metadata={})]

    result = split_text_into_chunks(docs)

    assert result == docs


def test_split_text_into_chunks_multiple_documents(mock_text_splitter):
    docs = [
        Document(page_content="Content 1", metadata={}),
        Document(page_content="Content 2", metadata={}),
    ]

    result = split_text_into_chunks(docs)

    assert result == docs


def test_split_text_into_chunks_empty_list(mock_text_splitter):
    result = split_text_into_chunks([])

    assert result == []


# ---------------------------------------------------------------------------
# Fixtures for embed_chunks_and_Vector_storage
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_embeddings(monkeypatch):
    class FakeEmbeddings:
        def __init__(self, model):
            self.model = model

    monkeypatch.setattr("app.injestion.OpenAIEmbeddings", FakeEmbeddings)


@pytest.fixture
def mock_chroma(monkeypatch):
    class FakeChroma:
        pass

    def fake_from_documents(documents, embedding, persist_directory):
        return FakeChroma()

    monkeypatch.setattr("app.injestion.Chroma.from_documents", fake_from_documents)
    return FakeChroma


# ---------------------------------------------------------------------------
# Tests: embed_chunks_and_Vector_storage
# ---------------------------------------------------------------------------

def test_embed_chunks_and_vector_storage_success(mock_embeddings, mock_chroma):
    chunks = [
        Document(page_content="Chunk 1", metadata={}),
        Document(page_content="Chunk 2", metadata={}),
    ]

    result = embed_chunks_and_Vector_storage(chunks)

    assert isinstance(result, mock_chroma)


def test_embed_chunks_and_vector_storage_empty_chunks(mock_embeddings, mock_chroma):
    result = embed_chunks_and_Vector_storage([])

    assert isinstance(result, mock_chroma)


# ---------------------------------------------------------------------------
# Tests: ingestion_process
# ---------------------------------------------------------------------------

def test_ingestion_process_success(monkeypatch):
    pdfs = [Document(page_content="PDF", metadata={})]
    chunks = [Document(page_content="Chunk", metadata={})]
    vector_db = object()

    monkeypatch.setattr(
        "app.injestion.load_pdf_files",
        lambda _path: pdfs,   # ✅ accept argument
    )
    monkeypatch.setattr(
        "app.injestion.split_text_into_chunks",
        lambda docs: chunks,
    )
    monkeypatch.setattr(
        "app.injestion.embed_chunks_and_Vector_storage",
        lambda docs: vector_db,
    )

    result = ingestion_process()

    assert result is vector_db



def test_ingestion_process_empty_pdfs(monkeypatch):
    vector_db = object()

    monkeypatch.setattr(
        "app.injestion.load_pdf_files",
        lambda _path: [],   # ✅ accept argument
    )
    monkeypatch.setattr(
        "app.injestion.split_text_into_chunks",
        lambda docs: [],
    )
    monkeypatch.setattr(
        "app.injestion.embed_chunks_and_Vector_storage",
        lambda docs: vector_db,
    )

    result = ingestion_process()

    assert result is vector_db

