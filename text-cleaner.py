from tkinter import *
import sqlite3
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk


#================================DATABASE CONNECTION==================================
##conn=sqlite3.connect('mydb')
##cur=conn.cursor()
##dbvals=cur.execute('''INSERT into mytable VALUES('th is58 68 85');''')
##conn.commit()
#=========**********************************************************************===================================





#=================================ROOT WINDOW CONFIGURATION=====================
root=Tk()
x=root.winfo_screenwidth()//2
y=root.winfo_screenheight()//2
width=800
height=450
root.geometry(f'{width}x{height}+{x-(width//2)}+{y-(height//2)}')
root.title("Text Automation")
root.resizable(False,False)
#================**************************************************************===========================





#================================LEFT FRAME FOR DATABASE OPERATIONS===========================================================
lframe=Frame(root,width=300,height=400,bd=4,relief='solid',bg="#3f3f9f")
lframe.place(x=5,y=5)



#================TOTAL KEYS AVAILABLE=========
##conn=sqlite3.connect('mydb')
##cur=conn.cursor()
##avail_keys=cur.execute('''SELECT * FROM mytable;''')
##count_keys_var=len(avail_keys.fetchall())
##conn.close()

#============================================LABEL====================================================
#++++++++++++++++^^^^LABEL^^^^+++++++++++

keysl=Label(lframe,text="AVAILABLE KEYS : ",font="Times 18",fg="white",bg="#9f5f9f",width=18,padx=5)
keysl.place(x=5,y=5)

#=======================================*****************************************==============================================



#===================================================LISTBOX WITH SCROLL BAR X AND Y==============================================
#+++++++++++++++++++++++++^^^^^^^^^^^^^LIST BOX^^^^^^++++++++++++++++++++++++

scrollbary=Scrollbar(lframe)                        # VERTICAL SCROLL BAR
scrollbarx=Scrollbar(lframe,orient=HORIZONTAL)      # HORIZONTAL SCROLL BAR
                                                    # LIST BOX
listbox=Listbox(lframe,selectmode=EXTENDED,width=29,font="Times 14",yscrollcommand=scrollbary.set,xscrollcommand=scrollbarx.set)

conn=sqlite3.connect('mydb')
cur=conn.cursor()
dbvals=cur.execute('''SELECT * FROM mytable;''')         # LISTBOX GETTING DATA FROM DATABASE
for vals in dbvals:
    listbox.insert(END,vals[0])
conn.close()
listbox.place(x=5,y=45)

scrollbary.config(command=listbox.yview)            #SCROLL BAR CONFIG++++++++++
scrollbarx.config(command=listbox.xview)
scrollbary.place(x=270,y=45,height=225)
scrollbarx.place(x=5,y=268,width=280)
#======================================****************************************************==============================================

keysl2=Label(lframe,text=listbox.size(),font="Times 16",fg="white",anchor=W,bg="#9f9f9f",width=4,pady=3)
keysl2.place(x=235,y=5)


#==============================BUTTON FUNCTIONS ==================================================================================

################
################
################    NO NEED NOW   ###########
#=============================REFRESH BUTTON FUNCTION====================================================
def refreshb_f():
    listbox.delete(0,END)
    
    #RIGHT FRAME LISTBOX REFRESH
    rframelistbox.delete(0,END)
    selected_logf_label['text']=rframelistbox.size()
    
    #***************
    conn=sqlite3.connect('mydb')
    cur=conn.cursor()
    dbvals=cur.execute('''SELECT * FROM mytable;''')
    # LISTBOX GETTING DATA FROM DATABASE
    for vals in dbvals:
        listbox.insert(END,vals[0])
    
    keysl2['text']=listbox.size()       #  keysl2 UPDATE AVAILABLE KEYS
    conn.close()
    addb['state']=NORMAL
    deleteb['state']=NORMAL
    updateb['state']=NORMAL
    selectb['state']=NORMAL
    open_file['state']=NORMAL
    open_file['text']="OPEN FILE"
    save_file['state']=DISABLED
    name_selected_logf_labelb['text']=""

    try:
        filename.close()
    except:
        return
#=====================*********END************==================================================
##############################################################################################


#=====================ADD BUTTON FUNCTION====================================================================
def addb_f():
    
    def addb_b_f():
        conn=sqlite3.connect('mydb')
        cur=conn.cursor()
        x=cur.execute('SELECT * FROM mytable;')
    
        try:  
            cur.execute(f"INSERT INTO mytable VALUES('{addbf_e.get().strip()}');")
            conn.commit()
            addb_f_templ=Label(addoperationw,text=f"ADDED : {addbf_e.get().strip()}",width=45,justify=LEFT,anchor=W)
            addb_f_templ.place(x=24,y=119)
            #AUTO REFRESH LISTBOX AFTER ADDING NEW KEY
            listbox.delete(0,END)
            dbvals=cur.execute('''SELECT * FROM mytable;''')         # LISTBOX GETTING DATA FROM DATABASE
            
            for vals in dbvals:
                listbox.insert(END,vals[0])
            conn.close()
        except Exception as e:
            messagebox.showinfo("warning","ALREADY EXISTS.!")          
        
    # BUTTON DISABLED FOR FURTHER OPENINGS
    addb['state']=DISABLED
    deleteb['state']=DISABLED
    updateb['state']=DISABLED
    selectb['state']=DISABLED
    
    # ADD OPERATION WINDOW CONFIGURATION
    addoperationw=Toplevel(root)
    addoperationw.title('ADD KEYS TO DATA')
    addoperationw.geometry(f'{width//2}x{height//2}+{width+(width//3)}+{height-(height//2)}')
    addoperationw.resizable(False,False)
    addoperationw.configure(bg="#7f5f7f")
    
    #WIDGETS
    addbf_l=Label(addoperationw,font="Times 20",text="ADD KEY",bd=3,relief="solid").place(x=25,y=5)
    addbf_l_a=Label(addoperationw,font="Times 14",text="ENTER KEY").place(x=25,y=80)
    addbf_e=Entry(addoperationw,font="Times 14",width=25,bd=3,relief="sunken")
    addbf_e.place(x=150,y=80)
    

    addbf_b=Button(addoperationw,text="SUBMIT",font="Times 16",width=15,bd=4,relief="raised",command=addb_b_f).place(x=25,y=150)
#=================************* END ********************************************************=================================


#==================DELETE BUTTON FUNCTION========================================================================================
def deleteb_f():
    def deletebf_b_f():
        
        deletebf_b_f_vals=dellistbox.curselection()
        if dellistbox.curselection() != () :                #VALIDATION IF 0 ITEM SELECTION
            conn=sqlite3.connect('mydb')
            cur=conn.cursor()
            deletebf_b_f_vals_i_count=0
            for deletebf_b_f_vals_i in deletebf_b_f_vals:
                cur.execute(f"DELETE FROM mytable WHERE name='{dellistbox.get(deletebf_b_f_vals_i)}';")
                
                conn.commit()
                deletebf_b_f_vals_i_count += 1
            messagebox.showinfo(f"SUCCESS!","SUCCESSFULLY DELETED names : %d"%deletebf_b_f_vals_i_count)

            # REFRESH DELLISTBOX AFTER SUCCESS FULLY DELETION
            dellistbox.delete(0,END)
            deletebf_b_f_vals_refresh=cur.execute('''SELECT * FROM mytable;''')         # LISTBOX GETTING DATA FROM DATABASE
            for delete_val_refresh in deletebf_b_f_vals_refresh:
                dellistbox.insert(END,delete_val_refresh[0])
            conn.close()
            
        else:                                           # VALIDATION IF 0 ITEM SELECTED FOR DELETE
            messagebox.showinfo("ALERT","PLEASE SELECT AT LEAST 1 NAME")
    addb['state']=DISABLED
    deleteb['state']=DISABLED
    updateb['state']=DISABLED
    selectb['state']=DISABLED
    
    # ADD OPERATION WINDOW CONFIGURATION
    delete_operationw=Toplevel(root)
    delete_operationw.title('DELETE KEYS FROM DATA')
    delete_operationw.geometry(f'{350}x{400}+{width+(width//3)}+{height-(height//2)}')
    delete_operationw.resizable(False,False)
    delete_operationw.configure(bg="#7f5f7f")
    
    #WIDGETS
    deletebf_l=Label(delete_operationw,font="Times 20 ",text="DELETE KEYS",bd=3,relief="solid").place(x=5,y=5)
    
    delscrollbarx=Scrollbar(delete_operationw,orient=HORIZONTAL)
    delscrollbary=Scrollbar(delete_operationw)
    dellistbox=Listbox(delete_operationw,width=30,font="Times 14",height=11,
                       selectmode=EXTENDED,xscrollcommand=delscrollbarx.set,
                       yscrollcommand=delscrollbary.set)
    #================================DATABASE CONNECTION==================================
    conn=sqlite3.connect('mydb')
    cur=conn.cursor()
    dbvals=cur.execute('''SELECT * FROM mytable;''')         # LISTBOX GETTING DATA FROM DATABASE
    for vals in dbvals:
        dellistbox.insert(END,vals[0])
    conn.close()
    dellistbox.place(x=5,y=50)
    delscrollbarx.config(command=dellistbox.xview)
    delscrollbary.config(command=dellistbox.yview)
    delscrollbarx.place(x=5,y=296,width=274)
    delscrollbary.place(x=279,y=50,height=263)
    

    deletebf_b=Button(delete_operationw,text="DELETE",font="Times 12 bold",width=15,bd=4,relief="raised",command=deletebf_b_f).place(x=5,y=340)    
#================*********************** END DELETE BUTTON FUNCTION*********************************==============================================

#=============================UPDATE BUTTON FUNCTION==============================================================
def updateb_f():
    def updatebf_b_f():
        updatebf_b_f_list=updatelistbox.get(0,END)
        print(updatebf_b_f_list)
        updatebf_b_f_var= updatebf_la_e.get().strip()
        if updatelistbox.curselection() != ():
            if updatebf_b_f_var != '' :
                if updatebf_b_f_var not in updatebf_b_f_list:
                    
                    conn=sqlite3.connect('mydb')
                    cur=conn.cursor()

                    dbvals=cur.execute(f"UPDATE mytable SET name = '{updatebf_b_f_var}' \
                    WHERE name = '{updatebf_b_f_list[updatelistbox.curselection()[0]]}';") 
                    conn.commit()
                    messagebox.showinfo("SUCCESS",f"SUCCESSFULLY UPDATED {updatebf_b_f_list[updatelistbox.curselection()[0]]} -> {updatebf_b_f_var}")

                    # REFRESH UPDATELISTBOX AFTER SUCCESSFULLY UPDATE
                    updatelistbox.delete(0,END)
                    updatebf_b_f_vals_refresh=cur.execute('''SELECT * FROM mytable;''')         # LISTBOX GETTING DATA FROM DATABASE
                    for update_val_refresh in updatebf_b_f_vals_refresh:
                        updatelistbox.insert(END,update_val_refresh[0])
                    conn.close()
                else:
                    messagebox.showinfo("ALERT","NAME ALREADY EXISTS IN THE DATABASE")
                    
            else:
                messagebox.showinfo("ALERT","PLEASE ENTER KEY IN THE TEXT FIELD")
        else:
            messagebox.showinfo("ALERT","PLEASE SELECT THE KEY.")
    addb['state']=DISABLED
    deleteb['state']=DISABLED
    updateb['state']=DISABLED
    selectb['state']=DISABLED
    
    # UPDATE OPERATION WINDOW CONFIGURATION
    update_operationw=Toplevel(root)
    update_operationw.title('UPDATE KEYS FROM DATA')
    update_operationw.geometry(f'{350}x{420}+{width+(width//3)}+{height-(height//2)}')
    update_operationw.resizable(False,False)
    update_operationw.configure(bg="#7f5f7f")

    #WIDGETS
    updatebf_l=Label(update_operationw,font="Times 20 ",text="UPDATE KEYS",bd=3,relief="solid").place(x=5,y=5)
    
    updatescrollbarx=Scrollbar(update_operationw,orient=HORIZONTAL)
    updatescrollbary=Scrollbar(update_operationw)
    updatelistbox=Listbox(update_operationw,width=30,font="Times 14",height=11,
                       selectmode=SINGLE,xscrollcommand=updatescrollbarx.set,
                       yscrollcommand=updatescrollbary.set)
    #================================DATABASE CONNECTION==================================
    conn=sqlite3.connect('mydb')
    cur=conn.cursor()
    dbvals=cur.execute('''SELECT * FROM mytable;''')         # LISTBOX GETTING DATA FROM DATABASE
    for vals in dbvals:
        updatelistbox.insert(END,vals[0])
    conn.close()
    updatelistbox.place(x=5,y=50)
    updatescrollbarx.config(command=updatelistbox.xview)
    updatescrollbary.config(command=updatelistbox.yview)
    updatescrollbarx.place(x=5,y=296,width=274)
    updatescrollbary.place(x=279,y=50,height=263)
    
    updatebf_la=Label(update_operationw,text="ENTER NAME : ",font="Times 12 bold").place(x=5,y=340)
    
    updatebf_la_e=Entry(update_operationw,font="Times 12 bold",width=23)
    updatebf_la_e.focus()
    updatebf_la_e.place(x=140,y=340)
    
    updatebf_b=Button(update_operationw,text="UPDATE",font="Times 12 bold",width=15,bd=4,relief="raised",command=updatebf_b_f).place(x=5,y=380)    
#==============*********************END UPDATE BUTTON FUNCTION******************************===================================


#=================SELECT BUTTON FUNCTION==================================================
def selectb_f():
    rframelistbox.delete(0,END)
    for listbox_indices in listbox.curselection():
        rframelistbox.insert(END,listbox.get(listbox_indices))
    selected_logf_label['text']=rframelistbox.size()
    
#============***********END SELECT BUTTON FUNCTION************======================
    
#================***************************************************************************=====================================

#===================================================BUTTONS===========================================================================
#+++++++++++^^^^^BUTTONS^^^^^+++++++++++++++
refreshb=Button(lframe,text="REFRESH",bd=2,relief="raised",font="Times 10",width=10,command=refreshb_f)#DONE
addb=Button(lframe,text="ADD KEY",bd=2,relief="raised",font="Times",width=13,command=addb_f)  #DONE
deleteb=Button(lframe,text="DELETE KEY",bd=2,relief="raised",font="Times",width=13,command=deleteb_f)   # DONE
updateb=Button(lframe,text="UPDATE KEY",bd=2,relief="raised",font="Times",width=13,command=updateb_f)   #DONE
selectb=Button(lframe,text="SELECT KEYS",bd=2,relief="raised",font="Times",width=13,command=selectb_f)    # DONE



refreshb.place(x=110,y=290)
addb.place(x=15,y=320)
deleteb.place(x=150,y=320)
updateb.place(x=15,y=355)
selectb.place(x=150,y=355)

#==============************************************************************************======================================


def open_file_f():
    if rframelistbox.size() == 0:
        messagebox.showinfo("ALERT","FIRST SELECT KEYS")
    else:
        global filename
        filename=filedialog.askopenfile(title="SELECT YOUR LOG FILE",filetypes=[("text file","*.txt")])
        if filename != None:
            open_file['state']=DISABLED
            save_file['state']=NORMAL
            
            name_selected_logf_labelb['text']=str(filename).split('/')[-1].split('.txt')[0]
            open_file['text']="OPENED FILE"
            #SAVE
            '''
            print("opened")
            for line in filename:
                if not any(x in line for x in rframelistbox.get(0,END)):
                    print(line)                   '''

   
def save_file_f():
    save_as_file=filedialog.asksaveasfilename(title="ENTER FILE NAME",defaultextension=".txt",filetypes=[("text files",".txt")])
    try:
        with open(save_as_file,"a+") as f:
                for line in filename:
                    if not any(x in line for x in rframelistbox.get(0,END)):
                        f.write(line)

        messagebox.showinfo("SUCCESS","YOUR FILE IS READY..!!!")
    except:
        messagebox.showinfo("ALERT","NO FILE CHOOSEN..!!")
        
#=============RIGHT FRAME FOR FILE SELECTION AND CREATION=====================================================================
rframe=Frame(root,width=480,height=400,bd=4,relief='solid',bg="#9f9f3f")
rframe.place(x=310,y=5)

logf_label=Label(rframe,text="SELECTED KEYS : ",font="Times 18",fg="white",bg="#9f5f9f",anchor=W,width=18,padx=5)
logf_label.place(x=5,y=5)

selected_logf_label=Label(rframe,text="0",font="Times 18",fg="white",bg="#9f2f9f",anchor=W,width=4,padx=5)
selected_logf_label.place(x=220,y=5)

name_selected_logf_labelb=Label(rframe,text="",font="Times 14",pady=5,bg="#9f9f3f")
name_selected_logf_labelb.place(x=140,y=300)

rframescrollbary=Scrollbar(rframe)                        # VERTICAL SCROLL BAR
rframescrollbarx=Scrollbar(rframe,orient=HORIZONTAL)      # HORIZONTAL SCROLL BAR
                                                    # LIST BOX
rframelistbox=Listbox(rframe,selectmode=EXTENDED,width=29,font="Times 14",yscrollcommand=rframescrollbary.set,
                      xscrollcommand=rframescrollbarx.set)

rframelistbox.place(x=5,y=45)

rframescrollbary.config(command=rframelistbox.yview)            #SCROLL BAR CONFIG++++++++++
rframescrollbarx.config(command=rframelistbox.xview)
rframescrollbary.place(x=270,y=45,height=225)
rframescrollbarx.place(x=5,y=268,width=280)

open_file=Button(rframe,text="OPEN FILE",font="Times 14",command=open_file_f)
open_file.place(x=5,y=300)

save_file=Button(rframe,text="SAVE FILE",font="Times 14",command=save_file_f,state=DISABLED)
save_file.place(x=5,y=350)



#select_dir=Button(rframe,text="OUPUT DIRECTORY",font="Times 12",command=None)
#select_dir.place(x=300,y=5)

#output_name=Button(rframe,text="OUTPUT NAME",font="Times 12",command=None,width=15)
#output_name.place(x=300,y=50)























#=============**************************************************************************==========================================




root.mainloop()
