import os
import re
import math

class Test:
    def __init__(self, bag_of_words : dict, directory : str, prior : float):
        if not (1 >= prior >= 0):
            raise ValueError("Prior is a value between 0 and 1 inclusive")
        self.directory = directory
        self.prior = prior
        self.bag_of_words = bag_of_words

    def classify_file(self):
        return 0
    
    def classify_directory(self):
        directories = os.listdir(self.directory)
        print(directories)
        """
        for each dir in directories:
            open directory ...
            ...
            
        """
        results = {}
        path = os.path.join(self.directory, "spam")
        for file in os.listdir(path):
            filepath = os.path.join(path, file)
            with open(filepath, "r", errors="ignore") as f:
                data = f.read()
                lines = re.sub("\n", " ", data)
                tokens = lines.split(" ")
                prb= math.log(self.prior)
                for token in tokens:
                    found = self.bag_of_words.get(token)
                    if found is not None:
                        prb += math.log(found['p_w'])
                results[file] = math.exp(prb)
        for result, probability in results.items():
            print(result, probability)
                
                
        
    
