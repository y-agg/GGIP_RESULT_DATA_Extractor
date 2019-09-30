from tabula import read_pdf
from PyPDF2 import PdfFileReader
import json
from os import path


def rectify(SIDindex,df):
    rectifying=[]
    local=""
    ddf=list(df[2])
    counts=0
    for i in ddf:
        if str(type(i))=="<class 'str'>":
            if SIDindex in i:
                break
        counts+=1     
    for i in df.columns:
        if str(type(df.loc[counts,i]))=="<class 'str'>":    
            if "-" in df.loc[counts,i] or "SID:" in df.loc[counts,i]:
                pass
            else:
                local=local+" "+df.loc[counts,i]
    local=local+"  "+"None"
    
    local=local.split(" ")
    for j in local:
        if j=='':
            local.pop(local.index(j))
    rectifying.append(local)
  
    local=""
    for i in df.columns:
        if str(type(df.loc[counts,i]))=="<class 'str'>":    
            if "-" in df.loc[counts,i]:
                local=local+df.loc[counts,i]
    if local.split("  ")[-1]:
        rectifying.append(local.split("  ")[-1])   
    else:
        rectifying.append("A")
    print (local )
    return
    print( rectifying)

def result(link,page,pge):
    stud={}
    li=[]
    SID=[]
    df = read_pdf(link+'.pdf',pages=pge, multiple_tables=True)
    if len(df)!=2:
        return
    df=df[1]
    
    var=list(df[2])
    for i in var[1:]:
        if str(type(i))=="<class 'str'>":
            if "SID:" in i:
                SID.append(i)       
    for i in var[1:]:
        if str(type(i))=="<class 'str'>":
            if "SID:" in i or "SchemeID:" in i:
                continue
            else:
                li.append(i)
    count=0
    for i in range(0,len(li),2):    
        stud={
        "Name":li[i+1],
        "Roll_no":li[i],
        "Marks":rectify(SID[count],df)
        } 
        count+=1
        page.append(stud)    


def page1st(link,frames):
    frame={}
    page1 = read_pdf(link+'.pdf')
    for i in page1:
        li=[]
        for j in page1[i]:
            li.append(j)
        frame[i]=li
    for i in frame:
        if i=="Code" or i=="Unnamed: 3":
            frames[i]=frame[i]
    frames["Subject"]=frames["Unnamed: 3"]
    del frames["Unnamed: 3"]

def imp(link,page,frames,status=False):
    #page1st(link,frames)
    with open(link+'.pdf', 'rb') as pdfFileObj:        
        pdfReader = PdfFileReader(pdfFileObj) 
        pages=pdfReader.getNumPages()
        result(link,page,2)
        return 
        if status==True:
            print("Scaned page Number: " , end="")
        for i in range(pages+1):                
            if status==True:
                print(i+1 , end=" ")
            result(link,page,i)
        if status==True:
            print(" .")

def getgrade(val):
    if( val>40):
        return "Pass"
    else:
        return "Fail"
    
    
    
def printdetail(detail,sdata):
    global edata
    edata=sdata
    counter=0
    print(len(detail["Code"]))
    return
    print(sdata["Name"]+"  //  "+sdata["Roll_no"])
    for j in range(len(detail["Code"])-1):
        print("("+detail["Code"][j]+")("+detail["Subject"][j]+")" , end=" ")
        Minor,Major,Total,Grade=sdata["Marks"][0][counter],sdata["Marks"][0][counter+1],0,""
        if counter<14:
            if Minor.isdigit()==True and Major.isdigit()==True:
                Total=int(Minor)+int(Major)
            elif Minor.isdigit()==True and Major.isdigit()==False:
                Total=int(Minor)
            elif Minor.isdigit()==False and Major.isdigit()==True:
                Total=int(Major)
            else:
                Total=-1
            Grade=getgrade(Total)
            print(f"{Minor}+{Major}={Total}({Grade})")
        counter+=2
        print("\r")
    print("("+detail["Code"][-1]+")("+detail["Subject"][-1]+")" , end=" ")
    print(f"{sdata['Marks'][-1]}({getgrade(int(sdata['Marks'][-1]))})")

def checker(link):
    try:
        flag=0
        with open(link+'.json',"r") as file:
            data = json.load(file)
        rno=input("Enter Your Roll Number:")
        if len(rno)!=11:
            raise Exception("Error : Enter 11 digit Number")
        for i in data[1]:
           if i["Roll_no"]==rno:
               printdetail(data[0], i)
               flag=1
               break
        if flag==0:
            raise Exception("Error: No Result Found")
    except Exception as error:
        print(error)
        
def main(link):
    page=[]
    frames={}
    
    if path.exists(link+'.json')==True:
        checker(link)
    else:
        imp(link,page,frames,status=True)
        return 
        Result=[frames,page]
        with open(link+'.json', "w") as x:
            x.write(json.dumps(Result, indent=1))
link="020_BCA_3rd Sem Regular_Final Declared Result_December 2018"
main(link)
    