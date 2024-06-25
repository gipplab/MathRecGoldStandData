import os
import requests
import csv

def download_csv(url, save_path='downloaded.csv'):
    """
    Download the CSV file from the given URL and save it to the specified path.
    """
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print(f'CSV file downloaded and saved as {save_path}')
    return save_path

def save_texts_from_csv(csv_path, output_folder='output_texts'):
    """
    Read the CSV file and save each row's third column contents into a text file
    named with the content of the first column.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    with open(csv_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row if there is one
        for row in csv_reader:
            document_id = row[0]
            paragraph_text = row[2]
            output_path = os.path.join(output_folder, f"{document_id}.txt")
            with open(output_path, 'w', encoding='utf-8') as text_file:
                text_file.write(paragraph_text)
            print(f'Saved text for document ID {document_id} to {output_path}')

if __name__ == '__main__':
    url = input("Enter the URL of the CSV file: ")
    csv_path = download_csv(url)
    save_texts_from_csv(csv_path)