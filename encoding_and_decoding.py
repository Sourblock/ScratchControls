def lettersTest():
    setLetters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_- \n,;.():/*\\'
    letters = []
    for i in range(0,9):
        letters.append("")
    for i in range(0,len(setLetters)):
        letters.append(setLetters[i])
    
    return letters

def encode(string):
    encoded = ''
    letters = lettersTest()
    for i in range(0,len(string)):
        temp = letters.index(string[i]) + 1
        encoded = str(encoded) + str(temp)
    
    return encoded

def decode(input):
    decoded = ''
    letters = lettersTest()
    for i in range(1,len(str(input)),2):
        item = str(input)[i-1] + str(input)[i]
        temp = letters[int(item) - 1]
        decoded = str(decoded) + str(temp)
    
    return decoded

def main():
    
    lettersTest()
    print(encode("SB115"))
    print(decode("5437626266"))

if __name__ == "__main__" :
    main()