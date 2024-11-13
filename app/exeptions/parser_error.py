class ParserError(Exception):
    """Base exception for parser-related errors"""
    pass

class ParsingError(ParserError):
    """Raised when parsing an article fails"""
    pass