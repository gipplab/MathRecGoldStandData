import os
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def extract_text_tokens_of_interest(folder_path, output_file='text_tokens_of_interest.json'):
    stop_words = set(stopwords.words('english'))
    tokens_of_interest = {}

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                tokens = word_tokenize(text)
                filtered_tokens = [token for token in tokens if token.lower() not in stop_words and token.isalnum()]
                tokens_of_interest[filename] = filtered_tokens

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(tokens_of_interest, json_file, indent=4)
    print(f'Tokens of interest saved to {output_file}')

if __name__ == '__main__':
    folder_path = input("Enter the folder location: ")
    extract_text_tokens_of_interest(folder_path)