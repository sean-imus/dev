standard_input = "Fairy"

# switches first and last character of input word

word = input()

char_count = len(word)

first_char = word[0]
last_char = word[char_count - 1]

print(last_char + word[1:char_count - 1] + first_char)