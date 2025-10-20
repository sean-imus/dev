standard_input = "E"

# outputs the next character in the alphabet, wrapping from Z to A

char = input()

if char == "Z":
    next_char = ord("A")
else:
    next_char = ord(char) + 1

print(chr(next_char))