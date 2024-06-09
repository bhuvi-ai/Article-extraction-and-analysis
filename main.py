from Extraction import ArticleExtractor
from Text_Analysis import TextAnalysis

def main():
    # Run article extraction
    extractor = ArticleExtractor()
    extractor.process_urls("input.xlsx")  # Provide the correct input file name/path

    # Run text analysis
    text_analysis = TextAnalysis()
    text_analysis.main()

if __name__ == "__main__":
    main()
