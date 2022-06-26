import os
import heapq
class BinaryTreeNode:
    def __init__(self,value,freq) -> None:
        self.value=value 
        self.freq=freq 
        self.left=None 
        self.right=None 

    def __lt__(self,other) -> bool:
        return self.freq < other.freq

    def __eq__(self, other) -> bool:
        return self.freq == other.freq


class Huffman_Coding:
    def __init__(self,path) -> None:
        self.path=path 
        self.__heap=[]
        self.__codes={}
        self.__reverseCodes={}

    
    def __make_freq_dict(self,text):
        d={}
        for i in text:
            if i not in d:
                d[i]=0
            
            d[i]+=1
        return d 


    def __buildheap(self,freq_dict):
        for key in freq_dict:
            frequency = freq_dict[key]
            binaryTreeNode = BinaryTreeNode(key,frequency)
            heapq.heappush(self.__heap,binaryTreeNode)

    def __buildTree(self):
        while len(self.__heap)>1:
            binaryNode1 = heapq.heappop(self.__heap)      
            binaryNode2 = heapq.heappop(self.__heap)  
            freq_sum = binaryNode1.freq+binaryNode2.freq
            newBinaryNode = BinaryTreeNode(None,freq_sum)
            newBinaryNode.left = binaryNode1
            newBinaryNode.right = binaryNode2
            heapq.heappush(self.__heap,newBinaryNode)
        return 
    def __buildCodesHelper(self,root,curr_bits):
        if root is None:
            return 
        if root.value is not None:
            self.__codes[root.value] = curr_bits 
            self.__reverseCodes[curr_bits] = root.value 
            return 
        self.__buildCodesHelper(root.left,curr_bits+"0")
        self.__buildCodesHelper(root.right,curr_bits+"1")

    def __getEncodedText(self,text):
        encoded_text=""
        for i in text:
            encoded_text+= self.__codes[i]
        return encoded_text

    def __buildCodes(self):
        root = heapq.heappop(self.__heap)
        self.__buildCodesHelper(root,"")

    def __get_padded_encoded_text(self,encoded_text):
        padded_amount = 8-(len(encoded_text)%8)

        for i in range(padded_amount):
            encoded_text+='0'
        
        padded_info ="{0:08b}".format(padded_amount)
        padded_encoded_text = padded_info+encoded_text
        return padded_encoded_text
    
    def __getBytesArr(self,padded_encoded_text):
        arr=[]
        for i in range(0,len(padded_encoded_text),8):
            byte = padded_encoded_text[i:i+8]
            arr.append(int(byte,2))
        return arr 

    def compress(self):
        #get file from path
        #read text from file
        file_name,file_extension = os.path.splitext(self.path)
        output_path = file_name+".bin"
        with open(self.path,"r+") as file, open(output_path,"wb") as output:
            text = file.read()
            text = text.rstrip()

            # mmake freq dict using the text 
            freq_dict = self.__make_freq_dict(text)

            #construct the heap from freq dict 

            self.__buildheap(freq_dict)

            #construct the binary tree 
            self.__buildTree()

            #construct the codes from BinaryTree 

            self.__buildCodes()

            #creating the encoded text using code 
            encoded_text =self.__getEncodedText(text)
            #pad this encoded text 
            padded_encoded_text = self.__get_padded_encoded_text(encoded_text)

            bytes_arr = self.__getBytesArr(padded_encoded_text)

            #return this binary file as output 
            final_bytes = bytes(bytes_arr) 

            output.write(final_bytes)
        print("Compressed")
        return output_path 
    
    def __removePadding(self,text):
        padding_info=text[:8]
        extra_padding = int(padding_info,2)

        text = text[8:]
        text_after_remove_paddding = text[:-1*extra_padding]
        return text_after_remove_paddding
    
    def __decodeText(self,text):
        decode_text=""
        current_bits=""
        for bit in text:
            current_bits+=bit 
            if current_bits in self.__reverseCodes:
                character = self.__reverseCodes[current_bits]
                decode_text+=character 
                current_bits = ""
        return decode_text

    
    
    def decompress(self,input_path):
        filename,fileextension = os.path.splitext(self.path)
        output_path = filename+"_decompressed"+".txt"
        with open(input_path,'rb') as file , open(output_path,'w') as output:
            bit_string=""
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8,"0")
                bit_string+=bits
                byte = file.read(1)
            actual_text = self.__removePadding(bit_string)
            decompressed_text = self.__decodeText(actual_text)
            output.write(decompressed_text)
        return

path=r"C:\Users\Asus\OneDrive\Desktop\sample.txt"
h=Huffman_Coding(path)
output_path = h.compress()
h.decompress(output_path)




