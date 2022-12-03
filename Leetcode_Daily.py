def frequencySort(s: str) -> str:
    # Create a dictionary to store the frequency of each character
    freq = {}
    for char in s:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1
    # Sort the dictionary based on the frequency of each character
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    # Create a string to store the result
    result = ""
    # Loop through the sorted dictionary and append the characters to the result string
    for char, freq in sorted_freq:
        result += char * freq
    return result