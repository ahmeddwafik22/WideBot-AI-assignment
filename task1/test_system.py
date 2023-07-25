import spell_checker

## make object from spell_checker

spell_system=spell_checker.spell_checker()

## search for word "hello"
search=spell_system.searchWord("hello")
if(search):
    print("The word exist")
else:
    print("The word doesn't exist")

## try add word

spell_system.addWord("hello")

## search for it
search=spell_system.searchWord("hello")
if(search):
    print("The word exist")
else:
    print("The word doesn't exist")

## store dictionary
spell_system.storeWords("dictionary.txt")
search=spell_system.searchWord("aa")
if(search):
    print("The dictionary stored successfully")
else:
    print("The dictionary not stored")

## get 4 nearest word
nearest_words=spell_system.get_nearest_words("abandon")
print("nearest words are" ,nearest_words)

