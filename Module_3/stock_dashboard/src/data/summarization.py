from transformers import pipeline

def summarize_text(text: str, max_length: int, min_length: int) -> str:
    """
    Summarize input text using a transformer model.
    
    Args:
        text: Input text to summarize
        max_length: Maximum length of summary
        min_length: Minimum length of summary
    
    Returns:
        Summarized text
    """
    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = summarizer(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )[0]['summary_text']
        return summary
    except Exception as e:
        raise Exception(f"Summarization failed: {str(e)}")