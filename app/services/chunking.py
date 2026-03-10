def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def chunk_pages(pages, chunk_size=500, overlap=50):
    """
    Chunk text from pages, preserving page metadata.
    
    Args:
        pages: List of (page_text, page_num)
        chunk_size: Size of each chunk
        overlap: Overlap between chunks
    
    Returns:
        List of (chunk, metadata_dict)
    """
    chunks_with_meta = []
    for page_text, page_num in pages:
        chunks = chunk_text(page_text, chunk_size, overlap)
        for chunk in chunks:
            metadata = {
                "source": "",  # Will be set in upload
                "page": page_num
            }
            chunks_with_meta.append((chunk, metadata))
    return chunks_with_meta
