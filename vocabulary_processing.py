# Use to process words
# e.g., remove words appearing in over 90% of spam/ham files
# e.g., remove words having a count of 1

def remove_words_above_threshold(bag : dict, threshold : int) -> dict:
    bag_out={}
    for word in bag:
        print(bag.get(word)[1])
        print(bag.get(word)[2])

def remove_words_below_threshold(bag: dict, threshold : int) -> dict:
    return 0
