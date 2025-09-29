alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

while True:
    k2 = input("Please input k2\n").upper().replace(" ", "")
    if len(k2) < 7:
        print("k2 must be of length at least 7")
        continue
    if any(x not in alpha+" " for x in k2):
        print("k2 can only contain letters of the Latin alphabet (and spaces that will be removed later)")
        continue
    break

print(len(k2))
dic = {}

for i, char in enumerate(k2):
    if char not in dic.values():
        dic[len(dic)] = char

for char in alpha:
    if char not in dic.values():
        dic[len(dic)] = char

print(dic)

dic_r = {char: i for i, char in enumerate(dic.values())}
print(dic_r)

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
        print("Text must be only in the English alphabet, no special characters.")
        continue
    
    amount = input("Enter shift coefficient:\n")
    amount = abs(int(amount)) % 26
    
    if choice == '1':
        # Encoding
        result = "".join([dic[(dic_r[x] + amount) % 26] for x in message])
        print("Encoded message:", result)
    else:
        # Decoding
        result = "".join([dic[(dic_r[x] - amount) % 26] for x in message])
        print("Decoded message:", result)