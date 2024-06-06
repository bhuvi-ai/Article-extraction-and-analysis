import pandas as pd #use pandas to read .xlxs file like input.xlxs
import requests #use requests for url 
from bs4 import BeautifulSoup # use BeautifulSoup library for extract datra from web pages
import os #use os to perform to make directory in local system and 

class ArticleExtractor:
    def __init__(self):
        # When I create an instance of ArticleExtractor, I check if a directory for storing articles exists.
        # If it doesn't exist, I create it.
        if not os.path.exists("txt_article_content"):
            os.mkdir("txt_article_content")

    def extract_article(self, url):
        # This method fetches and extracts the content from a given URL.
        try:
            response = requests.get(url)  # Make a request to get the content of the URL.
            soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML content using BeautifulSoup.

            # Remove the header and footer from the HTML to clean up the content.
            for element in soup(['header', 'footer']):
                element.decompose()

            # Extract the article title from the HTML's <title> tag.
            title = soup.find('title').text.strip()
            article_content = ""

            # Find the main content container.
            content_container = self.find_main_content_container(soup)
            if content_container:
                # when its reaches to main content container, extract the text from it.
                article_content = self.get_text_from_container(content_container)

            return title, article_content.strip()  # Return the title and the article content.

        except Exception as e:
            # If there's an error during extraction, print the error message.
            print(f"Error when extracting {url}: {e}")
            return None, None

    def find_main_content_container(self, soup):
        # Look for possible main content containers, such as <div>, <article>, and <section> tags.
        possible_containers = soup.find_all(['div', 'article', 'section'])
        for container in possible_containers:
            # Check each container to see if it's likely to be the main content container.
            if self.is_likely_content_container(container):
                return container
        return None

    def is_likely_content_container(self, container):
        # Calculate the total length of text inside <p>, <li>, <h2>, <h3>, <h4>, and <pre> tags.
        text_length = sum(len(p.get_text(strip=True)) for p in container.find_all(['p', 'li', 'h2', 'h3', 'h4', 'pre']))
        # If the text length is greater than 100 characters, consider it the main content container.
        return text_length > 100

    def get_text_from_container(self, container):
        # Extracts text from the container, including text from <p>, <ul>, <li>, <h2>, and other tags.
        
        text_parts = []
        for element in container.descendants:
            if element.name in ['p', 'ul', 'li', 'h2', 'h3', 'h4', 'pre'] and element.get_text(strip=True):
                text_parts.append(element.get_text(separator=' ', strip=True))
        return ' '.join(text_parts)

    def save_article(self, url_id, title, article_content):
        # Save the article content to a text file with the URL_ID as the file name.
        with open(f"txt_article_content/{url_id}.txt", "w", encoding="utf-8") as file:
            file.write(f"Title: {title}\n\n")  # Write the title at the top.
            file.write(article_content)  # Write the article content.

    def is_already_extracted(self, url_id):
        # Check if an article with the given URL_ID has already been extracted by looking for the file.
        return os.path.exists(f"txt_article_content/{url_id}.txt")

    def process_urls(self, input_file):
        # Read the URLs from an Excel file.
        df = pd.read_excel(input_file)
        for index, row in df.iterrows():
            url_id = row["URL_ID"]  # Get the URL_ID from the current row.
            url = row["URL"]  # Get the URL from the current row.

            if self.is_already_extracted(url_id):
                # If the article has already been extracted, skip it.
                print(f"Article {url_id} already extracted. Skipping...")
                continue

            # Extract the article content.
            title, article_content = self.extract_article(url)
            if title and article_content:
                # If extraction is successful, save the article content.
                self.save_article(url_id, title, article_content)
                print(f"Article {url_id} extracted and saved successfully.")
            else:
                # If extraction failed, print a message.
                print(f"Failed to extract article {url_id}.")

def main():
    input_file = ".xlsx"  # Name of the Excel file containing URLs to process.
    extractor = ArticleExtractor()  # Create an instance of ArticleExtractor.
    extractor.process_urls(input_file)  # Process the URLs from the Excel file.

if __name__ == "__main__":
    main()  # Run the main function if this script is executed directly.
