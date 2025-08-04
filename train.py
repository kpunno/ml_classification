# TODO: Idea: want to extract each word of concatenated words
# Example: fromsender, not a real word: should be 'from' and 'sender'
# implement dictionary API to find subsets of strings?

# TODO: Stucture variables as key:value pairs?
#   Then we can have dirpath, regex ... etc, in the var file\
#   Yes, this will need to be done, so I can have a variable for the training spam directory, training ham directory, and testing directory

# TODO: Problematic because it is not generalized, has too much knowledge of external factors (ie. hardcoded things)

# TODO: Pass your own lambda to build to define a different way of parsing or something

import os
import re
from typing import Pattern

class Train:
    def __init__(self, directory : str, valid_chars : Pattern = r"^[A-Za-z']+$", stopwords_dir : str = "./stopwords_nltk", p_w_upper_bound : int = 1, p_w_lower_bound : int = 0):
        self.directory = directory
        self.stopwords = self.read_file(stopwords_dir).split("\n")
        # Do we want to include numbers? Possibly should be alphanumeric.
        # Validate tokens (is this the best version?)
        self.valid_chars = valid_chars
        self.p_w_upper_bound = p_w_upper_bound
        self.p_w_lower_bound = p_w_lower_bound

        self.files_list = os.listdir(self.directory)

        self.build()

    def get_directory(self) -> str:
        return self.directory

    def get_files_list(self) -> list:
        return self.files_list

    """
    # Extract text contents from email
    def get_email_contents(self, filepath):
        subject = ""
        with open(filepath, "r", errors="ignore") as file:
            line = ""
            while (line := file.readline()) not in ("\n", ""):
                if "subject" in line.lower():
                    subject = line
            return f"{subject} {file.read().lower()}"
    """
            
    def read_file(self, filepath):
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
    def build(self) -> dict:
        dirpath = self.get_directory()
        files = self.get_files_list()
        files_count = len(files)
        print(f"Building from {dirpath}, with {files_count} files.")

        dict_counts = {}
        for filename in files:
            filepath = os.path.join(dirpath, filename)
            data = self.read_file(filepath)
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
        self.bag_of_words = dict_probabilities



    

        
