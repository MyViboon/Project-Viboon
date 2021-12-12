from tkinter import *
from tkinter import ttk,messagebox
import csv
from datetime import datetime


GUI = Tk()
GUI.geometry('750x500')
GUI.title('โปรแกรมคำนวนค่าไฟฟ้า V1.0')
 
######################## MenuBar ###############################
menubar = Menu(GUI)
GUI.config(menu=menubar)

filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Expot to')

filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Edit',menu=filemenu)

filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Option',menu=filemenu)

def About():
    messagebox.showinfo('เพิ่มเติม','โปรแกรมนี้จัดทำขึ้นเพื่อใช้บันทึกงานเวลาเดินทาง\nจัดทำโดย By วิบูลย์')

filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=filemenu)
filemenu.add_command(label='About',command=About)


###########################################################################################

# Icon1 = PhotoImage(file='running.png')
# Icon2 = PhotoImage(file='notes.png')

Tap = ttk.Notebook(GUI)
T1 = Frame(Tap,background='#afe8a7')
T2 = Frame(Tap)
T3 = Frame(Tap)
Tap.pack(fill=BOTH, expand=1)

Tap.add(T1, text=f'{"ลงบันทึก": ^20s}')#,image=Icon1,compound='top')
Tap.add(T2, text=f'{"แสดงผล": ^20s}')#,image=Icon2,compound='top')
Tap.add(T3, text=f'{"ตารางแสดงผล": ^20s}')

#################################### *** TAB 1  *** #######################################
F1 = Frame(T1)
F1.pack()    

FONT1 = (None,17)
FONT2 = ('Angsana New',20)

days = {'Mon': 'จันทร์',
        'Tue': 'อังคาร',
        'Wed':'พุธ',
        'Thu':'พฤหัส',
        'Fri':'ศุกร์',
        'Sat':'เสาร์',
        'Sun':'อาทิตย์'}
#------------------------------------------------------------------------------------------

def tick():
    today = datetime.now().strftime('%a')
    dt = datetime.now()
    dt = dt.replace(year=dt.year+543)
    dt = dt.strftime("%d/%m/%Y  %H:%M:%S")
    dt = 'วัน' + days[today] + '-' + dt + 'น'
    lb_clock.config(text=dt)
    lb_clock.after(1000, tick)      #ให้เรียกฟังก์ชันตัวมันเองทุก 1 วินาที
 

lb_clock = ttk.Label(T1,font='times 11',background='#afe8a7')
lb_clock.place(x=390,y=20)

tick()

M_img = PhotoImage(file='FT.png').subsample(3)
BG1 = ttk.Label(T1,image=M_img,background='#afe8a7')
BG1.place(x=220,y=40)
#------------------------------------------------------------------------------------------

def Save(evevt=None):
    print('ทดสอบ')
    Before = E_Before.get()
    After = E_After.get()
    Month = E_Month.get()

    try:
        unit = int(Before) - int(After)
        
        if unit<=150:
            Ea = unit*3.2484   
            
        elif unit<=250:
            Ea = (150*3.2484) + (unit-150)*4.2218

        elif unit>=400:
            Ea = (150*3.2484) + (250*4.2218) + (unit-400)*4.4217

        Service = 38.22
        FT = unit*(-0.1532)
        Vat = (Ea + FT+ Service)*0.07
        total = Ea + FT + Service
        result = Ea + FT + Vat+ Service
        
        today = datetime.now().strftime('%a')
        stam = datetime.now()
        time = stam.now().strftime("%d/%m/%Y- %H:%M:%S")
        transictionid = stam.now().strftime("%Y%m%d%H%M%f")
        time = days[today] + '-'+ time 

        Mtext = '        ***----  บันทึกเดือน : {}  ----***'.format(Month)
        text0 = '\nจำนวนไฟฟ้า(:หน่วย) ----------- *   {:.2f} หน่วย'.format(unit)
        text1 = '\nค่าพลังงานไฟฟ้า -------- *   {:.2f} หน่วย'.format(Ea)
        text2 = '\nค่าบริการรายเดือน --------------*   {}บาท'.format(Service)
        text3 = '\nค่า FT (-0.1532)บาท/หน่วย ----*   {:.2f} บาท'.format(FT)
        text4 = '\nรวมเงินค่าไฟฟ้า ---------------*   {:.2f} บาท'.format(total)
        text5 = '\nภาษีมูลค่าเพิ่ม 7% -------------*   {:.2f} บาท'.format(Vat)
        text6 = '\nรวมเงินค่าไฟฟ้า สุทธิ ----------*   {:.2f} บาท'.format(result)

        text = Mtext + text0 + text1 + text2 + text3 + text4 + text5 + text6
        
        V_result.set(text)
        
        with open ('savecsv.csv','a',newline='',encoding='utf-8') as f:
            wy = csv.writer(f)
            data = [transictionid,time,Month,Before,After,unit,"{:.2f}".format(result)]
            wy.writerow(data)

    except:
        print('No data')
        messagebox.showwarning('ERROR','กรุณากรอกข้อมูลทุกช่อง')
    E_Before.set('')
    E_After.set('')
    E_Month.set('')

    Updatetable()

    E1.focus()
    GUI.bind('<Return>',Save)
#============================================================================

L = ttk.Label(T1,text='หน่วยไฟล่าสุด',font=FONT2,background='#afe8a7')
L.place(x=150,y=220)
E_Before = StringVar()
E1 = ttk.Entry(T1,textvariable=E_Before,font=FONT2)
E1.place(x=110,y=260) 

L = ttk.Label(T1,text='หน่วยไฟเดือนที่แล้ว',font=FONT2,background='#afe8a7')
L.place(x=340,y=220)
E_After = StringVar()
E2 = ttk.Entry(T1,textvariable=E_After,font=FONT2)
E2.place(x=320,y=260)

L = ttk.Label(T1,text='เลือกเดือนที่บันทึก',font=FONT2,background='#afe8a7')
L.place(x=180,y=320)
# E_Before = StringVar()
# E1 = ttk.Entry(T1,textvariable=E_Before,font=FONT2)
# E1.place(x=270,y=270)
E_Month = StringVar()
T1.option_add('*font','consolas 16')
E3 = ttk.Combobox(T1,textvariable=E_Month,value=["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน",
"พฤษภาคม ", "มิถุนายน", "กรกฎาคม", "สิงหาคม",
"กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"])
E3.place(x=335,y=320,width=160)

B_img = PhotoImage(file='save.png')
B1 = ttk.Button(T1,text='    บันทึกที่นี่',image=B_img,compound='left',command=Save)
B1.place(x=230,y=380,width=150)

###################################### TAP 2  ############################################
L = ttk.Label(T2,text='ใบแจ้งค่าไฟฟ้า',font=FONT2).pack(pady=20)
V_result = StringVar()
V_result.set('***** กรุณากรอกข้อมูลแล้วกดSAVE เพื่อแสดงผล *****')
VS = ttk.Label(T2, textvariable=V_result,font=FONT2,foreground='blue')
VS.pack(pady=10)

#=========================================================================================

###################################### TAP 3  ############################################

def read_csv():
    with open('savecsv.csv',newline='',encoding='utf-8') as f:
        fr = csv.reader(f)
        data = list(fr)
    return data
  
header = ['รหัส','วันที่','เดือน','ล่าสุด','ก่อน','จำนวนหน่วย','ค่าไฟสุทธิ(บาท)']
headerwidht = [130,160,80,80,80,80,80]

L = ttk.Label(T3,text='ตารางแสดงผลบันทึก',font=FONT2).pack(pady=20)
Etable = ttk.Treeview(T3,columns=header,show='headings',height=15)
Etable.pack()

for h in header:
    Etable.heading(h,text=h)
for h,w in zip(header,headerwidht):
    Etable.column(h,width=w)
#------------------------------------------------------------------------------------------
alltransition = {}

def UpdateCSV():
    with open('savecsv.csv','w',newline='',encoding='utf-8') as f:
        fw = csv.writer(f)
        data = list(alltransition.values())
        fw.writerows(data)    
   
def Delete(event=None):
    check = messagebox.askyesno('Conferm?','คุณต้องการลบข้อมูลใช่หรือไม่?')
    if check == True:
        select = Etable.selection()
        data = Etable.item(select)
        data = data['values']
        try:
            transitionid = data[0]
            del alltransition[str(transitionid)]

            UpdateCSV()
            Updatetable()
        except:
            #print('ไม่ได้เลือก')
            messagebox.showwarning('คำเตือน','คุณไม่ได้เลือกรายการ!!')
    else:
        pass

Dbutton = ttk.Button(T3,text='Delete',command=Delete)
Dbutton.place(x=500,y=50)   
Etable.bind('<Delete>',Delete)

def Updatetable():
    Etable.delete(*Etable.get_children())
    try:
        data = read_csv()
        for d in data:
            alltransition[d[0]] = d
            Etable.insert('',0,values=d)
    except:
        print('No data')
        pass

def EditTab():
    POPUP = Toplevel()
    POPUP.geometry('300x320')
    POPUP.title('เมนูแก้ไข')

#================================================================================
    def Edit():

        # print(transitionid)
        # print(alltransition)
        olddata = alltransition[str(transitionid)]
        print('ข้อมูลชุดเก่า :',olddata)
        V1 = E_Month
        V2 = int(E_Before.get()) 
        V3 = int(E_After.get())
        V4 = V2 - V3
        
        if V4<=150:
            Ea = V4*3.2484   
            
        elif V4<=250:
            Ea = (150*3.2484) + (V4-150)*4.2218

        elif V4>=400:
            Ea = (150*3.2484) + (250*4.2218) + (V4-400)*4.4217

        Service = 38.22
        FT = V4*(-0.1532)
        Vat = (Ea + FT+ Service)*0.07
        # total = Ea + FT + Service
        result = Ea + FT + Vat+ Service 

        newdata = [olddata[0],olddata[1],V1,V2,V3,V4,"{:.2f}".format(result)]
        alltransition[str(transitionid)] = newdata

        UpdateCSV()
        Updatetable()

    L = ttk.Label(POPUP,text='หน่วยไฟล่าสุด',font=FONT2)
    L.pack()
    E_Before = StringVar()
    E1 = ttk.Entry(POPUP,textvariable=E_Before,font=FONT2)
    E1.pack()

    L = ttk.Label(POPUP,text='หน่วยไฟเดือนที่แล้ว',font=FONT2)
    L.pack()
    E_After = StringVar()
    E2 = ttk.Entry(POPUP,textvariable=E_After,font=FONT2)
    E2.pack()

    L = ttk.Label(POPUP,text='เลือกเดือนที่บันทึก',font=FONT2)
    L.pack()
    E_Month = StringVar()
    POPUP.option_add('*font','consolas 14')
    E3 = ttk.Combobox(POPUP,textvariable=E_Month,value=["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน",
    "พฤษภาคม ", "มิถุนายน", "กรกฎาคม", "สิงหาคม",
    "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"])
    E3.pack()
#===========================================================================================
    B_img = PhotoImage(file='save.png')
    B2 = ttk.Button(POPUP,text='  บันทึกแก้ไข',image=B_img,compound='left',command=Edit)
    B2.pack(pady=10)

    select = Etable.selection()
    data = Etable.item(select)
    data = data['values']
    print(data)
    transitionid = data[0]

    E_Before.set(data[3])
    E_After.set(data[4])
    E_Month.set(data[2])
    
    
    POPUP.mainloop()

FONT3 = (None,9)
rigthclick = Menu(GUI,tearoff=0)
rigthclick.add_command(font=FONT3,label='Edit',command=EditTab)
rigthclick.add_command(font=FONT3,label='Delete',command=Delete)

# leftclick = False

# def left(event):
#     global leftclick
#     leftclick = True 

def menupopup(event):
    # if leftclick == True:
    rigthclick.post(event.x_root,event.y_root)
    #print(rigthclick.post(event.x_root,event.y_root))

# Etable.bind('<Button-1>',left)
Etable.bind('<Button-3>',menupopup)

#============================================================

Updatetable()

GUI.mainloop()