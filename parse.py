
# return a bag of words from a list of files

import os
import re
from typing import Pattern

stopwords_default_dir = "./stopwords_nltk"
# alphabet validation including apostrophe
validation_pattern_default = r"^[A-Za-z']+$" 

# probability omit (unused)
p_upper_bound_default = 1
p_lower_bound_default = 0

class Parse:
    def __init__(
            self,
            dir : str, # should not contain dirs, should only contain files
            type : str, # spam or ham
            valid_chars : Pattern = validation_pattern_default,
            stopwords_dir : str = stopwords_default_dir,
    ):
        if type not in ("spam","ham"):
            raise ValueError("type must match \"spam\" or \"ham\"")
        self.filepath_list = [os.path.join(dir,file) for file in os.listdir(dir)]
        self.files_count = len(self.filepath_list)
        self.valid_chars = valid_chars
        self.stopwords = self.read_file(stopwords_dir).split("\n") # list
            
    def read_file(self, filepath):
        with open(filepath, "r", errors="ignore") as file:
            return file.read().lower()

    # regex full matching
    def charset_full_match(self, token):
        return True if re.fullmatch(self.valid_chars, token) else False

    # regex partial matching
    def charset_match(self, token):
        return True if re.match(self.valid_chars, token) else False

    # parse text file, return organized tokens
    def tokenize_file(self, data: str) -> dict:
        cleaned_tokens=[]
        line = re.sub(r"\n", " ", data) # want to form a line from a file
        line = re.sub(r"[.,:\-!]","", line) # want to remove punctuation marks
        tokens = line.split(" ") # want to get tokens from the result of these actions
        for token in tokens:
            token = token.strip() # trim whitespace from token
            if self.charset_full_match(token) and token not in self.stopwords: # full match against alphabet
                cleaned_tokens.append(token)
        return dict.fromkeys(cleaned_tokens, 1)

    # build bag of words from scratch
    def build_bag_of_words(self) -> dict:
        filepaths = self.filepath_list
        with_counts = {}
        for path in filepaths:
            data = self.read_file(path)
            token_dict = self.tokenize_file(data)
            # Should we use 'keys()' or 'items()'?
            for word in token_dict.keys():
                with_counts[word] = with_counts.get(word, 0) + 1
        
        return with_counts






    

        
