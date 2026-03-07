"""
Logistics Document Detection Service

Detects if a document is logistics-related by checking for logistics keywords.
"""

LOGISTICS_KEYWORDS = {
    "shipment",
    "consignee",
    "shipper",
    "cargo",
    "container",
    "port",
    "bill of lading",
    "invoice",
    "packing list",
    "freight",
    "customs",
    "delivery",
    "logistics",
    "transport",
    "tracking",
    "warehouse",
    "distribution",
    "origin",
    "destination",
    "receiver",
    "sender",
    "goods",
    "package",
    "shipment number",
    "awb",
    "hs code",
    "tariff",
}


def detect_logistics_document(text: str) -> bool:
    """
    Detect if document contains logistics-related content.
    
    Checks the provided text against a set of logistics keywords.
    Returns True if at least one keyword is found.
    
    Args:
        text (str): The extracted text from the document.
    
    Returns:
        bool: True if logistics keywords detected, False otherwise.
    """
    if not text:
        return False
    
    # Convert text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Check if any logistics keyword appears in the text
    for keyword in LOGISTICS_KEYWORDS:
        if keyword in text_lower:
            return True
    
    return False


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
