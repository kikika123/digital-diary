from mysql.connector import *
from tkinter import *
from tkinter.ttk import *
from random import *
from smtplib import *
from tkinter import filedialog
import pickle
from tkinter import messagebox
import os
from dotenv import load_dotenv

load_dotenv()

def generate_PID():
    mydb=connect(host="localhost",user="root",database="CS")
    mycursor=mydb.cursor()
    sql=mycursor.execute("select max(PID) from profile")
    p= mycursor.fetchone()
    if p is not None:
        PID=p[0]+1
    else:
        PID=1
    mydb.close()
    return PID
        
def createacc():
    global create
    global EMAIL
    global Email
    global NAME
    global PHNO
    global PSSWD
    global DOB
    global Username
    
    home.withdraw()
    create=Tk()
    create.geometry('600x400')
    create.title("Create an Account")
    email=Label(create,text="Enter Email")
    email.grid(row = 0, column = 0)
    Email=Text(create,height=1,width=25)
    Email.grid(row = 0, column = 1)
    b3=Button(create,text="Check",command=lambda:checkemail())
    b3.grid(row = 0, column = 2)
    name=Label(create,text="Name")
    name.grid(row = 1, column = 0)
    Name=Text(create,height=1,width=25)
    Name.grid(row = 1, column = 1)
    phno=Label(create,text="Phone Number")
    phno.grid(row = 2, column = 0)
    Phno=Text(create,height=1,width=25)
    Phno.grid(row = 2, column = 1)
    psswd=Label(create,text="Password")
    psswd.grid(row = 4, column = 0)
    Psswd=Text(create,height=1,width=25)
    Psswd.grid(row = 4, column = 1)
    dob=Label(create,text="Date of Birth(yyyy-mm-dd)")
    dob.grid(row = 5, column = 0)
    Dob=Text(create,height=1,width=25)
    Dob.grid(row = 5, column = 1)
    l=[Email,Name,Phno,Psswd,Dob]
    bu1=Button(create,text='submit',command=lambda:submit(l))
    bu1.grid(row=7, column= 2)
    b1=Button(create,text="send OTP",command=lambda:send_otp(Email,bu1))
    b1.grid(row = 0, column = 4)
    create.mainloop()
    
def send_otp(Email,bu1):
    global otp_wind
    
    otp_wind= Toplevel(create)
    otp_wind.geometry('200x200')
    flag = True
    #print(Email)
    smtpobj = SMTP('smtp.outlook.com', 587)
    r=randint(100000,999999)
    smtpobj.starttls()

    senderemail_id = os.environ.get("DD_SENDER_EMAIL")
    senderemail_id_password = os.environ.get("DD_SENDER_PASS")
    
    receiveremail_id= Email
    smtpobj.login(senderemail_id, senderemail_id_password)
    message = """From: From python program <{0}>
    To: To New User <{1}>
    MIME-Version: 1.0
    Content-type: text/html
    Subject: Account Confirmation

    your OTP for Registration is {2} 

    Enter the OTP and verify your account
    """.format(senderemail_id,receiveremail_id,r)
    try:
        smtpobj.sendmail(senderemail_id,receiveremail_id, message)
    except:
        flag = False
    smtpobj.quit()
    #if (flag):
    otp_wind.title('Verify OTP')
    otp_wind.geometry('200x200')
    m2=Label(otp_wind,text=" Mail send")
    m2.pack()
    otp= Entry(otp_wind,width=20)
    otp.pack()
    b1 = Button(otp_wind, text = "Verify", command= lambda:verify(r,otp,bu1))  
    b1.pack()
    
    otp_wind.mainloop()
'''#else:
        M1=Label(otp_wind,text="ERROR: Some error happened; Mail NOT send")
        M1.pack()'''
    

    
def verify(r,otp,bu1):
    o = int(otp.get())
    
    #if o == r:
    l3=Label(create,text='email id Verified') 
    l3.grid(row = 6, column = 1)
    bu1['state']='normal'
    otp_wind.destroy()
    '''else:
        l4=Label(otp_wind,text="Please Check your OTP again")
        l4.pack()'''  
               
def checkemail():
    email=str(Email.get("1.0", "end-1c"))
    ERR=Label(create,text="This email is already used. Try another email")
    OKAY=Label(create,text="Email check Successful. Proceed")
    mydb=connect(host="localhost",user="root",database="CS")
    mycursor=mydb.cursor()
    mycursor.execute("select* from profile")
    for i in mycursor:
        #print(i)
        if (i[2]==email):
            ERR.grid(row = 8, column = 1)
        else:
            OKAY.grid(row = 8, column = 1)        


    
def submit(l):
   
    EMAIL = l[0].get("1.0", "end-1c")
    NAME = l[1].get("1.0", "end-1c")
    PHONE = l[2].get("1.0", "end-1c")
    PSSWD = l[3].get("1.0", "end-1c")
    DOB = l[4].get("1.0", "end-1c")
    
    PID = generate_PID()
    #print(PID)
     
    mydb=connect(host="localhost",user="root",database="CS")
    mycursor=mydb.cursor()
    sql1="insert into profile(pid,Name,email,phone,dob)values({},'{}','{}','{}','{}');".format(PID,NAME,EMAIL,PHONE,DOB)
    sql2="insert into user(pid,password,Email)values({},'{}','{}');".format(PID,PSSWD,EMAIL)
    mycursor.execute(sql1)
    mycursor.execute(sql2)
    mydb.commit()
    mydb.close()
    messagebox.showinfo("User confrimation", "New User created Back to login window?")
    create.destroy()
    home.deiconify()

def login(p):
    global PID
    Email=p[0].get("1.0", "end-1c")
    Psswd=p[1].get("1.0", "end-1c")
    #print(Email)
    #print(Psswd)
    mydb=connect(host="localhost",user="root",database="CS")
    mycursor=mydb.cursor()
    sql = "select * from user where Email like '{}' and password like '{}';".format(Email,Psswd)
    mycursor.execute(sql)
    data = mycursor.fetchone()
    if any(data):
        PID = data[0]
        home.destroy()
        login_window()
    else:
        l=Label(home,text="Login failed").grid(row = 9, column = 2)
    mydb.close()
    
    
    
def openFile(clicked,txtarea,pathh):
    file = str(clicked.get())
    #print(file)
    txtarea.delete("1.0", "end-1c")
    pathh.delete("1.0", "end-1c")
    pathh.insert("end-1c", file)
    tf = open(file,'rb')
    file_cont = pickle.load(tf)
    #print(file_cont)
    txtarea.insert("end-1c", file_cont)
    tf.close()

def saveFile(txtarea,pathh):

    data = str(txtarea.get("1.0", "end-1c"))
    file = str(pathh.get("1.0", "end-1c"))
   
    f =  open(file,"wb")
    pickle.dump(data,f)
    f.close()
    
    

    mydb=connect(host="localhost",user="root",database="CS")
    mycursor=mydb.cursor()
    loc = str(PID)+'\\'+file
    sql = "select * from diary where did like '{}' and pid = {}".format(file,PID)
    mycursor.execute(sql)
    d = mycursor.fetchone()
    if d == None:
        sql = "insert into diary values ({},'{}','{}')".format(PID,file,loc)
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()
    
    

def login_window():
    mydb=connect(host="localhost",user="root",database="CS")
    mycursor=mydb.cursor()
    sql = "select * from profile where PID = {}".format(PID)
    mycursor.execute(sql)
    d = mycursor.fetchone()
    name = "Welcome " + d[1]
    
    ws = Tk()
    ws.title("!!!MY DIARY!!!")
    ws.geometry("700x500")
    ws['bg']='#B0E0E6'
    email=Label(ws,text=name)
    email.pack()
    # adding frame
    frame = Frame(ws)
    frame.pack(pady=20)

    # adding scrollbars
    ver_sb = Scrollbar(frame, orient=VERTICAL )
    ver_sb.pack(side=RIGHT, fill=BOTH)

    hor_sb = Scrollbar(frame, orient=HORIZONTAL)
    hor_sb.pack(side=BOTTOM, fill=BOTH)

    # adding writing space
    txtarea = Text(frame, width=70, height=20)
    txtarea.pack(side=LEFT)

    # binding scrollbar with text area
    txtarea.config(yscrollcommand=ver_sb.set)
    ver_sb.config(command=txtarea.yview)

    txtarea.config(xscrollcommand=hor_sb.set)
    hor_sb.config(command=txtarea.xview)

    # adding path showing box
    pathh = Text(ws, width=4, height=2)
    pathh.pack(expand=True, fill=X, padx=10)

    global options
    global clicked
    
    sql = "select * from diary where pid = {}".format(PID)
    mycursor.execute(sql)
    d = mycursor.fetchall()
    mydb.close()
    diarynames = []
    for i in d:
        diarynames.append(i[1])

    
    if diarynames != []:
        options = diarynames
        clicked = StringVar()
        clicked.set( diarynames[0] )

        # Create Dropdown menu
        drop = OptionMenu( ws , clicked , *options )
        drop.pack(side=LEFT, padx=10)

    # adding buttons
    b1 = Button( ws,text="Open File",command=lambda:openFile(clicked,txtarea,pathh))
    b1.pack(side=LEFT,padx=20)

    b2 = Button(ws,text="Save File",command=lambda:saveFile(txtarea,pathh))
    b2.pack(side=LEFT,padx=20)

    b3 = Button(ws,text="Exit",command=lambda:ws.destroy())
    b3.pack(side=LEFT,padx=20)
    b4 = Button(ws,text="Refresh Window",command=lambda:refresh_list(ws))
    b4.pack(side=LEFT,padx=20)
    b5 = Button(ws,text="Clear",command=lambda:clear(txtarea,pathh))
    b5.pack(side=LEFT,padx=20)
    
def clear(txtarea,pathh):
    txtarea.delete("1.0", "end-1c")
    pathh.delete("1.0", "end-1c")

    
def refresh_list(ws):
    ws.destroy()
    login_window()
    

def home(): 
    global home
    home= Tk()
    home.geometry('400x150')
    home.title("Digital Diary")
    email=Label(home,text="Enter Email") 
    Email=Text(home,height=1,width=30)
    passwd=Label(home,text="Password")
    Psswd=Text(home,height=1,width=30)
    p=[Email,Psswd]
    b1=Button(home,text="Login",command=lambda:login(p))
    b2=Button(home,text="Create Account",command=createacc)
    l=Label(home,text="WELCOME TO DIGITAL DIARY")
    
    l.grid(row = 0, column = 2)
    email.grid(row = 2, column = 1)
    Email.grid(row = 2, column = 2)
    passwd.grid(row = 3, column = 1)
    Psswd.grid(row = 3, column = 2)
    b1.grid(row = 8, column = 2)
    b2.grid(row = 8, column = 1)
    

    home.mainloop()
home()
