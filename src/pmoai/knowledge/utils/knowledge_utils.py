from typing import List


def split_text_into_chunks(
    text: str, chunk_size: int = 1000, chunk_overlap: int = 200
) -> List[str]:
    """
    Split text into chunks of a specified size with overlap.

    Args:
        text: The text to split.
        chunk_size: The size of each chunk.
        chunk_overlap: The overlap between chunks.

    Returns:
        A list of text chunks.
    """
    if not text:
        return []

    # Split text into paragraphs
    paragraphs = text.split("\n\n")
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    chunks = []
    current_chunk = []
    current_size = 0

    for paragraph in paragraphs:
        # If adding this paragraph would exceed the chunk size,
        # save the current chunk and start a new one
        paragraph_size = len(paragraph)
        if current_size + paragraph_size > chunk_size and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            
            # Keep some paragraphs for overlap
            overlap_size = 0
            overlap_paragraphs = []
            for p in reversed(current_chunk):
                if overlap_size + len(p) <= chunk_overlap:
                    overlap_paragraphs.insert(0, p)
                    overlap_size += len(p)
                else:
                    break
            
            current_chunk = overlap_paragraphs
            current_size = overlap_size
        
        current_chunk.append(paragraph)
        current_size += paragraph_size
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))
    
    return chunks
