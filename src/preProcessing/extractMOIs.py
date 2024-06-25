import os
import json
import re
import xml.etree.ElementTree as ET
from sympy import latex, sympify
from lxml import etree

def latex_to_mathml(latex_str):
    try:
        expr = sympify(latex_str)
        mathml_str = latex(expr, form='mathml')
        return mathml_str
    except Exception as e:
        print(f"Error converting LaTeX to MathML: {e}")
        return None

def extract_math_tokens_of_interest(folder_path, output_file='math_tokens_of_interest.json'):
    math_tokens_of_interest = {}

    latex_pattern = re.compile(r'\$([^\$]+)\$')

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                matches = latex_pattern.findall(text)
                mathml_trees = []
                for match in matches:
                    mathml_str = latex_to_mathml(match)
                    if mathml_str:
                        root = etree.fromstring(mathml_str)
                        for elem in root.iter():
                            mathml_trees.append(etree.tostring(elem).decode('utf-8'))
                math_tokens_of_interest[filename] = mathml_trees

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(math_tokens_of_interest, json_file, indent=4)
    print(f'Math tokens of interest saved to {output_file}')

if __name__ == '__main__':
    folder_path = input("Enter the folder location: ")
    extract_math_tokens_of_interest(folder_path)