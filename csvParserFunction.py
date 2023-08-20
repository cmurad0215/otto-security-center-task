import csv

configInstanceID=[]     #needed for matching with ARC 
configPrivateIP=[]
ssmIP=[]
##########################################################################################
securityIP=[]
tempIP=[]
##########################################################################################
arcInstanceID=[]
arcIP=[]
arcIPs=[]
arcEmptyID=[]
##########################################################################################
myIPformat="10.109."
myIPformat2="172.16."
mystr=""
myIPs=""
##########################################################################################
uniqueIPs=[]
##########################################################################################
duplicateSSM=[]
duplicateARC=[]
duplicateSecurity=[]
duplicateConfig=[]
"""##########################################################################################"""
def populateUniqueIPs(source_list, destination_list):   # function - name says it all
    for items in range(len(source_list)):  #tempIP is the security IP
        ipFound=0
        for jtems in range(len(destination_list)):
            if (source_list[items]==destination_list[jtems]):
                ipFound=1
        #break
        if (ipFound==0):
            destination_list.append(source_list[items])
"""##########################################################################################"""
def populateDuplicateIPs(source_list, destination_list):
    for item in range(len(source_list)):
        potentialDuplicateIP=source_list[item]
        ipFound=0
        for jtems in range(len(destination_list)):
            if (potentialDuplicateIP==destination_list[jtems]):
                ipFound=1
                #print(destination_list[jtems])
        if (ipFound==0):
            for jtems in range(item+1, len(source_list)):
                if (potentialDuplicateIP==source_list[jtems]):
                    destination_list.append(potentialDuplicateIP)
"""##########################################################################################"""

""" getting Config IPs """
with open('./Data/Config.csv', 'r') as configFile:
    reader=csv.DictReader(configFile)

    for items in reader:
        configInstanceID.append(items['resourceId'])
        configPrivateIP.append(items['configuration.privateIpAddress'])
""" ----------------------------------------------------------------------------------------- """


""" making a list of Unique IPs, AWS Config is the baseline, since there are no duplicates """
print(len(uniqueIPs))
populateUniqueIPs(configPrivateIP,uniqueIPs)
""" ----------------------------------------------------------------------------------------- """


""" getting SSM IPs """
with open('./Data/SSM.csv', 'r') as ssmFile:
    reader=csv.DictReader(ssmFile)

    for items in reader:
        ssmIP.append(items['IP address'])
""" ----------------------------------------------------------------------------------------- """



""" getting Security IPs """
with open('./Data/Security.csv', 'r') as securityFile:
    reader=csv.DictReader(securityFile)

    for items in reader:
        securityIP.append(items['Device IPs'])
""" ----------------------------------------------------------------------------------------- """



""" extracting IPs in the format from the Security Center IPs """
for items in range(0, len(securityIP)):
    myIPList=str(securityIP[items])
    myeol=len(myIPList)

    for counter in range(0, myeol):
                
                if (myIPList[counter]!=' '):
                    if (myIPList[counter]!=','):
                        mystr+=myIPList[counter]
                        
                    else:
                        if ((myIPformat in mystr) or (myIPformat2 in mystr)):
                            tempIP.append(mystr)
                        mystr=""

                    if (counter==(myeol-1)):
                        if ((myIPformat in mystr) or (myIPformat2 in mystr)):
                            tempIP.append(mystr)
                        
                        mystr=""

    myIPs=""

""" ----------------------------------------------------------------------------------------- """


""" getting ARC Instance IDs """
with open('./Data/ARC.csv', 'r') as arcFile:
    reader=csv.DictReader(arcFile)

    for items in reader:
        arcInstanceID.append(items['NAME'])
""" ----------------------------------------------------------------------------------------- """

""" Getting corresponding IPs for ARC Instance IDs, two lists are maintained, one with blanks and one without """
""" I know it's just lazy, but doing it, may be will improve on this at a later date """
for items in range(0,len(arcInstanceID)):
    ipFound=0
    for searchIPs in range(0, len(configInstanceID)):
        if (arcInstanceID[items]==configInstanceID[searchIPs]):
            arcIP.append(configPrivateIP[searchIPs])
            arcIPs.append(configPrivateIP[searchIPs])
            ipFound=1
            break
    if (ipFound==0):
        arcIP.append("")
        arcEmptyID.append(arcInstanceID[items])
""" ----------------------------------------------------------------------------------------- """


""" adding more Unique IPs from the rest 3 lists """
populateUniqueIPs(tempIP,uniqueIPs)
populateUniqueIPs(ssmIP,uniqueIPs)
populateUniqueIPs(arcIP,uniqueIPs)
""" ----------------------------------------------------------------------------------------- """

tempStr=""
inConfig=[]
inSSM=[]
inSecurity=[]
inARC=[]

totalIPs=len(uniqueIPs)

for items in range(0,totalIPs):
    ipPresent="no"
    for jtems in range(0, len(configPrivateIP)):
        if (uniqueIPs[items]==configPrivateIP[jtems]):
            ipPresent="yes"
    inConfig.append(ipPresent)
    
    ipPresent="no"
    for ktems in range(0, len(ssmIP)):
        if (uniqueIPs[items]==ssmIP[ktems]):
            ipPresent="yes"
    inSSM.append(ipPresent)
    
    ipPresent="no"
    for ltems in range(0, len(tempIP)):
        if (uniqueIPs[items]==tempIP[ltems]):
            ipPresent="yes"
    inSecurity.append(ipPresent)
    
    ipPresent="no"
    for mtems in range(0, len(arcIPs)):
        if (uniqueIPs[items]==arcIPs[mtems]):
            ipPresent="yes"
    inARC.append(ipPresent)

header="IP Address,Config,SSM,Security,ARC"
populateDuplicateIPs(tempIP,duplicateSecurity)
populateDuplicateIPs(arcIPs,duplicateARC)
populateDuplicateIPs(configPrivateIP,duplicateConfig)
populateDuplicateIPs(ssmIP,duplicateSSM)

print("Duplicate Security IPs are: ", duplicateSecurity)
print("Duplicate ARC IPs are: ", duplicateARC)
print("Duplicate Config IPs are: ", duplicateConfig)
print("Duplicate SSM IPs are: ", duplicateSSM)

outputFile = open("./Data/finalList.csv", "w")
outputFile.write(header)
for items in range(0,totalIPs):
    outputFile.write("\n")
    saveToFile=uniqueIPs[items]+","+inConfig[items]+","+inSSM[items]+","+inSecurity[items]+","+inARC[items]
    outputFile.write(saveToFile)
outputFile.close()

print("ARC servers not found in AWS Config are:",arcEmptyID)
