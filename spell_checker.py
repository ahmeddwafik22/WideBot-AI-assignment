## store the dictionary using prefix (trie) tree

maxChar=26 #there are 26 possible on each node in the tree
class trieNode:
    def __init__(self) -> None:
        self.index = None ## it stores the index of the word array if it is None means that this prefix node is not end of the word
        self.child = [None for i in range(maxChar)]  #26 possible child initizalize them None

class spell_checker():
    def __init__(self):
        self.root=trieNode()
        self.words=[] ## this is the dictionary array when we read from file, additionally on it any word we insert on the tree
                      ##O(N) space complexity, where N is the number of words

        self.index_after_word=None ## this index will be used to store the index of nearest word which after it in lexicographic order

        self.backtracked_words=[] ## this function will store words which share the same first character in the given word that we want to get its neighbour
                                  ## O(N) space complexity where N is the number of words that has the first char in the word



    ## addWord takes O(N) time complexity where N is the number of Chracters in the word
    def addWord(self,word:str,idx=-1):
        if(idx==-1): ## if idx==-1 means that word not from dictionary so we add it at the end of the words dictionary array
            self.words.append(word)
            idx=len(self.words)-1
        word=word.lower()
        cur = self.root
        for c in word:
            # taking ascii value
            ind = ord(c) - ord('a')
            # making a new path if not exist
            if cur.child[ind]==None:
                cur.child[ind] = trieNode()
            # go to next node
            cur = cur.child[ind]

        cur.index=idx ## make it true to know that this node is end of word


    ## searchWord takes O(N) time complexity where N is the number of Chracters in the word
    def searchWord(self,word):
        word=word.lower()
        cur=self.root
        for c in word:
            ind = ord(c) - ord('a')
            if  cur.child[ind]==None: ## if character node not from parent child ,so this word not in the tree,so we stop traverse
                return False
            cur=cur.child[ind]

        return True if cur.index is not None else False ## if we dont reach the end of the word, so this word not in the tree, so it return false

    #it takes O(N*K) time complexity where N is the number of words as we loop on them and K is length of the string as we replace invalid chracters
    def preprocess_words(self,words):
        words=[word.replace("\n","").replace("'","")  for word in words if "\ufffd"  not in word] ##take only valid words and clean word from "\n" or "'"
        return words


    ## this function read words from file
    ## it takes O(N*K) time complexity
    def get_words_from_path(self,file_path):
        words=None
        try:
            with open(file_path, "r", encoding="utf-8",errors="replace") as file:  ##it takes O(N) time complexity where N is the number of words
                words = file.readlines()
        except Exception as e:
            print(f"No such path: {file_path} ")
            return self.words
        words=self.preprocess_words(words) # O(N*K)
        self.words+=words

        return words

    ## it takes O(N*K) time complexity
    ## it stores the words by looping through them and using insertWord method
    def storeWords(self,file_path):
        words=self.get_words_from_path(file_path) #O(N*K) time complexity
        if words:
            for idx,word in enumerate(words):# O(N*K) time complexity
             self.addWord(word) #O(k) where k is the length of the string


    #O(K*N) time complexity where K is the number of nodes and N is the length of the string
    ## this function will keep track of all childs of specific nodes from ascending order which will help us to get the nearest words
    def backTrack(self,node,word):
        if (node == None):
            return
        for i in range(maxChar):
            if (node.child[i] != None):
                if node.child[i].index is not None:
                    self.backtracked_words.append(self.words[node.child[i].index]) ##store the backtracked word in the backtracked array
                    if(word==self.backtracked_words[-1]):
                        self.backtracked_words.remove(self.backtracked_words[-1]) ##remove the given target word if it exist in the backtracked array
                    try:
                        if(word<self.backtracked_words[-1] and self.index_after_word is None):
                            self.index_after_word= len(self.backtracked_words) - 1 ##store the index of the first after word in lexicographic order to the given word
                    except:
                        pass
            self.backTrack(node.child[i],word)
        return self.index_after_word

    #O(K*N) time complexity where K is the number of nodes and N is the length of the string
    ## this function get the 4 nearest word that share the same first char
    def get_nearest_words(self,word):
        nearest_words=[] ## O(4)=O(1) space complexity
        word=word.lower()
        ind =ord(word[0])-ord('a')

        try:
            if self.root.child[ind].index is not None:
                self.backtracked_words.append(self.words[self.root.child[ind].index])
                if(word==self.backtracked_words[-1]):
                    self.backtracked_words.remove(self.backtracked_words[-1])
        except:
            return []

        first_nearest_index=self.backTrack(self.root.child[ind],word) ##O(K*N) time complexity

        ## after getting the index we start add this word by this index , the word by index+1 , index-1 and index-2 in the nearest_words array

        ## example suppose that the words is ['a','b','d','e'] and the target word is 'c'
        ## backtracked method will return index 2 which is the index that word in array after c in lexicographic order
        ## so we make that append in the nearest_words: words[index],words[index+1],words[index-1],words[index-2]

        try:
            nearest_words.append(self.backtracked_words[first_nearest_index])
        except:
            pass
        try:
            nearest_words.append(self.backtracked_words[first_nearest_index + 1])
        except:
            pass
        try:
            if(first_nearest_index-1>=0):
                nearest_words.append(self.backtracked_words[first_nearest_index - 1])
        except:
            pass
        try:
            if(first_nearest_index-2>=0):
                nearest_words.append(self.backtracked_words[first_nearest_index - 2])
        except:
            pass

        if(first_nearest_index is None): ## if first_nearest_index is none means the given word is greater than all words in the array, so we return last 2 words in the array
            try:
                nearest_words.append(self.backtracked_words[-1])
                nearest_words.append(self.backtracked_words[-2])

            except:
                pass

        self.backtracked_words=[]
        self.index_after_word=None


        return nearest_words
