from text_processing.normalizer import RawTextNormalizer
from pdf.extract_text import extract_only_text_from_pdf
from pathlib import Path

if __name__ == "__main__":
    test_file = Path(__file__).parent / "materials" / "sample.pdf"
    full_text = extract_only_text_from_pdf(test_file)
    print("=== Original Text ===")
    print(full_text)

    normalizer = RawTextNormalizer(enable_spellcheck=False)
    normalized_text = normalizer.normalize(full_text)
    print("\n=== Normalized Text ===")
    print(normalized_text)
