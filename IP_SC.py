
myIPformat="10.109."
myIPformat2="172.16."

outputFile=open("./SCIPout.txt", "w")

mystr=""
myIPs=""

with open('./SCIPin.txt') as f:
    #myOutputString[0][0]=f.readline()
    
    #next(f)
    mylines=f.readlines()       # reading all lines in a file
    #print(mylines)
    totallines = len(mylines)   # counting the number of lines in the file
    #print(totallines)
    #print(totallines)
    
    outputListColumn = 4
    myOutputList = [['a'] * outputListColumn] * totallines
    #finalOutput = ['a'] * totallines
    
    myOutputList[0][0]=mylines[0]
    myOutputList[0][1]=''
    myOutputList[0][2]=''

    #print(myOutputList)

    finalOutput = mylines[0]
    outputFile.write(finalOutput)

    outputListRow=1
    toIncrementColumn=0


    for myaddr in mylines[1:]:
        #print(myOutputList[m][0])
        print("outputListRow: ",outputListRow)
        outputListColumn=0
        myQuotes=0
        
        myOutputList[outputListRow][0]=''
        myOutputList[outputListRow][1]=''
        myOutputList[outputListRow][2]=''
        
        myeol=len(myaddr)
        for counter in range(0, myeol):
            if myaddr[counter]=='\"' :
                myQuotes+=1
                if myQuotes<9:
                    myOutputList[outputListRow][outputListColumn]+=myaddr[counter]
                else:
                    if myQuotes%2==1:
                        myOutputList[outputListRow][outputListColumn]+=myaddr[counter]
                        if(myQuotes==9):
                            outputListColumn+=1

                    else:
                        if(myQuotes==10):
                            outputListColumn+=1
                        #print(len(myOutputList))
                        myOutputList[outputListRow][outputListColumn]+=myaddr[counter]

            else:
                myOutputList[outputListRow][outputListColumn]+=myaddr[counter]
                
        #print(outputListRow, end=" ")
        #print(outputListColumn, end=" ")
        
        print("Length of this row", len(myOutputList[outputListRow][1]))
        #print(" ")

        myIPList=myOutputList[outputListRow][1]
        print(myOutputList[outputListRow][1])
        myeol=len(myIPList)

        for counter in range(0, myeol):
            
            if (myIPList[counter]!=' '):
                if (myIPList[counter]!=','):
                    mystr+=myIPList[counter]
                    
                else:
                    if ((myIPformat in mystr) or (myIPformat2 in mystr)):
                        if (myIPs==""):
                            myIPs+=mystr
                        else:
                            myIPs=myIPs+", "+mystr
                    
                    mystr=""
                if (counter==(myeol-1)):
                    
                    if ((myIPformat in mystr) or (myIPformat2 in mystr)):
                        if (myIPs==""):
                            myIPs+=mystr
                        else:
                            myIPs=myIPs+", "+mystr
                    
                    mystr=""
        #print(myIPs)
        myOutputList[outputListRow][1]=myIPs
        outputOne=myOutputList[outputListRow][0]
        print(myOutputList[outputListRow][0])
        print(myOutputList[outputListRow][1])
        print(myOutputList[outputListRow][2])
        #outputTwo=myIPs
        print(myIPs)
        outputThree=myOutputList[outputListRow][2]
        concatOutput=outputOne+myIPs+outputThree
        #finalOutput[outputListRow]= str(myOutputList[outputListRow][0]) + str(myOutputList[outputListRow][1]) + str(myOutputList[outputListRow][2])
        #finalOutput[outputListRow]=concatOutput
        #print(myOutputList[outputListRow][0], end="")
        #print(myOutputList[outputListRow][1], end="")
        #print(myOutputList[outputListRow][2], end="")
        #print(finalOutput[outputListRow])
        
        print(" ")
        #outputFile.write(myIPs+"\n")
        myIPs=""

        outputFile.write(concatOutput)

        outputListRow+=1
        
        #print(" ")
            
        

    #for myaddr in f.readlines():
    #    print(myaddr)
        
    """
        myeol=len(myaddr)
        for counter in range(0, myeol):
            
            if (myaddr[counter]!=' '):
                if (myaddr[counter]!=','):
                    mystr+=myaddr[counter]
                    
                else:
                    if ((myIPformat in mystr) or (myIPformat2 in mystr)):
                        if (myIPs==""):
                            myIPs+=mystr
                        else:
                            myIPs=myIPs+", "+mystr
                    
                    mystr=""
                if (counter==(myeol-1)):
                    
                    if ((myIPformat in mystr) or (myIPformat2 in mystr)):
                        if (myIPs==""):
                            myIPs+=mystr
                        else:
                            myIPs=myIPs+", "+mystr
                    
                    mystr=""
        #print(myIPs)
        outputFile.write(myIPs+"\n")
        myIPs=""
    """

outputFile.close()



