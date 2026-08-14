"""
Generator - calls the LLM with retrieved content to generate answers.
"""

from typing import Optional, Any, Dict, List
import logging

from app.llm.client import LLMClient
from app.config.prompts import (
    SYSTEM_PROMPT,
    GENERAL_SUMMARY_PROMPT,
    EXECUTIVE_SUMMARY_PROMPT,
    BULLET_POINTS_PROMPT,
    KEY_FINDINGS_PROMPT,
    ACTION_ITEMS_PROMPT,
)
from app.utils.timers import timeit

logger = logging.getLogger(__name__)

class Generator:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client


    @timeit
    def generate(
        self,
        context: str,
        query: str,
        summary_type: str = "general",
        temperature: Optional[float] = None,
        max_tokens: int = 500,
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Generate a response from the LLM based on the provided context and query.

        Args:
            context (str): The context retrieved from the vector store.
            query (str): The user's query.
            summary_type (str): The type of summary to generate. Options are "general", "executive", "bullet_points", "key_findings", "action_items".
            temperature (float): Sampling temperature for the LLM.
            max_tokens (int): Maximum number of tokens to generate.

        Returns:
            str: The generated response from the LLM.
        """
        if not context or not context.strip():
            logger.warning("Empty context provided to generator.")
            return "No relevant information found to answer the query."
        prompt = self._get_prompt(summary_type)
        sys_prompt = system_prompt or SYSTEM_PROMPT

        prompt = prompt.format(system_prompt=sys_prompt, context=context)
        logger.debug(f"Generating with prompt length: {len(prompt)} chars")
        response = self.llm_client.complete(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response

    def generate_summary(
        self,
        context: str,
        summary_type: str = "general",
        **kwargs,
    ) -> str:
        return self.generate(
            context=context,
            query="",
            summary_type=summary_type,
            **kwargs,
        )

    def generate_answer(
        self,
        context: str,
        question: str,
        **kwargs,
    ) -> str:
        return self.generate(
            context=context,
            query=question,
            summary_type="general",
            **kwargs,
        )

    @staticmethod
   
    def _get_prompt(summary_type: str) -> str:
        """Return the appropriate prompt template for the requested summary type."""
        prompts = {
            "general": GENERAL_SUMMARY_PROMPT,
            "executive": EXECUTIVE_SUMMARY_PROMPT,
            "bullet_points": BULLET_POINTS_PROMPT,
            "key_findings": KEY_FINDINGS_PROMPT,
            "action_items": ACTION_ITEMS_PROMPT,
        }

        if summary_type not in prompts:
            raise ValueError(
                f"Unsupported summary type: {summary_type}. "
                f"Supported types: {', '.join(prompts.keys())}"
            )

        return prompts[summary_type]


    @staticmethod
    def _get_prompt_template(summary_type: str) -> str:
        """Legacy alias for backward compatibility."""
        return Generator._get_prompt(summary_type)