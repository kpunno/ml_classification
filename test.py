
class Classifier:
    def __init__(self, bag_of_words : dict, prior : float):
        if not (1 >= prior >= 0):
            raise ValueError("Prior is a value between 0 and 1 inclusive")
        self.prior = prior
        self.bag_of_words = bag_of_words
    
