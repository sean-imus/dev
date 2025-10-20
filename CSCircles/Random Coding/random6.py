standard_input = "word"

# converts input word to Pig Latin

word = input()

def piglatinmaker(word):
    first_char = word[0]
    return word[1:] + first_char + "ay"

print(piglatinmaker(word))