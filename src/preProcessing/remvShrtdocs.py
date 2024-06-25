import os
import langid

# Define the folder path
folder_path = 'path to the folder where all the zbMATH open documents are present'

def remove_short_documents(folder_path, min_tokens=35):
    """
    Remove documents with less than min_tokens text tokens.
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                tokens = content.split()
                if len(tokens) < min_tokens:
                    os.remove(file_path)
                    print(f'Removed {file_path} (less than {min_tokens} tokens)')

def remove_non_english_documents(folder_path):
    """
    Remove documents if the language is other than English.
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                lang, _ = langid.classify(content)
                if lang != 'en':
                    os.remove(file_path)
                    print(f'Removed {file_path} (non-English document)')

def remove_empty_documents(folder_path):
    """
    Remove documents if they do not have any content.
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            if os.path.getsize(file_path) == 0:
                os.remove(file_path)
                print(f'Removed {file_path} (empty document)')

# Execute the functions
remove_short_documents(folder_path)
remove_non_english_documents(folder_path)
remove_empty_documents(folder_path)