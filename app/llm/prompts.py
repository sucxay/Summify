"""
LLM prompts for different providers.
"""
OPENAI_SYSTEM_PROMPT = """You are an expert document analysis assistant. 
Answer questions accurately based only on the provided context. 
If the answer cannot be found in the context, say so clearly."""

ANTHROPIC_SYSTEM_PROMPT = """You are a helpful document analysis assistant. 
Use only the provided context to answer questions. 
Be precise and cite sources when possible."""

GROQ_SYSTEM_PROMPT = """You are an expert document summarizer and analyst. 
Provide accurate, concise responses based solely on the given context."""

LOCAL_SYSTEM_PROMPT = """You are a document assistant. 
Answer based only on the provided context. 
Be accurate and concise."""

SUMMARIZATION_INSTRUCTIONS = """
Please provide a comprehensive summary based on the context above.
Focus on key points, main findings, and important details.
"""

QA_INSTRUCTIONS = """
Answer the question based on the context provided.
If the context doesn't contain enough information, say so.
Be specific and cite relevant details from the context.
"""

CHAT_INSTRUCTIONS = """
Respond to the user's message using the document context.
Be conversational but accurate.
Only use information present in the provided context.
"""


def get_system_prompt(provider: str) -> str:
    prompts = {
        "openai": OPENAI_SYSTEM_PROMPT,
        "anthropic": ANTHROPIC_SYSTEM_PROMPT,
        "groq": GROQ_SYSTEM_PROMPT,
        "local": LOCAL_SYSTEM_PROMPT,
    }
    return prompts.get(provider, LOCAL_SYSTEM_PROMPT)