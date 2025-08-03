# TODO: Idea: want to extract each word of concatenated words
# Example: fromsender, not a real word: should be 'from' and 'sender'
# implement dictionary API to find subsets of strings?

# TODO: Stucture variables as key:value pairs?
#   Then we can have dirpath, regex ... etc, in the var file\
#   Yes, this will need to be done, so I can have a variable for the training spam directory, training ham directory, and testing directory

# TODO: Problematic because it is not generalized, has too much knowledge of external factors (ie. hardcoded things)

import os
import re
from typing import Pattern

p_w_upper_bound =0.90
p_w_lower_bound =0.05

def get_directory(dirtype : str) -> str:
    dirpath = open(f"./var").read().strip()
    return f"{dirpath}{dirtype}"

def get_files_list(dirtype : str) -> list:
    dir = get_directory(dirtype)
    return os.listdir(dir)

def get_files_count(dirtype : str) -> int:
    return len(get_files_list(dirtype))

# Extract text contents from file
def get_data(filepath):
    with open(filepath, "r", errors="ignore") as file:
        return file.read().lower()

# Do we want to include numbers? Possibly should be alphanumeric.
# Validate tokens (is this the best version?)
valid_chars1 = r"^[A-Za-z']+$" 
stopwords = get_data("./stopwords_nltk").split("\n")

# regex full matching
def charset_full_match(valid_chars_regex, token):
    return True if re.fullmatch(valid_chars_regex, token) else False

# regex partial matching
def charset_match(valid_chars_regex, token):
    return True if re.match(valid_chars_regex, token) else False

# print a portion that appears under and over a certain percentage
def print_portion(tokens : dict, files_count : int, lower_bound_percent : int, upper_bound_percent : int):
    print("index ".rjust(10), " word".ljust(40), "count".center(10),"percent".center(10),sep="|")
    print("-"*100)
    index=1
    total=1
    for word,count in tokens.items():
        rate = count/files_count
        if lower_bound_percent <= rate <= upper_bound_percent:
            print(f"{str(index)} ".rjust(10),f" {word}".ljust(40),str(count).center(10),f"{100*count/files_count}%".center(10), sep="|")
            total+=1
        index+=1
    print(f"{total} items appear within {lower_bound_percent*100}% and {upper_bound_percent*100}% of files.")

# parse text file, return organized tokens
# V2, split lines, clean lines, split lines, validate tokens
def parse_text(data: str, valid_chars_regex: Pattern) -> dict:
    cleaned_tokens=[]
    line = re.sub(r"\n", " ", data)
    line = re.sub(r"[.,:\-!]","", line)
    tokens = line.split(" ")
    for token in tokens:
        token = token.strip()
        if charset_full_match(valid_chars_regex, token) and token not in stopwords:
            cleaned_tokens.append(token)
    return dict.fromkeys(cleaned_tokens, 1)

# build bag of words from scratch
def build_dictionary(dirtype : str) -> dict:
    dirpath = get_directory(dirtype)
    files_count = get_files_count(dirtype)
    files = os.listdir(dirpath)
    files_count = len(files)
    print(f"{dirpath} : {files_count}")

    dict_counts = {}
    for filename in files:
        filepath = os.path.join(dirpath, filename)
        data = get_data(filepath)
        token_dict = parse_text(data, valid_chars1)
        # Should we use 'keys()' or 'items()'?
        for word in token_dict.keys():
            dict_counts[word] = dict_counts.get(word, 0) + 1

    dict_probabilities = {}
    # type_char = f"p_w|{dirtype[:1]}"
    type_char = "p_w"
    for word, count in dict_counts.items():
        p_w = count/files_count
        ## Ignore words above, below given probability
        if p_w_upper_bound >= p_w >= p_w_lower_bound:
            dict_probabilities[word] = {"count": count, type_char: p_w}
        

    print(f"{len(dict_probabilities)} words in collection.")
    return dict_probabilities



    

        
