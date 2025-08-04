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
    
    def predict(self):
        prior = self.prior
        results = {}
        path = self.directory
        for file in os.listdir(path):
            filepath = os.path.join(path, file)
            with open(filepath, "r", errors="ignore") as f:
                data = f.read()
                lines = re.sub("\n", " ", data)
                tokens = lines.split(" ")
                eta = prior
                for token in tokens:
                    found = self.bag_of_words.get(token)
                    if found is not None:
                        # WTF is this?
                        p = found['p_w']
                        p = max(p, 1e-10)
                        eta += math.log((1 - p) / p) if p not in (0, 1) else 0
                # WTF is this?
                eta = max(min(eta, 700), -700)
                results[file] = 1 / (1+math.exp(eta))
        
        return results
                
                
        
    
