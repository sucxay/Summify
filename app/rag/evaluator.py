"""
Evaluator - Evaluates RAG pipeline performance using RAGAS metrics.
"""
from typing import List, Dict, Any, Optional
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class EvaluationResult:
    faithfulness: float = 0.0
    answer_relevancy: float = 0.0
    context_precision: float = 0.0
    context_recall: float = 0.0
    overall_score: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)


class RAGEvaluator:
    def __init__(self):
        self._ragas_available = False
        try:
            from ragas import evaluate
            from ragas.metrics import (
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall,
            )
            self._evaluate = evaluate
            self._metrics = [
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall,
            ]
            self._ragas_available = True
        except ImportError:
            logger.warning("RAGAS not installed. Using heuristic evaluation.")

    def evaluate(
        self,
        query: str,
        answer: str,
        contexts: List[str],
        ground_truth: Optional[str] = None,
    ) -> EvaluationResult:
        if self._ragas_available and ground_truth:
            return self._evaluate_with_ragas(query, answer, contexts, ground_truth)
        return self._evaluate_heuristic(query, answer, contexts)

    def _evaluate_with_ragas(
        self,
        query: str,
        answer: str,
        contexts: List[str],
        ground_truth: str,
    ) -> EvaluationResult:
        from ragas import evaluate
        from ragas.metrics import (
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        )

        dataset = {
            "question": [query],
            "answer": [answer],
            "contexts": [contexts],
            "ground_truth": [ground_truth],
        }

        metrics = [
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ]

        result = evaluate(dataset, metrics=metrics)
        scores = result.to_pandas()

        return EvaluationResult(
            faithfulness=round(float(scores["faithfulness"].iloc[0]), 4),
            answer_relevancy=round(float(scores["answer_relevancy"].iloc[0]), 4),
            context_precision=round(float(scores["context_precision"].iloc[0]), 4),
            context_recall=round(float(scores["context_recall"].iloc[0]), 4),
            overall_score=round(float(scores.iloc[0].mean()), 4),
            details={"method": "ragas"},
        )

    def _evaluate_heuristic(
        self,
        query: str,
        answer: str,
        contexts: List[str],
    ) -> EvaluationResult:
        context_relevance = self._calculate_context_relevance(query, contexts)
        answer_coverage = self._calculate_answer_coverage(answer, contexts)
        answer_length_score = self._calculate_answer_length_score(answer)

        overall = (context_relevance + answer_coverage + answer_length_score) / 3

        return EvaluationResult(
            faithfulness=answer_coverage,
            answer_relevancy=context_relevance,
            context_precision=context_relevance,
            context_recall=context_relevance,
            overall_score=round(overall, 4),
            details={"method": "heuristic"},
        )

    def _calculate_context_relevance(
        self, query: str, contexts: List[str]
    ) -> float:
        query_words = set(query.lower().split())
        if not query_words or not contexts:
            return 0.0

        scores = []
        for context in contexts:
            context_words = set(context.lower().split())
            overlap = query_words.intersection(context_words)
            score = len(overlap) / len(query_words) if query_words else 0.0
            scores.append(score)

        return round(sum(scores) / len(scores), 4) if scores else 0.0

    def _calculate_answer_coverage(
        self, answer: str, contexts: List[str]
    ) -> float:
        if not answer or not contexts:
            return 0.0

        combined_context = " ".join(contexts).lower()
        answer_words = set(answer.lower().split())

        if not answer_words:
            return 0.0

        covered = sum(
            1 for word in answer_words if word in combined_context
        )
        return round(covered / len(answer_words), 4)

    def _calculate_answer_length_score(self, answer: str) -> float:
        if not answer:
            return 0.0

        word_count = len(answer.split())

        if word_count < 10:
            return 0.3
        elif word_count < 30:
            return 0.6
        elif word_count < 100:
            return 1.0
        elif word_count < 300:
            return 0.8
        else:
            return 0.5

    def evaluate_batch(
        self,
        test_cases: List[Dict[str, Any]],
    ) -> List[EvaluationResult]:
        results = []
        for case in test_cases:
            result = self.evaluate(
                query=case.get("query", ""),
                answer=case.get("answer", ""),
                contexts=case.get("contexts", []),
                ground_truth=case.get("ground_truth"),
            )
            results.append(result)
        return results

    def get_average_scores(
        self,
        results: List[EvaluationResult],
    ) -> Dict[str, float]:
        if not results:
            return {}

        return {
            "avg_faithfulness": round(
                sum(r.faithfulness for r in results) / len(results), 4
            ),
            "avg_answer_relevancy": round(
                sum(r.answer_relevancy for r in results) / len(results), 4
            ),
            "avg_context_precision": round(
                sum(r.context_precision for r in results) / len(results), 4
            ),
            "avg_context_recall": round(
                sum(r.context_recall for r in results) / len(results), 4
            ),
            "avg_overall": round(
                sum(r.overall_score for r in results) / len(results), 4
            ),
            "num_samples": len(results),
        }