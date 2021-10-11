#!/usr/bin/env python3
import os
import subprocess
import ast

#cmd ierakstīs un palaidīs vajadzīgās komandas, lai sakonektētos ar draiveri
def driverSendRead(location, command, number, fileName):
    args = [location+'/sdrv.exe', command, number, fileName]
    subprocess.call(args, shell=True)
    
#atvērs un ierastīs vajadzīgo tekstu failā. Paredzēts vairāk connection failam target
def fileWriting(fileName, yourTxt):
    f = open(fileName,"w")
    f.write('"'+yourTxt+'"')
    f.close()

#izveidos mapi ar visu gadu kontrollentām
def dataCollection():
    #sdrvPATH='C:/Users/user/Desktop/chd_agentH/sdrv'
    sdrvPATH=os.path.join('C:', os.sep, 'Users', 'user','Desktop','chd_agentH','sdrv')
    #pārbauda vai eksistē mape kurā tiks glabātas kontrollentas
    if not os.path.isdir(sdrvPATH +'/data'):
        os.makedirs(sdrvPATH +'/data')
    #pārbauda vai eksistē fails, kuru pados k.a. META ERROR
    '''
    if not os.path.isdir(sdrvPATH +'/target.txt'):
        os.makedirs(sdrvPATH+'/target.txt')
    '''
    #atver failu un ieraksta "", lai meklētu gadus
    fileWriting(sdrvPATH+'/target.txt','')
    #terminālī aisūta failu uz draiveri
    driverSendRead(sdrvPATH,'send', '212',sdrvPATH + '/target.txt' )
    driverSendRead(sdrvPATH,'read', '213',sdrvPATH + '/output.txt' )
    #mēģinājums noņemt ciparus no output faila
    '''
    with open(sdrvPATH + '/output.txt') as files:
        data = ''.join(i for i in files.read() if not i.isdigit())
    with open(sdrvPATH + '/output.txt',"w") as files:
        files.write(data)
    '''
    yearList=[]
    monthList=[]
    controllFileList=[]
    with open(sdrvPATH + '/output.txt') as files:
        for line in files:
            #noņem atstarpes no beigām un sākuma
            line = line.strip()
            #ja sastop tukšu rindu, tad turpina ciklu tālāk
            if not line:
                continue 
            x,y = ast.literal_eval(line)
            #x,y ir kā tuple lists
            #print(x,y)
            #sameklē mapi, kur nosaukums sākas ar year
            if x.startswith('Year'):
                yearList.append(x) 
                #ja nav, tad izveido mapi ar konkrēto gadu
                if not os.path.isdir(sdrvPATH +'/data/'+x):
                    os.makedirs(sdrvPATH +'/data/'+x)  
                #ieraksta failā gadu, lai aizietu uz kontrollentas failu
                fileWriting(sdrvPATH+'/target.txt',x)
                #terminālī aisūta failu uz draiveri
                driverSendRead(sdrvPATH,'send', '212',sdrvPATH + '/target.txt' )
                driverSendRead(sdrvPATH,'read', '213',sdrvPATH + '/output.txt' )
                with open(sdrvPATH + '/output.txt') as files1:
                    for line1 in files1:
                        #noņem atstarpes no beigām un sākuma
                        line1 = line1.strip() 
                        #ja ir tukša rinda, tad turpina tālāk ciklu
                        if not line1:
                            continue 
                        #veido koku ar iegūtiem string no vienas līnijas, sadalīts tikai pa divi, jo sākumā ir mape un tad seko 1 vai 0, kas ir otrs, bet šobrīd interesē tikai 1 string
                        s,m = ast.literal_eval(line1)
                        #ja pirmais string sākums būs Month, tad ies tālāk iekšā mapē
                        if s.startswith('Month'):
                            #pievieno listam nosaukumu, lai vieglāk kaut kad vēlāk atrast, bet var arī šo dzēst ārā
                            monthList.append(s) 
                            #ja nav, tad izveido mapi ar konkrēto mēnesi
                            if not os.path.isdir(sdrvPATH +'/data/'+x+'/'+s):
                                os.makedirs(sdrvPATH +'/data/'+x+'/'+s) 
                            #ieraksta failā mēnesi, lai aizietu uz kontrollentas failu
                            fileWriting(sdrvPATH+'/target.txt',x+'\\'+s)
                            #terminālī aisūta failu uz draiveri
                            driverSendRead(sdrvPATH,'send', '212',sdrvPATH + '/target.txt' )
                            driverSendRead(sdrvPATH,'read', '213',sdrvPATH + '/output.txt' )
                            
                            with open(sdrvPATH + '/output.txt') as files2:
                                for line2 in files2:
                                    #noņem atstarpes
                                    line2 = line2.strip()
                                    if not line2:
                                        continue 
                                    k,u = ast.literal_eval(line2)
                                    if k.endswith('txt'):
                                        controllFileList.append(k)
                                        #ieraksta failā faila nosaukumu, lai aizietu uz kontrollentas failu
                                        fileWriting(sdrvPATH+'/target.txt',x+'\\'+s+'\\'+k)
                                        #terminālī aisūta failu uz draiveri
                                        driverSendRead(sdrvPATH,'send', '212',sdrvPATH + '/target.txt' )
                                        #lai lasītu failu un atkodētu, vajadzēja visus 5 mainīgos, tāpēc netiek padots uz funkciju, jo funkcija pieņem tikai 4
                                        #driverSendRead(sdrvPATH,'read', '214',sdrvPATH +'/data/'+x+'/'+s +'/'+ k+' ', '/'+'FileType=RAW')
                                        args = [sdrvPATH +'/SDRV.exe', 'read', '214', sdrvPATH +'/data/'+x+'/'+s +'/'+ k+' ', '/'+'FileType=RAW']
                                       # print("this is args:",args)
                                        subprocess.call(args, shell=True)

def main():
    dataCollection()
if __name__ == "__main__":
    main()
