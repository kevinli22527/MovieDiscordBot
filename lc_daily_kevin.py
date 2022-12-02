def closeStrings(self, word1: str, word2: str) -> bool:
    # if I can swap any two existing characters, then I can change all anagrams to the same word => frequency hashmaps must be the same for anagrams

    # if I can exchange all occurences of a character with another, I would essentially be exchanging the character frequencies

    # but, if there is a character that appears in one string but not the other, then there's no way to make the strings equal

    # I claim that if the strings contain the same set of characters AND the count of all the character frequencies (frequencies of all the frequencies) is the same for both strings, then the strings are "close". Since I would exchange the frequencies using Operation 2 and make anagrams on the identical frequency hashmaps using Operation 1

    # check if the strings contain the same set of characters
    if set(word1) != set(word2):
        return False

    # check if the count of all the character frequencies is the same for both strings------------------------------------------

    # 1. make a frequency dictionary (hashmap) for each word
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

    # 2. check if the count of all the character frequencies is the same for both strings
    frequncies1 = letterToFreq1.values()
    frequncies2 = letterToFreq2.values()
    count_freqencies1 = {}
    count_freqencies2 = {}
    for frequency in frequncies1:
        if frequency in count_freqencies1:
            count_freqencies1[frequency] += 1
        else:
            count_freqencies1[frequency] = 1

    for frequency in frequncies2:
        if frequency in count_freqencies2:
            count_freqencies2[frequency] += 1
        else:
            count_freqencies2[frequency] = 1

    if count_freqencies1 != count_freqencies2:  # check if the frequency of frequencies is the same for both strings
        return False

    return True
    
    