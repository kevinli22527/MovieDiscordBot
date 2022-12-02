def closeStrings(self, word1: str, word2: str) -> bool:
    # determine if length is the same
    # determine if the frequency of the letters are the same
    # determine if all of one type of letter can be switched to another
    # if all of these are true, return true
    # if any of these are false, return false
    # if the length is not the same, return false
    if len(word1) != len(word2):
        return False
    # make a dictionary for each word
    letterToFreq1 = {}
    for letter in word1:
        if letter in letterToFreq1:
            letterToFreq1[letter] += 1
        else:
            letterToFreq1[letter] = 1
    letterToFreq2 = {}
    for letter in word2:
        if letter in letterToFreq2:
            letterToFreq2[letter] += 1
        else:
            letterToFreq2[letter] = 1
    # if the lengths are different, the letters show in different frequencies        
    if(len(letterToFreq1) != len(letterToFreq2)):
        return False
    # check if set of frequenices is the same
    if set(letterToFreq1.values()) != set(letterToFreq2.values()):
        return False
    return True
