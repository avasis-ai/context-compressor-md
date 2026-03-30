"""Tests for context compressor."""

import pytest
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from context_compressor_md.compressor import (
    Tokenizer,
    SemanticCompressor,
    HybridCompressor,
    CompressionEvaluator,
    CompressionResult,
    CompressionMethod
)


class TestTokenizer:
    """Tests for Tokenizer."""
    
    def test_encode_decode(self):
        """Test encoding and decoding."""
        tokenizer = Tokenizer()
        
        text = "Hello, world! This is a test."
        tokens = tokenizer.encode(text)
        decoded = tokenizer.decode(tokens)
        
        assert isinstance(tokens, list)
        assert len(tokens) > 0
        assert isinstance(decoded, str)
    
    def test_count_tokens(self):
        """Test token counting."""
        tokenizer = Tokenizer()
        
        text = "This is a test sentence with several words."
        token_count = tokenizer.count_tokens(text)
        
        assert isinstance(token_count, int)
        assert token_count > 0
    
    def test_encode_empty(self):
        """Test encoding empty text."""
        tokenizer = Tokenizer()
        
        tokens = tokenizer.encode("")
        
        assert tokens == []
    
    def test_decode_empty(self):
        """Test decoding empty tokens."""
        tokenizer = Tokenizer()
        
        decoded = tokenizer.decode([])
        
        assert decoded == ""


class TestSemanticCompressor:
    """Tests for SemanticCompressor."""
    
    def test_compress_text(self):
        """Test basic text compression."""
        compressor = SemanticCompressor()
        
        text = "This is a long text that should be compressed significantly." * 3
        
        compressed, result = compressor.compress(text, 0.1)
        
        assert compressed is not None
        assert result.original_tokens > 0
        assert result.compressed_tokens < result.original_tokens
    
    def test_compress_empty(self):
        """Test compressing empty text."""
        compressor = SemanticCompressor()
        
        compressed, result = compressor.compress("", 0.1)
        
        assert compressed == ""
        assert result.original_tokens == 0
    
    def test_compress_ratio(self):
        """Test compression ratio parameter."""
        compressor = SemanticCompressor()
        
        text = "Test text for compression"
        
        compressed_10, result_10 = compressor.compress(text, 0.1)
        compressed_50, result_50 = compressor.compress(text, 0.5)
        
        # Less compression should result in more text
        assert len(compressed_50) >= len(compressed_10)
    
    def test_compression_method(self):
        """Test compression method identification."""
        compressor = SemanticCompressor()
        
        text = "Test compression"
        _, result = compressor.compress(text)
        
        assert result.compression_method == CompressionMethod.SEMANTIC


class TestHybridCompressor:
    """Tests for HybridCompressor."""
    
    def test_compress_hybrid(self):
        """Test hybrid compression."""
        compressor = HybridCompressor(semantic_weight=0.7)
        
        text = "This is a test for hybrid compression method." * 2
        
        compressed, result = compressor.compress(text, 0.2)
        
        assert compressed is not None
        assert result.compression_method == CompressionMethod.HYBRID
    
    def test_token_based_compression(self):
        """Test token-based compression."""
        compressor = HybridCompressor(semantic_weight=0.0)
        
        text = "Test text for token-based compression."
        
        compressed, result = compressor.compress(text, 0.2)
        
        # Hybrid always returns HYBRID method in metadata
        assert result.compression_method == CompressionMethod.HYBRID
    
    def test_semantic_based_compression(self):
        """Test semantic-based compression."""
        compressor = HybridCompressor(semantic_weight=1.0)
        
        text = "Test text for semantic compression."
        
        compressed, result = compressor.compress(text, 0.2)
        
        # Hybrid always returns HYBRID method in metadata
        assert result.compression_method == CompressionMethod.HYBRID


class TestCompressionEvaluator:
    """Tests for CompressionEvaluator."""
    
    def test_evaluate(self):
        """Test evaluation metrics."""
        evaluator = CompressionEvaluator()
        
        original = "This is original text that should be compressed."
        compressed = "This is compressed text."
        result = CompressionResult(
            original_tokens=10,
            compressed_tokens=5,
            compression_ratio=0.5,
            retention_rate=0.5,
            semantic_preservation=0.8,
            compression_method=CompressionMethod.SEMANTIC,
            timestamp=datetime.now()
        )
        
        metrics = evaluator.evaluate(original, compressed, result)
        
        assert isinstance(metrics, dict)
        assert "compression_efficiency" in metrics
        assert "information_retention" in metrics
    
    def test_get_eval_history(self):
        """Test getting evaluation history."""
        evaluator = CompressionEvaluator()
        
        original = "Test text"
        compressed = "Compressed"
        result = CompressionResult(
            original_tokens=2,
            compressed_tokens=1,
            compression_ratio=0.5,
            retention_rate=0.5,
            semantic_preservation=0.8,
            compression_method=CompressionMethod.SEMANTIC,
            timestamp=datetime.now()
        )
        
        evaluator.evaluate(original, compressed, result)
        
        history = evaluator.get_eval_history()
        
        assert len(history) == 1
    
    def test_average_metrics(self):
        """Test calculating average metrics."""
        evaluator = CompressionEvaluator()
        
        original = "Test text"
        compressed = "Compressed"
        result = CompressionResult(
            original_tokens=2,
            compressed_tokens=1,
            compression_ratio=0.5,
            retention_rate=0.5,
            semantic_preservation=0.8,
            compression_method=CompressionMethod.SEMANTIC,
            timestamp=datetime.now()
        )
        
        evaluator.evaluate(original, compressed, result)
        evaluator.evaluate(original, compressed, result)
        
        avg = evaluator.average_metrics()
        
        assert len(avg) > 0
        assert "compression_efficiency" in avg


class TestCompressionResult:
    """Tests for CompressionResult."""
    
    def test_result_creation(self):
        """Test creating compression result."""
        result = CompressionResult(
            original_tokens=100,
            compressed_tokens=20,
            compression_ratio=0.8,
            retention_rate=0.2,
            semantic_preservation=0.8,
            compression_method=CompressionMethod.SEMANTIC,
            timestamp=datetime.now()
        )
        
        assert result.original_tokens == 100
        assert result.compression_ratio == 0.8
        assert result.semantic_preservation == 0.8
    
    def test_result_to_dict(self):
        """Test converting result to dictionary."""
        result = CompressionResult(
            original_tokens=100,
            compressed_tokens=20,
            compression_ratio=0.8,
            retention_rate=0.2,
            semantic_preservation=0.8,
            compression_method=CompressionMethod.SEMANTIC,
            timestamp=datetime.now(),
            metadata={"test": "value"}
        )
        
        data = result.to_dict()
        
        assert data["original_tokens"] == 100
        assert data["compression_method"] == "semantic"
        assert data["metadata"]["test"] == "value"


class TestCompressionMethods:
    """Tests for compression methods."""
    
    def test_method_enum_values(self):
        """Test method enum values."""
        assert CompressionMethod.SEMANTIC.value == "semantic"
        assert CompressionMethod.TOKEN_BASED.value == "token_based"
        assert CompressionMethod.HYBRID.value == "hybrid"


class TestCompressionMetrics:
    """Tests for compression metrics."""
    
    def test_compression_ratio_calculation(self):
        """Test compression ratio calculation."""
        compressor = SemanticCompressor()
        
        # Full compression
        _, result = compressor.compress("Test", 0.01)
        assert result.compression_ratio >= 0.0
        assert result.compression_ratio <= 1.0
        
        # Less compression
        _, result = compressor.compress("Test", 0.9)
        assert result.compression_ratio >= 0.0
        assert result.compression_ratio <= 1.0
    
    def test_retention_rate_calculation(self):
        """Test retention rate calculation."""
        compressor = SemanticCompressor()
        
        _, result = compressor.compress("Test text here", 0.5)
        
        assert 0.0 <= result.retention_rate <= 1.0
