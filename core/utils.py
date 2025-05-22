import re

def normalize_answer(answer):
    """Normalize answer text for comparison by removing formatting and extra whitespace"""
    if not answer:
        return ""
    
    # Remove markdown formatting (bold, italic, etc.)
    normalized = re.sub(r'\*\*([^*]+)\*\*', r'\1', answer)  # Remove **text**
    normalized = re.sub(r'\*([^*]+)\*', r'\1', normalized)   # Remove *text*
    normalized = re.sub(r'_([^_]+)_', r'\1', normalized)     # Remove _text_
    
    # Remove extra whitespace and newlines
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    # Remove leading/trailing punctuation that might be artifacts
    normalized = normalized.strip('.,!?;:')
    
    # Convert to lowercase for case-insensitive comparison
    normalized = normalized.lower()
    
    # Enhanced semantic normalization for common financial/business terms
    
    # Handle frequency/time period equivalences
    frequency_mappings = {
        'quarterly': '4',
        'four times a year': '4',
        '4 times a year': '4',
        'four times per year': '4',
        '4 times per year': '4',
        'every quarter': '4',
        'every 3 months': '4',
        'semi-annually': '2',
        'twice a year': '2',
        '2 times a year': '2',
        'twice per year': '2',
        '2 times per year': '2',
        'every 6 months': '2',
        'annually': '1',
        'once a year': '1',
        '1 time a year': '1',
        'yearly': '1',
        'monthly': '12',
        '12 times a year': '12',
        'twelve times a year': '12'
    }
    
    # Handle percentage equivalences
    percentage_mappings = {
        'fifty percent': '50%',
        'twenty-five percent': '25%',
        'ten percent': '10%',
        'five percent': '5%',
        'one percent': '1%',
        'zero percent': '0%'
    }
    
    # Handle number word equivalences
    number_mappings = {
        'zero': '0',
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
        'ten': '10',
        'eleven': '11',
        'twelve': '12',
        'thirteen': '13',
        'fourteen': '14',
        'fifteen': '15',
        'sixteen': '16',
        'seventeen': '17',
        'eighteen': '18',
        'nineteen': '19',
        'twenty': '20'
    }
    
    # Apply mappings
    for phrase, standardized in frequency_mappings.items():
        if phrase in normalized:
            normalized = standardized
            break
    
    for phrase, standardized in percentage_mappings.items():
        if phrase in normalized:
            normalized = standardized
            break
    
    for word, number in number_mappings.items():
        if normalized == word:
            normalized = number
            break
    
    # Clean up common phrases that don't add value
    cleanup_patterns = [
        r'^the answer is\s*',
        r'^the correct answer is\s*',
        r'^answer:\s*',
        r'^correct answer:\s*',
        r'^based on.*?the.*?answer is\s*',
        r'^according to.*?the.*?answer is\s*',
        r'\..*$',  # Remove everything after first period
    ]
    
    for pattern in cleanup_patterns:
        normalized = re.sub(pattern, '', normalized, flags=re.IGNORECASE)
    
    # Final cleanup
    normalized = normalized.strip('.,!?;: ')
    
    # Extract just the core answer if it's a letter choice (A, B, C, D, etc.)
    letter_match = re.search(r'\b([a-e])\b', normalized)
    if letter_match:
        normalized = letter_match.group(1)
    
    # Extract just numbers if the answer appears to be numeric
    number_match = re.search(r'\b(\d+(?:\.\d+)?%?)\b', normalized)
    if number_match and len(normalized.split()) > 1:
        normalized = number_match.group(1)
    
    return normalized 