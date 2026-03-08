"""
Logistics Document Detection Service

Detects if a document is logistics-related by checking for logistics keywords.
"""

LOGISTICS_KEYWORDS = {
    "bill of lading",
    "consignee",
    "shipper",
    "container number",
    "port of discharge",
    "cargo",
    "shipment",
    "vessel",
    "freight",
    "hs code",
    "packing list",
    "invoice"
}


def detect_logistics_document(text: str) -> bool:
    """
    Detect if document contains logistics-related content.
    
    Counts logistics keywords in the text. Returns True if at least 3 keywords are found.
    
    Args:
        text (str): The extracted text from the document.
    
    Returns:
        bool: True if at least 3 logistics keywords detected, False otherwise.
    """
    if not text:
        return False
    
    # Convert text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Count how many logistics keywords appear
    keyword_count = 0
    for keyword in LOGISTICS_KEYWORDS:
        if keyword in text_lower:
            keyword_count += 1
    
    return keyword_count >= 3


def extract_preview(text: str, max_chars: int = 500) -> str:
    """
    Extract a preview of the document content.
    
    Args:
        text (str): The extracted text from the document.
        max_chars (int): Maximum number of characters in preview.
    
    Returns:
        str: First `max_chars` characters of the text.
    """
    if not text:
        return ""
    
    preview = text[:max_chars].strip()
    if len(text) > max_chars:
        preview += "..."
    
    return preview
