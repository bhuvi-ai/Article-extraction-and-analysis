import nltk  # Library for text processing
from nltk.tokenize import word_tokenize, sent_tokenize  # Functions to split text into words and sentences
from nltk.sentiment.vader import SentimentIntensityAnalyzer  # Tool for analyzing text sentiment
import pandas as pd  # Library to handle data structures like dataframes
import os  # Library for file operations
import re  # Library for regular expressions

#Download NLTK resources

nltk.download('punkt')  # Tokenizer models
nltk.download('vader_lexicon')  # Sentiment lexicon






class TextAnalysis:
    
    def __init__(self):
        self.stopwords = self.load_stopwords()

    def load_stopwords(self):
            stopword_files = [
                "StopWords_Auditor.txt", "StopWords_Currencies.txt", "StopWords_DatesandNumbers.txt",
                "StopWords_Generic.txt","StopWords_GenericLong.txt", "StopWords_Geographic.txt", "StopWords_Names.txt"
            ]
            stopwords = set()
            for file in stopword_files:
                with open(os.path.join("StopWords", file), 'r') as f:
                    stopwords.update(f.read().splitlines())
            return stopwords

    def load_dict(self, positive_dict_file, negative_dict_file):
        # Load positive and negative words from files and remove stopwords
        with open(positive_dict_file, 'r') as file:
            positive_words = set(file.read().splitlines())
        with open(negative_dict_file, 'r') as file:
            negative_words = set(file.read().splitlines())
        
        positive_words = positive_words - self.stopwords
        negative_words = negative_words - self.stopwords
        
        return positive_words, negative_words
    
    def cal_sentiment_score(self, text, positive_words, negative_words):
        # Calculate sentiment scores from text
        # sa = SentimentAnalyzer()  # Sentiment analyzer instance
        tokens = word_tokenize(text)  # Split text into words

        positive_score = 0
        negative_score = 0

        for word in tokens:
            word = word.lower()  # Convert word to lowercase
            if word.isalpha() and word not in self.stopwords:  # Check if word is alphabetic and not a stopword
                if word in positive_words:  # If word is positive
                    positive_score += 1
                if word in negative_words:  # If word is negative
                    negative_score += 1

        # Calculate sentiment metrics
        polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
        subjectivity_score = (positive_score + negative_score) / (len(tokens) + 0.000001)
        
        return positive_score, negative_score, polarity_score, subjectivity_score

    def calculate_avg_sentence_length(self, sentences):
        # Calculate average sentence length
        total_words = sum(len(word_tokenize(sentence)) for sentence in sentences)
        total_sentences = len(sentences)
        return total_words / total_sentences

    def calculate_percentage_complex_words(self, text):
        # Calculate percentage of complex words
        words = word_tokenize(text)
        complex_words = [word for word in words if len(word) > 2]
        return len(complex_words) / len(words)

    def calculate_fog_index(self, avg_sentence_length, percentage_complex_words):
        # Calculate Fog Index (reading difficulty)
        return 0.4 * (avg_sentence_length + percentage_complex_words)

    def calculate_avg_words_per_sentence(self, words, sentences):
        # Calculate average number of words per sentence
        return len(words) / len(sentences)

    def calculate_complex_word_count(self, text):
        # Calculate number of complex words
        words = word_tokenize(text)
        complex_words = [word for word in words if len(word) > 2]
        return len(complex_words)

    def calculate_word_count(self, text):
        # Calculate word count excluding stopwords
        words = word_tokenize(text)
        cleaned_words = [word for word in words if word not in self.stopwords and word.isalpha()]
        return len(cleaned_words)

    def count_syllables(self, word):
        # Count syllables in a word
        vowels = "aeiouAEIOU"
        count = 0
        if word[-1] in ['e', 'E'] and word[-2:] != 'le' and word[-2:] != 'LE':
            word = word[:-1]
        for index, letter in enumerate(word):
            if index == 0 and letter in vowels:
                count += 1
            elif letter in vowels and word[index-1] not in vowels:
                count += 1
        return count

    def calculate_syllable_count_per_word(self, text):
        # Calculate average syllables per word
        words = word_tokenize(text)
        syllable_count = sum(self.count_syllables(word) for word in words)
        return syllable_count / len(words)

    def calculate_personal_pronouns(self, text):
        # Count personal pronouns
        pronouns = ["I", "we", "my", "ours", "us"]
        pattern = r'\b(?:' + '|'.join(pronouns) + r')\b'
        matches = re.findall(pattern, text)
        return len(matches)

    def calculate_avg_word_length(self, text):
        # Calculate average word length
        words = word_tokenize(text)
        total_characters = sum(len(word) for word in words)
        return total_characters / len(words)
       
    def main(self):
        # Main function to process articles and save results
        input_data_file = "Output Data Structure.xlsx"
        positive_dict_file = "MasterDictionary/positive-words.txt"
        negative_dict_file = "MasterDictionary/negative-words.txt"
        articles_dir = "txt_article_content"
        
        positive_words, negative_words = self.load_dict(positive_dict_file, negative_dict_file)
        output_data = pd.read_excel(input_data_file)
        
        sentiment_results = []
        text_analysis_results = []
        
        for index, row in output_data.iterrows():
            url_id = row["URL_ID"]
            url = row["URL"]
            article_file = os.path.join(articles_dir, f"{url_id}.txt")
            
            if os.path.exists(article_file):
                with open(article_file, 'r', encoding='utf-8') as article:
                    article_text = article.read()
                
                # Sentiment analysis
                pos_score, neg_score, polarity_score, subjectivity_score = self.cal_sentiment_score(article_text, positive_words, negative_words)
                
                sentiment_results.append({
                    "URL_ID": url_id,
                    "URL": url,
                    "Positive_Score": pos_score,
                    "Negative_Score": neg_score,
                    "Polarity_Score": polarity_score,
                    "Subjectivity_Score": subjectivity_score
                })
                
                # Text analysis
                sentences = sent_tokenize(article_text)
                words = word_tokenize(article_text)
                
                avg_sentence_length = self.calculate_avg_sentence_length(sentences)
                percentage_complex_words = self.calculate_percentage_complex_words(article_text)
                fog_index = self.calculate_fog_index(avg_sentence_length, percentage_complex_words)
                avg_words_per_sentence = self.calculate_avg_words_per_sentence(words, sentences)
                complex_word_count = self.calculate_complex_word_count(article_text)
                word_count = self.calculate_word_count(article_text)
                syllable_count_per_word = self.calculate_syllable_count_per_word(article_text)
                personal_pronoun_count = self.calculate_personal_pronouns(article_text)
                avg_word_length = self.calculate_avg_word_length(article_text)
                
                text_analysis_results.append({
                    "URL_ID": url_id,
                    "Avg_Sentence_Length": avg_sentence_length,
                    "Percentage_Complex_Words": percentage_complex_words,
                    "Fog_Index": fog_index,
                    "Avg_Words_Per_Sentence": avg_words_per_sentence,
                    "Complex_Word_Count": complex_word_count,
                    "Word_Count": word_count,
                    "Syllable_Count_Per_Word": syllable_count_per_word,
                    "Personal_Pronoun_Count": personal_pronoun_count,
                    "Avg_Word_Length": avg_word_length
                })
        
        # Save sentiment analysis results
        sentiment_df = pd.DataFrame(sentiment_results)
        sentiment_df.to_excel("sentiment_analysis_results.xlsx", index=False)
        
        # Save text analysis results
        text_analysis_df = pd.DataFrame(text_analysis_results)
        text_analysis_df.to_excel("text_analysis_results.xlsx", index=False)
        
        # Merge and save the final results
        merged_df = pd.merge(sentiment_df, text_analysis_df, on='URL_ID')
        merged_df.to_excel("Output Data Structure.xlsx")
        print('Analysis Complete')




if __name__ == "__main__":
    ta = TextAnalysis()
    ta.main()