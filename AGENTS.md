# AGENTS.md - Context Compressor MD Project Context

This folder is home. Treat it that way.

## Project: Context-Compressor-MD (#29)

### Identity
- **Name**: Context-Compressor-MD
- **License**: MIT
- **Org**: avasis-ai
- **PyPI**: context-compressor-md
- **Version**: 0.1.0
- **Tagline**: Compress your agent's knowledge base by 10x without losing reasoning power

### What It Does
This pre-processing tool ingests massive SKILL.md files and repository documentation, mathematically compressing the text into high-density prompt representations. These representations retain full semantic meaning but utilize a fraction of the context window.

### Inspired By
- LLMLingua
- Cursor
- Anthropic Context
- Token optimization research

### Core Components

#### `/compressor/`
- Semantic compression
- Token-based compression
- Hybrid compression
- Compression evaluation

#### `/evals/`
- Quality metrics
- Benchmarking
- Performance tracking

### Technical Architecture

**Key Dependencies:**
- `tiktoken>=0.5` - Tokenization (Trust score: 9.1)
- `numpy>=1.24` - Numerical operations (Trust score: 8.7)
- `click>=8.0` - CLI framework (Trust score: 8.8)

**Core Modules:**
1. `compressor.py` - Compression algorithms and evaluation
2. `cli.py` - Command-line interface

### AI Coding Agent Guidelines

#### When Contributing:

1. **Understand the domain**: Token optimization requires mathematical precision
2. **Use Context7**: Check trust scores for new libraries before adding dependencies
3. **Preserve meaning**: Compression should not lose critical information
4. **Measure everything**: Track quality, efficiency, and retention metrics
5. **Balance tradeoffs**: Optimize for both compression and quality
6. **Benchmark rigorously**: Prove improvements with data

#### What to Remember:

- **Quality first**: Compression must preserve semantic meaning
- **Configurable ratios**: Allow targeting specific compression levels
- **Multiple methods**: Different use cases need different approaches
- **Metrics matter**: Track compression efficiency and quality
- **Performance**: Ensure compression doesn't become a bottleneck
- **Transparent**: Show users what was compressed and why

#### Common Patterns:

**Semantic compression:**
```python
from context_compressor_md.compressor import SemanticCompressor

compressor = SemanticCompressor()
compressed, result = compressor.compress(text, target_ratio=0.1)

print(f"Compressed: {result.compressed_tokens} tokens")
print(f"Saved: {result.compression_ratio:.1%}")
```

**Hybrid compression:**
```python
from context_compressor_md.compressor import HybridCompressor

compressor = HybridCompressor(semantic_weight=0.7)
compressed, result = compressor.compress(text, target_ratio=0.2)
```

**Evaluate compression:**
```python
from context_compressor_md.compressor import CompressionEvaluator

evaluator = CompressionEvaluator()
metrics = evaluator.evaluate(original, compressed, result)

print(f"Quality: {metrics['quality_score']:.2f}")
print(f"Efficiency: {metrics['compression_efficiency']:.2%}")
```

**Use tokenizer:**
```python
from context_compressor_md.compressor import Tokenizer

tokenizer = Tokenizer()
tokens = tokenizer.encode("Your text here")
count = tokenizer.count_tokens("Your text here")
```

### Project Status

- ✅ Initial implementation complete
- ✅ Semantic compression algorithm
- ✅ Token-based compression
- ✅ Hybrid compression method
- ✅ Compression evaluation metrics
- ✅ CLI interface with multiple commands
- ✅ Comprehensive test suite
- ⚠️ Advanced evaluation algorithms pending
- ⚠️ Model-specific optimizations pending

### How to Work with This Project

1. **Read `SOUL.md`** - Understand who you are
2. **Read `USER.md`** - Know who you're helping
3. **Check `memory/YYYY-MM-DD.md`** - Recent context
4. **Read `MEMORY.md`** - Long-term decisions (main session only)
5. **Execute**: Code → Test → Commit

### Red Lines

- **No stubs or TODOs**: Every function must have real implementation
- **Type hints required**: All function signatures must include types
- **Docstrings mandatory**: Explain what, why, and how
- **Test coverage**: New features need tests
- **Quality guaranteed**: Compression must preserve meaning

### Development Workflow

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/ -v

# Format code
black src/ tests/
isort src/ tests/

# Check syntax
python -m py_compile src/context_compressor_md/*.py

# Run CLI
context-compress --help

# Commit
git add -A && git commit -m "feat: add quality metrics"
```

### Key Files to Understand

- `src/context_compressor_md/compressor.py` - Core compression logic
- `src/context_compressor_md/cli.py` - Command-line interface
- `tests/test_compressor.py` - Comprehensive tests
- `README.md` - Usage examples

### Security Considerations

- **Trusted dependencies**: All verified via Context7
- **No external calls**: All processing local
- **Open algorithms**: Transparent compression methods
- **MIT License**: Open source, community-driven
- **Quality metrics**: Verify compression quality

### Next Steps

1. Add advanced evaluation algorithms
2. Model-specific optimizations (Claude, Llama, etc.)
3. Integration with major LLM platforms
4. Web-based compression dashboard
5. Batch processing for large documents
6. Performance optimizations for speed

### Unique Defensible Moat

The **proprietary information-theoretic compression model specifically fine-tuned on the internal attention heads of modern coding models** prevents naive summarizers from competing effectively. This requires:

- Deep understanding of tokenization and attention mechanisms
- Model-specific optimization algorithms
- Extensive benchmarking against multiple models
- Continuous updates for new model architectures
- Performance vs quality tradeoff analysis
- Production-grade compression pipelines

This is complex work requiring both AI expertise and optimization skills, making it difficult to replicate effectively.

---

**This file should evolve as you learn more about the project.**
