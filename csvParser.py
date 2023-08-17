import csv


#configAccountID=[]
configInstanceID=[]     #needed for matching with ARC 
#configInstanceType=[]
#configStatus=[]
configPrivateIP=[]
#configZone=[]  
#configTags=[]
#configPublicIP=[]
#configPlatform=[]
ssmIP=[]
#########################
securityIP=[]
tempIP=[]
##############################

arcInstanceID=[]
arcIP=[]
arcIPs=[]
arcEmptyID=[]
##############################
myIPformat="10.109."
myIPformat2="172.16."
mystr=""
myIPs=""

uniqueIPs=[]

##############################




""" getting Config IPs """

with open('./Data/Config.csv', 'r') as configFile:
    reader=csv.DictReader(configFile)

    for items in reader:
        #configAccountID.append(items['accountId'])
        configInstanceID.append(items['resourceId'])
        #configInstanceType.append(items['configuration.instanceType'])
        #configStatus.append(items['configuration.state.name'])
        configPrivateIP.append(items['configuration.privateIpAddress'])
        #configZone.append(items['availabilityZone'])
        #configTags.append(items['tags'])
        #configPublicIP.append(items['configuration.publicIpAddress'])
        #configPlatform.append(items['configuration.platform'])
""" ----------------------------------------------------------------------------------------- """


""" making a list of Unique IPs, AWS Config is the baseline, since there are no duplicates """
#uniqueIPs=configPrivateIP

for items in range(len(configPrivateIP)):
    uniqueIPs.append(configPrivateIP[items]) 
""" If you are wondering why the above two lines are added and the other line is commented out """
""" try uncommenting the other line, and commenting the above two and running the script """
""" if you know the exact reason for the bug, please feel free to let me know """
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
for items in range(len(tempIP)):  #tempIP is the security IP
    ipFound=0
    for jtems in range(len(uniqueIPs)):
        if (tempIP[items]==uniqueIPs[jtems]):
            ipFound=1
        #break
    if (ipFound==0):
        uniqueIPs.append(tempIP[items])


for items in range(len(ssmIP)):
    ipFound=0
    for jtems in range(len(uniqueIPs)):
        if (ssmIP[items]==uniqueIPs[jtems]):
            ipFound=1
        #break
    #print(ipFound)
    if (ipFound==0):
        uniqueIPs.append(ssmIP[items])


for items in range(len(arcIP)):
    ipFound=0
    for jtems in range(len(uniqueIPs)):
        if (arcIP[items]==uniqueIPs[jtems]):
            ipFound=1
    if (ipFound==0):
        uniqueIPs.append(arcIP[items])
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
            #print(arcIPs[mtems])
            ipPresent="yes"
            #print(arcIPs[jtems])
    inARC.append(ipPresent)

print("IP Address,","Config,","SSM,","Security,","ARC")
for items in range(0,totalIPs):
    print(uniqueIPs[items], ",", inConfig[items], ",", inSSM[items], ",", inSecurity[items], ",", inARC[items])

print("\n \n \n")

print(arcEmptyID)