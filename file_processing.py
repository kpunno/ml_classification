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

class FileProcessor:
    def __init__(self, dirtype, valid_chars=r"^[A-Za-z']+$", stopwords_dir="./stopwords_nltk", p_w_upper_bound=0.95, p_w_lower_bound=0.05):
        self.p_w_upper_bound = p_w_upper_bound
        self.p_w_lower_bound = p_w_lower_bound
        self.dirtype = dirtype
        self.stopwords = self.get_data(stopwords_dir).split("\n")
        # Do we want to include numbers? Possibly should be alphanumeric.
        # Validate tokens (is this the best version?)
        self.valid_chars = valid_chars

    def get_directory(self) -> str:
        dirpath = open(f"./var").read().strip()
        return f"{dirpath}{self.dirtype}"

    def get_files_list(self) -> list:
        dir = self.get_directory()
        return os.listdir(dir)

    def get_files_count(self) -> int:
        return len(self.get_files_list())

    # Extract text contents from file
    def get_data(self, filepath):
        with open(filepath, "r", errors="ignore") as file:
            return file.read().lower()

    # regex full matching
    def charset_full_match(self, token):
        return True if re.fullmatch(self.valid_chars, token) else False

    # regex partial matching
    def charset_match(self, token):
        return True if re.match(self.valid_chars, token) else False

    # print a portion that appears under and over a certain percentage
    def print_portion(self, tokens : dict, lower_bound_percent : int, upper_bound_percent : int):
        print("index ".rjust(10), " word".ljust(40), "count".center(10),"percent".center(10),sep="|")
        print("-"*100)
        index=1
        total=0
        files_count = self.get_files_count()
        for word,count in tokens.items():
            rate = count/files_count
            if lower_bound_percent <= rate <= upper_bound_percent:
                print(f"{str(index)} ".rjust(10),f" {word}".ljust(40),str(count).center(10),f"{100*count/files_count}%".center(10), sep="|")
                total+=1
            index+=1
        print(f"{total} items appear within {lower_bound_percent*100}% and {upper_bound_percent*100}% of files.")

    # parse text file, return organized tokens
    # V2, split lines, clean lines, split lines, validate tokens
    def parse_text(self, data: str) -> dict:
        cleaned_tokens=[]
        line = re.sub(r"\n", " ", data)
        line = re.sub(r"[.,:\-!]","", line)
        tokens = line.split(" ")
        for token in tokens:
            token = token.strip()
            if self.charset_full_match(token) and token not in self.stopwords:
                cleaned_tokens.append(token)
        return dict.fromkeys(cleaned_tokens, 1)

    # build bag of words from scratch
    def build_dictionary(self) -> dict:
        dirpath = self.get_directory()
        files = self.get_files_list()
        files_count = len(files)
        print(f"{dirpath} : {files_count}")

        dict_counts = {}
        for filename in files:
            filepath = os.path.join(dirpath, filename)
            data = self.get_data(filepath)
            token_dict = self.parse_text(data)
            # Should we use 'keys()' or 'items()'?
            for word in token_dict.keys():
                dict_counts[word] = dict_counts.get(word, 0) + 1

        dict_probabilities = {}
        # type_char = f"p_w|{dirtype[:1]}"
        type_char = "p_w"
        for word, count in dict_counts.items():
            p_w = count/files_count
            ## Ignore words above, below given probability
            if self.p_w_upper_bound >= p_w >= self.p_w_lower_bound:
                dict_probabilities[word] = {"count": count, type_char: p_w}
        

        print(f"{len(dict_probabilities)} words in collection.")
        return dict_probabilities



    

        
