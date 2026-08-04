"""
Centralized prompt templates for the RAG pipeline.
All prompts live here so they can be versioned, tested, and tuned.
"""

# ============================================
# Summarization Prompts
# ============================================

SYSTEM_PROMPT = """You are an expert document summarizer. Your task is to create accurate, 
concise, and well-structured summaries based ONLY on the provided document excerpts.

Rules:
- Only use information present in the provided context
- If the context doesn't contain enough information, say so honestly
- Maintain factual accuracy - do not add or infer information
- Use clear, professional language
- Structure your response with appropriate headings when helpful
"""

GENERAL_SUMMARY_PROMPT = """{system_prompt}

## Document Context
{context}

## Task
Provide a comprehensive summary of the document based on the excerpts above.
Cover the main topics, key findings, and important details.

## Summary
"""

EXECUTIVE_SUMMARY_PROMPT = """{system_prompt}

## Document Context
{context}

## Task
Create an executive summary (2-3 paragraphs) that captures:
1. The document's purpose and scope
2. The most critical findings or conclusions
3. Key recommendations or next steps (if any)

Keep it concise and business-focused.

## Executive Summary
"""

BULLET_POINTS_PROMPT = """{system_prompt}

## Document Context
{context}

## Task
Extract the key points from the document and present them as bullet points.
Group related points together under thematic headings.
Each bullet should be a single, clear statement.

## Key Points
"""

KEY_FINDINGS_PROMPT = """{system_prompt}

## Document Context
{context}

## Task
Identify and list the most important findings, conclusions, or insights from the document.
For each finding, explain why it's significant.
Prioritize the most impactful findings first.

## Key Findings
"""

ACTION_ITEMS_PROMPT = """{system_prompt}

## Document Context
{context}

## Task
Extract all action items, tasks, recommendations, or next steps mentioned in the document.
For each action item, include:
- What needs to be done
- Who is responsible (if mentioned)
- Deadline or timeline (if mentioned)
- Priority level (if can be inferred)

## Action Items
"""

# ============================================
# Map-Reduce Summarization (for long documents)
# ============================================

MAP_PROMPT = """{system_prompt}

Summarize the following excerpt from a larger document.
Focus on the main points and key details.

## Excerpt
{chunk_text}

## Summary of this excerpt
"""

REDUCE_PROMPT = """{system_prompt}

Combine the following partial summaries into a single, coherent summary.
Remove redundancy and ensure smooth flow between topics.

## Partial Summaries
{summaries}

## Combined Summary
"""

# ============================================
# Chat Prompts
# ============================================

CHAT_SYSTEM_PROMPT = """You are a helpful document assistant. Answer questions based on the 
document excerpts provided. If the answer isn't in the excerpts, say so clearly.
Be conversational but accurate."""

CHAT_QUERY_PROMPT = """{system_prompt}

## Document Context
{context}

## Conversation History
{history}

## User Question
{question}

## Answer
"""

# ============================================
# Retrieval Prompt (for generating better queries)
# ============================================

QUERY_REWRITE_PROMPT = """Given the user's question and conversation history, 
rewrite the question to be more specific and self-contained for document retrieval.
Remove references to previous conversation that wouldn't make sense in isolation.

Conversation History:
{history}

Original Question: {question}

Rewritten Question:"""

# ============================================
# Prompt Builder Helper
# ============================================

def build_summary_prompt(
    summary_type: str,
    context: str,
    system_prompt: str = SYSTEM_PROMPT,
) -> str:
    """
    Build a complete summarization prompt based on type.

    Args:
        summary_type: One of 'general', 'executive', 'bullet_points', 'key_findings', 'action_items'
        context: Retrieved document chunks formatted as string
        system_prompt: System prompt to use

    Returns:
        Formatted prompt string
    """
    prompt_templates = {
        "general": GENERAL_SUMMARY_PROMPT,
        "executive": EXECUTIVE_SUMMARY_PROMPT,
        "bullet_points": BULLET_POINTS_PROMPT,
        "key_findings": KEY_FINDINGS_PROMPT,
        "action_items": ACTION_ITEMS_PROMPT,
    }

    template = prompt_templates.get(summary_type, GENERAL_SUMMARY_PROMPT)
    
    return template.format(
        system_prompt=system_prompt,
        context=context,
    )


def build_chat_prompt(
    question: str,
    context: str,
    history: str = "",
    system_prompt: str = CHAT_SYSTEM_PROMPT,
) -> str:
    """Build a chat prompt with context and history."""
    return CHAT_QUERY_PROMPT.format(
        system_prompt=system_prompt,
        context=context,
        history=history or "No previous conversation.",
        question=question,
    )


def build_map_prompt(chunk_text: str) -> str:
    """Build a map-step prompt for a single chunk."""
    return MAP_PROMPT.format(
        system_prompt=SYSTEM_PROMPT,
        chunk_text=chunk_text,
    )


def build_reduce_prompt(summaries: str) -> str:
    """Build a reduce-step prompt for combining summaries."""
    return REDUCE_PROMPT.format(
        system_prompt=SYSTEM_PROMPT,
        summaries=summaries,
    )