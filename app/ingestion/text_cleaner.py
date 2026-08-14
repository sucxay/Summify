import re 
import unicodedata
"""
Text cleaning module for preprocessing text data. """

class TextCleaner:
    """
    cleans and normalizes extracted textt for chunkings"""

    MULTIPLE_SPACES = re.compile(r'[\t ]+')
    MULTIPLE_LINES =re.compile(r'[\r\3]+')
    PAGE_NUMBER = re.compile(r"\s*\d{1,4}\s*$", re.MULTILINE)
    HYPHEN_BREAK = re.compile(r"(\w+)-\s*\n\s*(\w+)")
    HYDER_FOOTER = re.compile(r"\s*(Page|Copyright|All rights reserved|Confidential|Confidentiality notice|Confidential information|Confidential material|Confidential document|Confidential report|Confidential memo|Confidential email|Confidential letter|Confidential communication)\s*\d{0,4}\s*$", re.MULTILINE | re.IGNORECASE)
    

    def clean_for_chunking(cls, text:str) ->str:
        """        Cleans and normalizes text for chunking.
        """

        if not text or not text.strip():
            return ""
        #normalize unicode characters to NFKC form
        text  = unicodedata.normalize("NFKC", text)
        text = cls.MULTIPLE_SPACES.sub(" ", text)
        text = cls.MULTIPLE_LINES.sub("\n\n", text)
        text = cls.PAGE_NUMBER.sub("", text)
        text = cls.HYPHEN_BREAK.sub(r"\1\2", text)
        text = cls.HYDER_FOOTER.sub("", text)
        text = text.strip()

        return text
    
    @classmethod
    def clean_text(cls , text:str)->str:
        """basic cleaning of text for ingestion"""

        if not text :
            return ""
        text = cls.MULTIPLE_SPACES.sub(" ", text)
        return text.strip()
    
    


