"""Command-line interface for context compressor."""

import click
import json
from typing import Optional

from .compressor import (
    Tokenizer,
    SemanticCompressor,
    HybridCompressor,
    CompressionEvaluator,
    CompressionResult
)


@click.group()
@click.version_option(version="0.1.0", prog_name="context-compress")
def main() -> None:
    """Context Compressor MD - Compress your agent's knowledge base."""
    pass


@main.command()
@click.argument("text")
@click.option("--method", "-m", default="semantic", type=click.Choice(["semantic", "token_based", "hybrid"]), help="Compression method")
@click.option("--ratio", "-r", default=0.1, type=float, help="Target compression ratio (0.0-1.0)")
@click.option("--output", "-o", type=click.Path(), help="Output file")
@click.option("--json-output", "-j", is_flag=True, help="Output as JSON")
def compress(text: str, method: str, ratio: float, output: Optional[str], json_output: bool) -> None:
    """Compress text using specified method."""
    # Initialize compressor based on method
    if method == "semantic":
        compressor = SemanticCompressor()
    elif method == "token_based":
        compressor = HybridCompressor(semantic_weight=0.0)
    else:  # hybrid
        compressor = HybridCompressor(semantic_weight=0.7)
    
    # Compress text
    compressed, result = compressor.compress(text, ratio)
    
    # Output results
    if json_output:
        click.echo(json.dumps({
            "compressed_text": compressed,
            "result": result.to_dict()
        }, indent=2))
    elif output:
        with open(output, 'w') as f:
            f.write(f"Original text: {len(text)} chars, {result.original_tokens} tokens\n")
            f.write(f"Compressed text: {len(compressed)} chars, {result.compressed_tokens} tokens\n\n")
            f.write("Compressed:\n")
            f.write(compressed)
        
        click.echo(f"✅ Compressed text saved to {output}")
    else:
        click.echo(f"\n📊 Compression Result")
        click.echo("=" * 50)
        click.echo(f"Original: {result.original_tokens} tokens ({len(text)} chars)")
        click.echo(f"Compressed: {result.compressed_tokens} tokens ({len(compressed)} chars)")
        click.echo(f"Compression Ratio: {result.compression_ratio:.1%}")
        click.echo(f"Retention Rate: {result.retention_rate:.1%}")
        click.echo(f"Method: {result.compression_method.value}")
        
        if output:
            click.echo(f"\nSaved to: {output}")
        
        click.echo(f"\n📝 Compressed Text:")
        click.echo("-" * 50)
        click.echo(compressed)


@main.command()
@click.option("--ratio", "-r", default=0.1, help="Target compression ratio")
def demo(ratio: float) -> None:
    """Run compression demo."""
    click.echo("\n🧪 Context Compression Demo")
    click.echo("=" * 50)
    
    # Sample knowledge base content
    sample_text = """
    The context compression system works by analyzing the semantic importance 
    of each sentence in a document. First, it splits the text into individual 
    sentences and calculates importance scores based on several factors including 
    position in the document, length, presence of important keywords, and content density.
    
    After calculating importance, the system selects the most critical sentences 
    that maintain the target compression ratio while preserving key information. 
    This approach ensures that essential concepts and arguments remain intact even 
    after significant compression.
    
    The compression ratio determines how much of the original content should be 
    retained. A ratio of 0.1 means the compressed text should be approximately 
    10% of the original length. The system intelligently balances compression 
    with information retention to maintain semantic meaning.
    
    Key benefits of this approach include reduced API costs, faster processing, 
    and the ability to fit more context into limited token windows while 
    maintaining the reasoning capabilities needed for complex tasks.
    """
    
    # Compress using different methods
    click.echo(f"\nOriginal Text: {len(sample_text)} characters")
    
    for method_name in ["semantic", "token_based", "hybrid"]:
        if method_name == "semantic":
            compressor = SemanticCompressor()
        elif method_name == "token_based":
            compressor = HybridCompressor(semantic_weight=0.0)
        else:
            compressor = HybridCompressor(semantic_weight=0.7)
        
        compressed, result = compressor.compress(sample_text, ratio)
        
        click.echo(f"\n{method_name.upper()} Compression (target {ratio:.0%}):")
        click.echo(f"  Tokens: {result.original_tokens} → {result.compressed_tokens}")
        click.echo(f"  Ratio: {result.compression_ratio:.1%}")
        click.echo(f"  Text: {compressed[:100]}...")
    
    # Evaluation demo
    click.echo(f"\n📊 Evaluation Demo")
    click.echo("=" * 50)
    
    evaluator = CompressionEvaluator()
    compressor = SemanticCompressor()
    
    compressed, result = compressor.compress(sample_text, ratio)
    evaluation = evaluator.evaluate(sample_text, compressed, result)
    
    click.echo(f"Quality Score: {evaluation['quality_score']:.2f}")
    click.echo(f"Efficiency: {evaluation['compression_efficiency']:.2%}")
    click.echo(f"Retention: {evaluation['information_retention']:.2%}")


@main.command()
def tokenizer() -> None:
    """Demonstrate tokenization."""
    click.echo("\n🔤 Tokenization Demo")
    click.echo("=" * 50)
    
    tokenizer = Tokenizer()
    
    sample = "Hello, world! This is a test sentence. How many tokens?"
    
    tokens = tokenizer.encode(sample)
    decoded = tokenizer.decode(tokens)
    
    click.echo(f"Text: {sample}")
    click.echo(f"Tokens: {len(tokens)}")
    click.echo(f"Token IDs: {tokens[:10]}...")  # Show first 10
    click.echo(f"Decoded: {decoded}")


@main.command()
@click.option("--output", "-o", type=click.Path(), help="Output file")
def history(output: Optional[str]) -> None:
    """Show compression history."""
    click.echo("\n📜 Compression History")
    click.echo("=" * 50)
    
    # Demo history (in real implementation, would read from stored history)
    click.echo("Note: This would show actual compression history in production.")
    click.echo("Currently running in demo mode.")


@main.command()
def help_text() -> None:
    """Show extended help information."""
    click.echo("""
Context Compressor MD - Compress Your Knowledge Base

FEATURES:
  • Semantic compression with quality preservation
  • Token-based compression for maximum efficiency
  • Hybrid compression combining both methods
  • Configurable compression ratios
  • JSON output for programmatic use
  • Comprehensive compression metrics

USAGE:
  context-compress [OPTIONS] COMMAND
    
Commands:
  compress    Compress text with specified method
  demo        Run compression demo
  tokenizer   Demonstrate tokenization
  history     Show compression history

OPTIONS:
  --method, -m    Compression method: semantic, token_based, hybrid
  --ratio, -r     Target compression ratio (0.0-1.0)
  --output, -o    Output file path
  --json-output, -j    Output as JSON

EXAMPLES:
  context-compress "Your text here" --method semantic --ratio 0.1
  context-compress "Your text" --method hybrid --output output.txt --json-output
  context-compress demo --ratio 0.05

For more information, visit: https://github.com/avasis-ai/context-compressor-md
    """)


def main_entry() -> None:
    """Main entry point."""
    main(prog_name="context-compress")


if __name__ == "__main__":
    main_entry()
