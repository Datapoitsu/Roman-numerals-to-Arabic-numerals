# -------------------- Roman Arabic Converter -------------------- ##
#Written by: Aarni Junkkala
#Code turns numbers from Roman to Arabic and vice versa.
#Limit of Roman numbers is from 1 to 3999 -> I -> MMMCMXCIX, can't convert numbers higer than that.

#If you want to call this script from outside, call: Convert(str || int)
RomanSymbols = ["I","V","X","L","C","D","M"]

def FilterValidSymbols(text:str,validSymbols:list[str]) -> str: #Keeps only symbols that are allowed
    result = ""
    for i in range(len(text)):
        if text[i] in validSymbols:
            result += text[i]
    return result

def AllSame(arr:list) -> bool: #Are all elements same in the array
    for i in range(1,len(arr)):
        if arr[i] != arr[0]:
            return False
    return True

def isRepetitive(arr:list,count:int) -> bool:
    for i in range(len(arr) - 3):
        if AllSame(arr[i:i+count]):
            return True
    return False

def romanIndex(char:chr) -> int:
    return RomanSymbols.index(char)

def romanIndexes(text:str) -> list[int]:
    result = []
    for i in range(len(text)):
        result.append(romanIndex(text[i]))
    return result

def inRange(arr:list,index:int|list[int]):
    if type(index) == int:
        index = [index]
    for i in range(len(index)):
        if index[i] < 0 or index[i] > len(arr) - 1:
            return False
    return True

def validSymbols(text:str) -> bool:
    for i in range(len(text)):
        if text[i].isdigit():
            return False
        if text[i].isalpha() and text[i] not in RomanSymbols:
            return False
    return True

def isLegalRoman(text:str) -> bool:
    if isRepetitive(text,4): #Error check: Max 3 of same symbol
        return False
    indexList = romanIndexes(text) #Converts to numbers matching indexes of roman numbers in ascending order.
    for i in range(len(indexList)):
        if indexList[i] % 2 == 0: #I, X, C, M = 1, 10, 100, 100
            if inRange(indexList,i + 1) and indexList[i+1] > indexList[i] + 2: #multiple of 10 must be followed by two greater or smaller. Correct: XL, incorrect XD.
                return False
            if inRange(indexList, [i - 1, i + 1]) and indexList[i - 1] < indexList[i] and indexList[i + 1] == indexList[i - 1]: #After reduction can't be followed by same number as before.
                return False
        if indexList[i] % 2 == 1: #V, L, D = 5, 50 ,500
            if inRange(indexList, i + 1) and indexList[i+1] > indexList[i]: #Next can't be greater.
                return False
            if inRange(indexList, i - 2) and indexList[i - 2] < indexList[i]: #If previos is reduced, this can't be in same range.
                return False
            if inRange(indexList, i + 1) and indexList[i] == indexList[i + 1]: #No repeats.
                return False
    return True

def IndevidualRomanToArabic(roman:str): #Converts indeviual symbols to arabic numbers, Example: XIV -> [10,1,5]
    numberList = []
    indexList = romanIndexes(roman) #Converts to numbers matching indexes of roman numbers in ascending order.
    for i in range(len(roman)):
        #Adds numbers based on following table [1,5,10,50,100,500,1000]
        numberList.append(10 ** ((indexList[i] + (indexList[i] % 2)) / 2) / (1 if indexList[i] % 2 == 0 else 2)) #What a nightmare of a formula!
    return numberList

def RomanToArabic(roman:str) -> int:
    roman = roman.upper()

    if not validSymbols(roman): #If contains invalid symbols.
        return None

    roman = FilterValidSymbols(roman, RomanSymbols) #Filtering spaces and special characters.
        
    if not isLegalRoman(roman):
        return None
    
    numberList = IndevidualRomanToArabic(roman) #Converting all roman symbols to indevidual numbers.

    #Calculates the reduction. XLIV -> [-10 + 100, -1 + 5] -> [90,4]
    result = 0
    iteration = iter(range(len(numberList)))
    for i in iteration:
        if i < len(numberList) -1 and numberList[i] < numberList[i + 1]:
            result += numberList[i + 1] - numberList[i]
            next(iteration)
        else:
            result += numberList[i]

    return int(result)

def ArabicToRoman(arabic:int|str) -> str:
    try:
        int(arabic)
    except:
        return None
    
    numberList = list(map(int,list(str(arabic)))) #Example: 123 -> [1,2,3]
    Result = ""
    for i in range(len(numberList)):
        match numberList[i]:
            case 0:
                continue
            case 1 | 2 | 3:
                for k in range(numberList[i]):
                    Result += RomanSymbols[2 * (len(numberList) - i) - 2] #1,10,100,1000
            case 5:
                Result += RomanSymbols[2 * (len(numberList) - i) - 1] #5,50,500
            case 6 | 7 | 8:
                Result += RomanSymbols[2 * (len(numberList) - i) - 1] #5,50,500
                for k in range(numberList[i] - 5):
                    Result += RomanSymbols[2 * (len(numberList) - i) - 2] #1,10,100,1000
            case 4:
                Result += RomanSymbols[2 * (len(numberList) - i) - 2] #1,10,100,1000
                Result += RomanSymbols[2 * (len(numberList) - i) - 1] #5,50,500
            case 9:
                Result += RomanSymbols[2 * (len(numberList) - i) - 2] #1,10,100,1000
                Result += RomanSymbols[2 * (len(numberList) - i)] #1,10,100,1000
    return Result

def Convert(number:str|int) -> int|str|None:
    if number in ["",None]:
        return None
    
    try: #checking the type. Numbers can also be inputted as a string.
        number = int(number) #If it can be a integer, then it is arabic
    except:
        number = str(number) #If it can't be an integer, then it could be roman
    
    #Arabic to Roman
    if isinstance(number, int) and number > 0 and number < 4000: #Can't be too high or low
        return ArabicToRoman(number)
    #Roman to Arabic
    if isinstance(number, str):
        return RomanToArabic(number)
    return None

def TestMatching(): #Tests that the functions return mirrored answers.
    incorrect = []
    for i in range(1,4000):
        if RomanToArabic(ArabicToRoman(i)) != i:
            incorrect.append(i)
    if len(incorrect) == 0:
        print("No errors!")
        return

    print("Incorrect at")
    for i in range(len(incorrect)):
        print(str(i) + " ",end="")

if __name__ == '__main__':
    while True:
        print("--------------------")
        print("Roman to Arabic to Roman number converter")
        UserInput = input("Insert number: ")
        if UserInput in ["","exit"]:
            break
        print(Convert(UserInput))