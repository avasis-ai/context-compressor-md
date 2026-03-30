"""Compressor for agent knowledge base optimization."""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import numpy as np
import tiktoken


class CompressionMethod(Enum):
    """Compression method types."""
    SEMANTIC = "semantic"
    TOKEN_BASED = "token_based"
    HYBRID = "hybrid"


@dataclass
class CompressionResult:
    """Result of a compression operation."""
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float
    retention_rate: float
    semantic_preservation: float
    compression_method: CompressionMethod
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "original_tokens": self.original_tokens,
            "compressed_tokens": self.compressed_tokens,
            "compression_ratio": self.compression_ratio,
            "retention_rate": self.retention_rate,
            "semantic_preservation": self.semantic_preservation,
            "compression_method": self.compression_method.value,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }


class Tokenizer:
    """Handles tokenization for context compression."""
    
    def __init__(self, encoding_name: str = "cl100k_base"):
        """
        Initialize tokenizer.
        
        Args:
            encoding_name: Tokenizer encoding name
        """
        self._tokenizer = tiktoken.get_encoding(encoding_name)
    
    def encode(self, text: str) -> List[int]:
        """
        Encode text to tokens.
        
        Args:
            text: Text to encode
            
        Returns:
            List of token IDs
        """
        return self._tokenizer.encode(text)
    
    def decode(self, tokens: List[int]) -> str:
        """
        Decode tokens to text.
        
        Args:
            tokens: List of token IDs
            
        Returns:
            Decoded text
        """
        return self._tokenizer.decode(tokens)
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text.
        
        Args:
            text: Text to count
            
        Returns:
            Number of tokens
        """
        return len(self._tokenizer.encode(text))


class SemanticCompressor:
    """Compresses text while preserving semantic meaning."""
    
    def __init__(self):
        """Initialize semantic compressor."""
        self._compression_history: List[Dict[str, Any]] = []
    
    def compress(self, text: str, target_ratio: float = 0.1) -> Tuple[str, CompressionResult]:
        """
        Compress text while preserving key information.
        
        Args:
            text: Text to compress
            target_ratio: Target compression ratio (0.0-1.0)
            
        Returns:
            Tuple of (compressed_text, CompressionResult)
        """
        if not text or len(text.strip()) == 0:
            return "", CompressionResult(
                original_tokens=0,
                compressed_tokens=0,
                compression_ratio=1.0,
                retention_rate=1.0,
                semantic_preservation=1.0,
                compression_method=CompressionMethod.SEMANTIC,
                timestamp=datetime.now()
            )
        
        # Split text into sentences
        sentences = self._split_into_sentences(text)
        
        # Calculate sentence importance
        importance_scores = self._calculate_sentence_importance(sentences)
        
        # Sort by importance
        sorted_sentences = sorted(
            zip(sentences, importance_scores),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Select top sentences to maintain target ratio
        target_tokens = int(len(text) * target_ratio)
        selected_sentences = []
        current_tokens = 0
        
        for sentence, score in sorted_sentences:
            if current_tokens + len(sentence) <= target_tokens or len(selected_sentences) < 3:
                selected_sentences.append(sentence)
                current_tokens += len(sentence)
        
        # Compress selected sentences
        compressed_text = " ".join(selected_sentences)
        
        # Calculate results
        original_tokens = len(text)
        compressed_tokens = len(compressed_text)
        compression_ratio = (1 - (compressed_tokens / original_tokens)) if original_tokens > 0 else 0
        retention_rate = (compressed_tokens / original_tokens) if original_tokens > 0 else 0
        
        result = CompressionResult(
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            compression_ratio=compression_ratio,
            retention_rate=retention_rate,
            semantic_preservation=retention_rate,  # Simplified
            compression_method=CompressionMethod.SEMANTIC,
            timestamp=datetime.now(),
            metadata={
                "original_sentences": len(sentences),
                "selected_sentences": len(selected_sentences)
            }
        )
        
        self._compression_history.append(result.to_dict())
        
        return compressed_text, result
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        import re
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _calculate_sentence_importance(self, sentences: List[str]) -> List[float]:
        """Calculate importance score for each sentence."""
        if not sentences:
            return []
        
        # Simple importance scoring based on position and keywords
        importance_scores = []
        
        for i, sentence in enumerate(sentences):
            score = 0.0
            
            # Position-based scoring (first and last sentences often important)
            if i == 0 or i == len(sentences) - 1:
                score += 0.3
            
            # Length-based scoring (not too short, not too long)
            words = sentence.split()
            if 10 <= len(words) <= 30:
                score += 0.2
            
            # Keyword scoring
            important_words = ['important', 'key', 'critical', 'essential', 'must', 'should']
            if any(word in sentence.lower() for word in important_words):
                score += 0.3
            
            # Content density (ratio of content to stop words)
            if len(words) > 0:
                stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
                content_ratio = sum(1 for w in words if w.lower() not in stop_words) / len(words)
                if content_ratio > 0.7:
                    score += 0.2
            
            importance_scores.append(min(score, 1.0))
        
        return importance_scores


class HybridCompressor:
    """Combines semantic and token-based compression."""
    
    def __init__(self, semantic_weight: float = 0.7):
        """
        Initialize hybrid compressor.
        
        Args:
            semantic_weight: Weight for semantic compression (0.0-1.0)
        """
        self._semantic_weight = semantic_weight
        self._semantic_compressor = SemanticCompressor()
    
    def compress(self, text: str, target_ratio: float = 0.1) -> Tuple[str, CompressionResult]:
        """
        Compress text using hybrid method.
        
        Args:
            text: Text to compress
            target_ratio: Target compression ratio
            
        Returns:
            Tuple of (compressed_text, CompressionResult)
        """
        # Semantic compression
        semantic_compressed, semantic_result = self._semantic_compressor.compress(text, target_ratio)
        
        # Token-based compression (simplified)
        token_compressed, token_result = self._compress_token_based(text, target_ratio)
        
        # Combine results based on weight
        if self._semantic_weight >= 0.5:
            compressed_text = semantic_compressed
            compression_result = semantic_result
        else:
            compressed_text = token_compressed
            compression_result = token_result
        
        # Update metadata
        compression_result.metadata["semantic_weight"] = self._semantic_weight
        compression_result.compression_method = CompressionMethod.HYBRID
        
        return compressed_text, compression_result
    
    def _compress_token_based(self, text: str, target_ratio: float) -> Tuple[str, CompressionResult]:
        """Token-based compression."""
        if not text:
            return "", CompressionResult(
                original_tokens=0,
                compressed_tokens=0,
                compression_ratio=1.0,
                retention_rate=1.0,
                semantic_preservation=1.0,
                compression_method=CompressionMethod.TOKEN_BASED,
                timestamp=datetime.now()
            )
        
        tokenizer = Tokenizer()
        tokens = tokenizer.encode(text)
        
        # Calculate target token count
        target_tokens = int(len(tokens) * target_ratio)
        
        # Keep important tokens (first, last, unique)
        important_indices = [0, len(tokens) - 1]
        unique_tokens = set(tokens)
        
        for i, token in enumerate(tokens):
            if token in unique_tokens and i not in important_indices:
                important_indices.append(i)
                if len(important_indices) >= target_tokens * 2:
                    break
        
        # Select top tokens
        selected_indices = sorted(important_indices[:target_tokens])
        selected_tokens = [tokens[i] for i in selected_indices]
        
        compressed_text = tokenizer.decode(selected_tokens)
        
        original_tokens = len(tokens)
        compressed_tokens = len(selected_tokens)
        
        return compressed_text, CompressionResult(
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            compression_ratio=(1 - (compressed_tokens / original_tokens)) if original_tokens > 0 else 0,
            retention_rate=(compressed_tokens / original_tokens) if original_tokens > 0 else 0,
            semantic_preservation=0.5,  # Simplified
            compression_method=CompressionMethod.TOKEN_BASED,
            timestamp=datetime.now()
        )


class CompressionEvaluator:
    """Evaluates compression quality."""
    
    def __init__(self):
        """Initialize evaluator."""
        self._eval_results: List[Dict[str, Any]] = []
    
    def evaluate(self, original: str, compressed: str, result: CompressionResult) -> Dict[str, Any]:
        """
        Evaluate compression quality.
        
        Args:
            original: Original text
            compressed: Compressed text
            result: Compression result
            
        Returns:
            Evaluation metrics
        """
        # Calculate additional metrics
        original_words = len(original.split())
        compressed_words = len(compressed.split()) if compressed else 0
        
        metrics = {
            "compression_efficiency": result.compression_ratio,
            "information_retention": result.retention_rate,
            "word_reduction": (1 - (compressed_words / original_words)) if original_words > 0 else 0,
            "quality_score": result.semantic_preservation,
            "timestamp": datetime.now().isoformat()
        }
        
        self._eval_results.append(metrics)
        return metrics
    
    def get_eval_history(self) -> List[Dict[str, Any]]:
        """Get evaluation history."""
        return self._eval_results.copy()
    
    def average_metrics(self) -> Dict[str, float]:
        """Calculate average metrics across all evaluations."""
        if not self._eval_results:
            return {}
        
        avg = {}
        num_evals = len(self._eval_results)
        
        for key in self._eval_results[0].keys():
            if isinstance(self._eval_results[0][key], (int, float)):
                avg[key] = sum(r[key] for r in self._eval_results) / num_evals
        
        return avg
