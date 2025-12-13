# mypy: ignore-errors

from unittest.mock import ANY, MagicMock, call, patch

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.injestion import (
    embed_chunks_and_Vector_storage,
    ingestion_process,
    load_pdf_files,
    split_text_into_chunks,
)


class TestLoadPdfFiles:
    """Test suite for load_pdf_files function."""

    @patch("app.injestion.PyPDFLoader")
    @patch("app.injestion.os.path.join")
    @patch("app.injestion.os.listdir")
    def test_load_pdf_files_single_pdf(self, mock_listdir, mock_join, mock_loader_class):
        """
        Test loading a single PDF file.
        Verifies that PyPDFLoader is called correctly and documents are returned.
        """
        # Arrange
        files_folder_path = "/test/path"
        mock_listdir.return_value = ["document1.pdf"]
        mock_join.return_value = "/test/path/document1.pdf"

        mock_loader_instance = MagicMock()
        mock_document = Document(page_content="Test content", metadata={"source": "document1.pdf"})
        mock_loader_instance.load.return_value = [mock_document]
        mock_loader_class.return_value = mock_loader_instance

        # Act
        result = load_pdf_files(files_folder_path)

        # Assert
        assert len(result) == 1
        assert result[0] == mock_document
        mock_listdir.assert_called_once_with(files_folder_path)
        mock_join.assert_called_once_with(files_folder_path, "document1.pdf")
        mock_loader_class.assert_called_once_with("/test/path/document1.pdf")
        mock_loader_instance.load.assert_called_once()

    @patch("app.injestion.PyPDFLoader")
    @patch("app.injestion.os.path.join")
    @patch("app.injestion.os.listdir")
    def test_load_pdf_files_multiple_pdfs(self, mock_listdir, mock_join, mock_loader_class):
        """
        Test loading multiple PDF files.
        Verifies that all PDFs are loaded and documents are combined.
        """
        # Arrange
        files_folder_path = "/test/path"
        mock_listdir.return_value = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]

        mock_join.side_effect = lambda path, file: f"{path}/{file}"

        mock_loader_instance = MagicMock()
        mock_doc1 = Document(page_content="Content 1", metadata={"source": "doc1.pdf"})
        mock_doc2 = Document(page_content="Content 2", metadata={"source": "doc2.pdf"})
        mock_doc3 = Document(page_content="Content 3", metadata={"source": "doc3.pdf"})

        mock_loader_instance.load.side_effect = [
            [mock_doc1],
            [mock_doc2],
            [mock_doc3]
        ]
        mock_loader_class.return_value = mock_loader_instance

        # Act
        result = load_pdf_files(files_folder_path)

        # Assert
        assert len(result) == 3
        assert result[0] == mock_doc1
        assert result[1] == mock_doc2
        assert result[2] == mock_doc3
        assert mock_loader_class.call_count == 3
        assert mock_loader_instance.load.call_count == 3

    @patch("app.injestion.PyPDFLoader")
    @patch("app.injestion.os.path.join")
    @patch("app.injestion.os.listdir")
    def test_load_pdf_files_filters_non_pdf_files(self, mock_listdir, mock_join, mock_loader_class):
        """
        Test that non-PDF files are filtered out.
        Verifies that only .pdf files are processed.
        """
        # Arrange
        files_folder_path = "/test/path"
        mock_listdir.return_value = ["doc1.pdf", "doc2.txt", "doc3.PDF", "doc4.pdf"]
        mock_join.side_effect = lambda path, file: f"{path}/{file}"

        mock_loader_instance = MagicMock()
        mock_doc1 = Document(page_content="Content 1", metadata={})
        mock_doc3 = Document(page_content="Content 3", metadata={})
        mock_doc4 = Document(page_content="Content 4", metadata={})

        mock_loader_instance.load.side_effect = [
            [mock_doc1],
            [mock_doc3],
            [mock_doc4]
        ]
        mock_loader_class.return_value = mock_loader_instance

        # Act
        result = load_pdf_files(files_folder_path)

        # Assert
        assert len(result) == 3
        assert mock_loader_class.call_count == 3
        # Verify PyPDFLoader was not called for .txt file
        calls = [
            call(files_folder_path, "doc1.pdf"),
            call(files_folder_path, "doc3.PDF"),
            call(files_folder_path, "doc4.pdf"),
        ]
        mock_join.assert_has_calls(calls, any_order=False)

    @patch("app.injestion.PyPDFLoader")
    @patch("app.injestion.os.path.join")
    @patch("app.injestion.os.listdir")
    def test_load_pdf_files_empty_directory(self, mock_listdir, mock_join, mock_loader_class):
        """
        Test loading from empty directory.
        Verifies that empty list is returned when no PDFs are found.
        """
        # Arrange
        files_folder_path = "/test/path"
        mock_listdir.return_value = []

        # Act
        result = load_pdf_files(files_folder_path)

        # Assert
        assert result == []
        mock_listdir.assert_called_once_with(files_folder_path)
        mock_loader_class.assert_not_called()


class TestSplitTextIntoChunks:
    """Test suite for split_text_into_chunks function."""

    @patch("app.injestion.RecursiveCharacterTextSplitter")
    def test_split_text_into_chunks_single_document(self, mock_splitter_class):
        """
        Test splitting a single document into chunks.
        Verifies that RecursiveCharacterTextSplitter is configured correctly.
        """
        # Arrange
        input_documents = [Document(page_content="Test content", metadata={"source": "doc.pdf"})]
        mock_splitter_instance = MagicMock()
        chunked_doc = Document(page_content="Chunked content", metadata={"source": "doc.pdf"})
        mock_splitter_instance.split_documents.return_value = [chunked_doc]
        mock_splitter_class.return_value = mock_splitter_instance

        # Act
        result = split_text_into_chunks(input_documents)

        # Assert
        assert len(result) == 1
        assert result[0] == chunked_doc
        mock_splitter_class.assert_called_once_with(chunk_size=1000, chunk_overlap=200)
        mock_splitter_instance.split_documents.assert_called_once_with(input_documents)

    @patch("app.injestion.RecursiveCharacterTextSplitter")
    def test_split_text_into_chunks_multiple_documents(self, mock_splitter_class):
        """
        Test splitting multiple documents into chunks.
        Verifies that all documents are processed.
        """
        # Arrange
        input_documents = [
            Document(page_content="Content 1", metadata={"source": "doc1.pdf"}),
            Document(page_content="Content 2", metadata={"source": "doc2.pdf"})
        ]
        mock_splitter_instance = MagicMock()
        chunked_docs = [
            Document(page_content="Chunk 1", metadata={"source": "doc1.pdf"}),
            Document(page_content="Chunk 2", metadata={"source": "doc1.pdf"}),
            Document(page_content="Chunk 3", metadata={"source": "doc2.pdf"})
        ]
        mock_splitter_instance.split_documents.return_value = chunked_docs
        mock_splitter_class.return_value = mock_splitter_instance

        # Act
        result = split_text_into_chunks(input_documents)

        # Assert
        assert len(result) == 3
        assert result == chunked_docs
        mock_splitter_instance.split_documents.assert_called_once_with(input_documents)

    @patch("app.injestion.RecursiveCharacterTextSplitter")
    def test_split_text_into_chunks_empty_list(self, mock_splitter_class):
        """
        Test splitting empty document list.
        Verifies that empty list is handled correctly.
        """
        # Arrange
        input_documents = []
        mock_splitter_instance = MagicMock()
        mock_splitter_instance.split_documents.return_value = []
        mock_splitter_class.return_value = mock_splitter_instance

        # Act
        result = split_text_into_chunks(input_documents)

        # Assert
        assert result == []
        mock_splitter_instance.split_documents.assert_called_once_with([])


class TestEmbedChunksAndVectorStorage:
    """Test suite for embed_chunks_and_Vector_storage function."""

    @patch("app.injestion.Chroma")
    @patch("app.injestion.OpenAIEmbeddings")
    def test_embed_chunks_and_vector_storage_success(self, mock_embeddings_class, mock_chroma_class):
        """
        Test embedding chunks and storing in vector database.
        Verifies that OpenAIEmbeddings and Chroma.from_documents are called correctly.
        """
        # Arrange
        chunked_documents = [
            Document(page_content="Chunk 1", metadata={"source": "doc1.pdf"}),
            Document(page_content="Chunk 2", metadata={"source": "doc1.pdf"})
        ]
        mock_embeddings_instance = MagicMock()
        mock_embeddings_class.return_value = mock_embeddings_instance

        mock_vector_db = MagicMock(spec=Chroma)
        mock_chroma_class.from_documents.return_value = mock_vector_db

        # Act
        result = embed_chunks_and_Vector_storage(chunked_documents)

        # Assert
        assert result == mock_vector_db
        mock_embeddings_class.assert_called_once_with(model="text-embedding-3-small")
        mock_chroma_class.from_documents.assert_called_once_with(
            documents=chunked_documents,
            embedding=mock_embeddings_instance,
            persist_directory=ANY,
        )

    @patch("app.injestion.Chroma")
    @patch("app.injestion.OpenAIEmbeddings")
    def test_embed_chunks_and_vector_storage_empty_chunks(self, mock_embeddings_class, mock_chroma_class):
        """
        Test embedding empty chunk list.
        Verifies that function handles empty input correctly.
        """
        # Arrange
        chunked_documents = []
        mock_embeddings_instance = MagicMock()
        mock_embeddings_class.return_value = mock_embeddings_instance

        mock_vector_db = MagicMock(spec=Chroma)
        mock_chroma_class.from_documents.return_value = mock_vector_db

        # Act
        result = embed_chunks_and_Vector_storage(chunked_documents)

        # Assert
        assert result == mock_vector_db
        mock_chroma_class.from_documents.assert_called_once_with(
            documents=[],
            embedding=mock_embeddings_instance,
            persist_directory=ANY,
        )


class TestIngestionProcess:
    """Test suite for ingestion_process function."""

    @patch("app.injestion.embed_chunks_and_Vector_storage")
    @patch("app.injestion.split_text_into_chunks")
    @patch("app.injestion.load_pdf_files")
    def test_ingestion_process_success(self, mock_load_pdf, mock_split_chunks, mock_embed_storage):
        """
        Test complete ingestion process.
        Verifies that all functions are called in correct order with correct parameters.
        """
        # Arrange
        mock_pdf_docs = [
            Document(page_content="Content 1", metadata={"source": "doc1.pdf"}),
            Document(page_content="Content 2", metadata={"source": "doc2.pdf"})
        ]
        mock_chunked_docs = [
            Document(page_content="Chunk 1", metadata={"source": "doc1.pdf"}),
            Document(page_content="Chunk 2", metadata={"source": "doc1.pdf"})
        ]
        mock_vector_db = MagicMock(spec=Chroma)

        mock_load_pdf.return_value = mock_pdf_docs
        mock_split_chunks.return_value = mock_chunked_docs
        mock_embed_storage.return_value = mock_vector_db

        # Act
        result = ingestion_process()

        # Assert
        assert result == mock_vector_db
        mock_load_pdf.assert_called_once()
        mock_split_chunks.assert_called_once_with(mock_pdf_docs)
        mock_embed_storage.assert_called_once_with(mock_chunked_docs)

    @patch("app.injestion.embed_chunks_and_Vector_storage")
    @patch("app.injestion.split_text_into_chunks")
    @patch("app.injestion.load_pdf_files")
    def test_ingestion_process_empty_pdfs(self, mock_load_pdf, mock_split_chunks, mock_embed_storage):
        """
        Test ingestion process with no PDF files found.
        Verifies that process handles empty input gracefully.
        """
        # Arrange
        mock_load_pdf.return_value = []
        mock_split_chunks.return_value = []
        mock_vector_db = MagicMock(spec=Chroma)
        mock_embed_storage.return_value = mock_vector_db

        # Act
        result = ingestion_process()

        # Assert
        assert result == mock_vector_db
        mock_load_pdf.assert_called_once()
        mock_split_chunks.assert_called_once_with([])
        mock_embed_storage.assert_called_once_with([])
