dict = {i-65: chr(i) for i in range(65, 65+26)}
dict_r = {chr(i): i-65 for i in range(65, 65+26)}

print(dict)
print(dict_r)

while True:
    choice = input("Enter 1 to encode, 2 to decode, or 3 to exit: ")
    
    if choice == '3':
        print("Exiting the program.")
        break
    
    if choice not in ['1', '2']:
        print("Invalid choice. Please enter 1, 2, or 3.")
        continue
    
    message = input("Enter text to process:\n").upper().replace(" ", "")
    if not message.isalpha():
        print("Text must be only in the English alphabet, no special chars.")
        continue
    
    amount = input("Enter shift coefficient:\n")
    amount = abs(int(amount)) % 26
    
    if choice == '1':
        # Encoding
        result = "".join([dict[(dict_r[x] + amount) % 26] for x in message])
        print("Encoded message:", result)
    else:
        # Decoding
        result = "".join([dict[(dict_r[x] - amount) % 26] for x in message])
        print("Decoded message:", result)