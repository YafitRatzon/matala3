#פונקציה לקריאת קובץ טקסט
#יש להזין את הנתיב שבו הטקסט נמצא עם שם הטקסט בסופו
def read_file():
    file_name = input('Enter the file path and name: ')
    Chat_file = open(file_name, 'r', encoding='utf-8')
    return Chat_file

Chat_file = read_file()
print(Chat_file.readlines())

Chat_file.seek(0,0)

#ייבוא ספריות שימושיות
import re
import json

#פונקציה אשר תעבור על ההודעות בקובץ הטקסט ותיצור מהן רשימה של מילונים
#נבנה מילון ריק שיסנן תחילה את השורות שמתחילות בתאריך ושעה
#נאתחל משתמש אי די שימספר את המשתמשים וייתן לכל אחד מהם מזהה ייחודי משלו
def Whatsapp_Chat (Chat_file):
        
    dictionary_for_ids = {}     #יצירת מילון שאליו נכניס את אי די של המשתתפים בשיחה
    id = 1
    list_for_people = list()         # יצירת רשימה של משתתפים בשיחה
    date_from_chat='(([0-9]{2}|[0-9])\.([0][1-9]|[1][0-2]|[0-9])\.[0-9]{4})'

    
     #לולאה שתעבור על קובץ השיחה ותאתר את שמות המשתמשים, תכניס למילון ותיתן לכל אחד אי די משלו
    for line in Chat_file:
         if ((line.find("נוצרה על ידי")==-1) and (line.find("שינה/תה")==-1) and (line.find("שינית")==-1) and (line.find("החליף/ה")==-1) and (line.find("עזב/ה")==-1) and (line.find("מוצפנות מקצה-לקצה")==-1) and (line.find("קישור ההזמנה")==-1)):
            if ((line.find("הוסיף/ה")==-1) ):
                if (re.search(date_from_chat, line)):
                    part1 = line.find('-')
                    part2 = line.find(':',part1)
                    together = line[part1+2:part2]
                    if not together in list_for_people:
                        list_for_people.append(together)
                        dictionary_for_ids[together]= id
                        id = id+1

    Chat_file.seek(0,0)

#יצרתי רשימה שלתוכה יכנסו ההודעות טקסט שמופיעות בשיחת הווטסאפ
    text_list = list()


    for line in Chat_file:
        line = line.rstrip()
        if ((line.find("נוצרה על ידי")==-1) and (line.find("שינה/תה")==-1) and (line.find("שינית")==-1) and (line.find("החליף/ה")==-1) and (line.find("עזב/ה")==-1) and (line.find("מוצפנות מקצה-לקצה")==-1) and (line.find("קישור ההזמנה")==-1)):
            if ((line.find("הוסיף/ה")==-1) ):
                if (re.search(date_from_chat, line)):
                    text_dic = {}
                    part1 = line.find('-')
                    text_dic['datetime']= line[:part1]
                    part2 = line.find(':',part1)
                    person = line[part1+2:part2]
                    text_dic['id'] = dictionary_for_ids[person]
                    text = line[part2+1 :]
                    text_dic['text'] = text
                    text_list.append(text_dic)   
                   #ההנחה שהטקסט האחרון שהקוד זוכר הוא השורה האחרונה שנכנסה למילון ובעצם בכניסה לתנאי אלס הוא יוסיף את השורה הבאה 
                            #שלא מתחילה בתאריך כלומר היא המשך המשפט של השורה מעליה                         
                else:
                    text = text + " " + line
                    text_dic['text'] = text 

#יצירת מילון מטה דאטה
    
    Chat_file.seek(0,0)
    MetaData = {}
    for line in Chat_file:
        line = line.rstrip()
        if (line.find("נוצרה על ידי")!=-1):
            group = line.find('הקבוצה')
            created = line.find('נוצרה', group)
            part1 = line.find('-')
            MetaData['creation_date']= line[:part1]
            MetaData['num_of_people_in_gruop']= id
            MetaData['creator'] = line[created+13:]  #החיתוך נעשה באמצעות ספירת התוים לאחר המילה יוצר באנגלית ועד הסוף 
            MetaData['chat_name']= line[group+8:created-2] #החיתוך נעשה באופן זהה לכתוב מעלה


#יצירת מילון שכולל את רשימת המילונים שירצנו בשלב 2 ואת המטה דאטה בשלב 3
    
    total_dictionary = {}    #יצירת מילון
    total_dictionary['messages'] = text_list  #הכנסת הרשימה של הודעות הטקסט למילון תחת השם הודעות
    total_dictionary['metadata'] = MetaData #כנל בנוגע למטה דאטה

#ייצוא לגיסון
#נכניס לתוך הפונקציה את המטה דאטה ואפשרות לקרוא את השפה העברית, את המילון הכולל    
    Fjson = MetaData['chat_name']+".txt"
    with open (Fjson, 'w' , encoding='utf-16le') as outfile:
        json.dump(total_dictionary, outfile, ensure_ascii=False)

#נפעיל את הפונקציה שתבצע את הנדרש        
Whatsapp_Chat(Chat_file)