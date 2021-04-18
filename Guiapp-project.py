#creating a GUI application with the objective of drawing a chart on screen

import tkinter
from tkinter import messagebox,filedialog
from tkmagicgrid import *
import csv
import matplotlib
from tkinter.ttk import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import rcParams
from tkscrolledframe import ScrolledFrame
import mysql.connector
from tkinter import ttk
matplotlib.use("TkAgg")
window = tkinter.Tk()
window.title("A GUI for Drawing Charts in Python")
window.configure(background='yellow')
global var1
global val1
var1=[]
val1=[]
global newflag
newflag=0
rcParams.update({'figure.autolayout': True})
############function for Data Menu##############
def functionCreateData():
    #we will first connect to database
    global newflag
    newflag=1
    functionLoadDatafromdb()
    #pass
def functionLoadData():
    for widget in window.winfo_children():
        if isinstance(widget, tkinter.Frame):
           widget.destroy()
    
    window.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select your datafile",filetypes = (("csv files","*.csv"),("all files","*.*")))
    with open(window.filename, newline = "") as file:
        reader = csv.reader(file)
        
        # r and c tell us where to grid the labels
        r = 0
        parsed_rows = 0
        sf = ScrolledFrame(window, width=100, height=300)
        sf.pack(side="left",expand=0)
        sf.bind_arrow_keys(window)
        sf.bind_scroll_wheel(window)
        inner_frame = sf.display_widget(Frame)
        grid = MagicGrid(inner_frame)
        #grid.pack(side="top", expand=1, fill="both")
        grid.grid(row=0,column=0)
        global var1
        global val1
        global axisnames
        var1=[]
        val1=[]
        axisnames=[]
        for row in reader:
            #print(row[0],row[1])
            if parsed_rows == 0:
                axisnames=row
                # Display the first row as a header
                if row==['Variable','Value']:
                    chart_menu.entryconfigure('Line', state='active')
                    chart_menu.entryconfigure('Bar', state='active')
                    chart_menu.entryconfigure('Pie', state='active')
                    chart_menu.entryconfigure('Histogram', state='active')
                else:
                    chart_menu.entryconfigure('ScatterPlot', state='active')
                    chart_menu.entryconfigure('Line', state='active')
                    chart_menu.entryconfigure('Bar', state='active')
                    chart_menu.entryconfigure('Pie', state='active')
                    chart_menu.entryconfigure('Histogram', state='active')
                    
                    
                #columncount=len
                
                grid.add_header(*row)
            else:
                grid.add_row(*row)
                var1.append(row[0])
                val1.append(int(row[1]))
            parsed_rows += 1
        #print("varibales are:",var1)
        #print("values are:",val1)
            
def functionLoadDatafromdb():
    

    for widget in window.winfo_children():
        if isinstance(widget, tkinter.Frame):
           widget.destroy()
    databaseframe=tkinter.Frame(window)
    label_user=tkinter.Label(databaseframe,text="DB User: ",anchor=tkinter.W,background="dark slate gray",foreground="white",font=("Times", 12))
    label_password=tkinter.Label(databaseframe,text="DB Password:", anchor=tkinter.W,background="dark slate gray",foreground="white",font=("Times", 12)) 
    label_user.grid(row=0,column=0,sticky=tkinter.E+tkinter.W)
    label_password.grid(row=1,column=0, sticky=tkinter.E+tkinter.W)
    dbuser=tkinter.Entry(databaseframe)
    dbpassword=tkinter.Entry(databaseframe,show="*")
    dbuser.grid(row=0,column=1,sticky=tkinter.E+tkinter.W)
    dbpassword.grid(row=1,column=1,sticky=tkinter.E+tkinter.W)
    connectb=tkinter.Button(databaseframe,text="Log in",font=("Times", 12),command=lambda:dbconnexion(dbuser.get(),dbpassword.get()))
    cancelb=tkinter.Button(databaseframe,text="Cancel",command=databaseframe.destroy,font=("Times", 12))
    connectb.grid(row=2,column=1,sticky=tkinter.W)
    cancelb.grid(row=2,column=2)
    databaseframe.pack()
       
    #print(citys)#pass                 
  

def dbconnexion(uname,pwd):
    #uname=dbuser.get()
    print(uname)
    print(pwd)
    #print(pframe)
    try:
       con= mysql.connector.connect(user=uname, password=pwd,host='127.0.0.1')       
       c = con.cursor()
       dbs=[]
       c.execute("""SHOW databases""")
       for row in c:
           eachdb =row[0]
           #print(city)
           dbs.append(eachdb)
       c.close()
       print(dbs)
       messagebox.showinfo("Mysql connection Status", "succesfully conected as root!")
       global succuname
       global succpassword
       succuname = uname
       succpassword = pwd
       # we will now display the database names for user wwould choose to workon
       #databaseframe.destroy
       for widget in window.winfo_children():
           if isinstance(widget, tkinter.Frame):
               widget.destroy()
           #widget.destroy()
           #print(widget)
       avdatabases=tkinter.Frame(window)       
       tkinter.Label(avdatabases,text="Following are the Availible databases in the system.Choose the database you want to work with",justify = tkinter.LEFT,padx = 20).pack()
       rbcount=1
       gr = tkinter.StringVar()
       gr.set("L")
       for i in dbs:
           if(newflag==1):
              tkinter.Radiobutton(avdatabases,text=i,padx = 20,variable=gr,value=i,command=lambda:createtables(gr.get())).pack(anchor=tkinter.W)
           else:
               tkinter.Radiobutton(avdatabases,text=i,padx = 20,variable=gr,value=i,command=lambda:gettables(gr.get())).pack(anchor=tkinter.W)
           rbcount +=1
       if (newflag==1):
           tkinter.Radiobutton(avdatabases,text="New Database",padx = 20,variable=gr,value="Create a New Database",command=lambda:createtables(gr.get())).pack(anchor=tkinter.W)
       avdatabases.pack()
    except mysql.connector.errors.ProgrammingError:
        # Loop over the login interface if not
        print("INcorrect username")
        messagebox.showinfo("Mysql connection Status", "Wrong Username/password-Retry!")
        #window.destroy
        
def createtables(database):
    #create the database/tables and fields
    #print(database)
    global buttoncount
    global newflag
    #if(database !="New Database"):
       #newflag=0
    buttoncount=0
    global fieldvalues
    global fieldtypes
    fieldvalues=[]
    fieldtypes=[]
    for widget in window.winfo_children():
        if isinstance(widget, tkinter.Frame):
           widget.destroy()
    t_text="Create the Schema of your new database & Table to enter data to"   
    newdataentry=tkinter.Frame(window)
    tkinter.Label(newdataentry,text=t_text,justify = tkinter.LEFT,padx = 20).grid(row=0,column=0,columnspan=2)
    label_database=tkinter.Label(newdataentry,text="Database Name:",anchor=tkinter.W,background="dark slate gray",foreground="white", font=("Times", 12))
    label_table=tkinter.Label(newdataentry,text="Table Name:", anchor=tkinter.W,background="dark slate gray",foreground="white", font=("Times", 12))
    label_database.grid(row=1,column=0,sticky=tkinter.E+tkinter.W)
    label_table.grid(row=2,column=0, sticky=tkinter.E+tkinter.W)
    dbname=tkinter.Entry(newdataentry)
    tablename=tkinter.Entry(newdataentry)
    dbname.grid(row=1,column=1,sticky=tkinter.E+tkinter.W)
    tablename.grid(row=2,column=1,sticky=tkinter.E+tkinter.W)
    connectb=tkinter.Button(newdataentry,text="Create Table Fields",font=("Times", 12),command=lambda:addfields(dbname.get(),tablename.get()))
    connectb.grid(row=3,column=0,columnspan=2)
    newdataentry.pack()
     
              
def addfields(a,b):
    global buttoncount
    #global fieldvalues
    #global fieldtypes
    if ((a!="")&(b!="")):
        print("got dabase name: {} and table name: {}".format(a,b))
        #we will now go on adding the fileds names and field types
        newfieldentry=tkinter.Frame(window)
        label_fieldname=tkinter.Label(newfieldentry,text="Field Name:", anchor=tkinter.W,background="dark slate gray",foreground="white",font=("Times", 12))
        fieldname=tkinter.Entry(newfieldentry)
        fieldtype=ttk.Combobox(newfieldentry,values=['BINARY','CHAR','VARBINARY','VARCHAR(255)','TINYBLOB','TINYTEXT','BLOB','TEXT','MEDIUMBLOB','MEDIUMTEXT','LONGBLOB','LONGTEXT','TINYINT','SMALLINT','MEDIUMINT','INT','BIGINT','FLOAT'])
        label_fieldtype=tkinter.Label(newfieldentry,text="Choose Field Type:", anchor=tkinter.W,background="dark slate gray",foreground="white", font=("Times", 12))
        button_fieldupdate=tkinter.Button(newfieldentry,text="update",font=("Times", 12),command=lambda:updatefield(fieldname.get(),fieldtype.get()))
        label_fieldname.grid(row=4,column=0)
        fieldname.grid(row=4,column=1)
        label_fieldtype.grid(row=4,column=2)
        fieldtype.grid(row=4,column=3)
        button_fieldupdate.grid(row=4,column=4)
        
        if(buttoncount==0):
           tkinter.Button(newfieldentry,text="Create the Schema",font=("Times", 12),name="createnewdb",command=lambda:updateschema(a,b)).grid(row=3,column=2,columnspan=2)
        buttoncount=buttoncount+1
        #connectb.grid(row=5,column=0,columnspan=4)        
        #fieldname.pack()
        #fieldtype.pack()
        newfieldentry.pack()
        print(buttoncount)
    else:
        print("got dabase name: {} and table name: {}".format(a,b))
        messagebox.showinfo("Database Creation Validation:", "Database Name and/or Table Name can not be blank.Pl enter a valid name")
        
def updatefield(n,t):
    global fieldvalues
    global fieldtypes
    #print(n)
    #print(t)
    if((n!="") & (t != "")):
       fieldvalues.append(n)
       fieldtypes.append(t)
       print(fieldvalues)
       print (fieldtypes)
    else:
        messagebox.showinfo("Field type validation:", "Field type and name can not be blank")
        
        
def updateschema(a,b):
    global succuname
    global succpassword
    global recordcount
    global newflag
    print("new database creation:{}".format(newflag))
    recordcount=0
    con= mysql.connector.connect(user=succuname, password=succpassword,host='127.0.0.1')
    c = con.cursor()
    if(newflag==1):
       querystring = "drop database if exists {}".format(a)
       c.execute(querystring)
       querystring = "create database {}".format(a)
       c.execute(querystring)
    querystring = "use {}".format(a)
    c.execute(querystring)
    print("user: {} passwrd: {}".format(succuname,succpassword))
    querystring="create table {} (".format(b)
    for f in range(len(fieldvalues)):
        print("f: {} and length is :{}".format(f,len(fieldvalues)))
        if (f==len(fieldvalues)-1):
           querystring=querystring+"{} {}".format(fieldvalues[f],fieldtypes[f])
        else:
           querystring=querystring+"{} {},".format(fieldvalues[f],fieldtypes[f])
    querystring=querystring+")"
    print(querystring)
    c.execute(querystring)
    c.close
    messagebox.showinfo("{} Table under {} database\n- Sucessfully Created \n with {} fields".format(b,a,len(fieldvalues)), "Pl Poceed with data entry")
    for widget in window.winfo_children():
        if isinstance(widget, tkinter.Frame):
           widget.destroy()
    # we will now create a few entry fields for updation of data
    newfieldentry=tkinter.Frame(window)
    mlbl=tkinter.Label(newfieldentry,text="{} Table Dta entry wizard".format(a))
    entries=[]
    for f in range(len(fieldvalues)):
        lbl=tkinter.Label(newfieldentry,text="{}".format(fieldvalues[f]), anchor=tkinter.W,background="dark slate gray",foreground="white", font=("Times", 12)).grid(row=f,column=0)
        ent=tkinter.Entry(newfieldentry)
        entries.append(ent)        
        ent.grid(row=f,column=1)        
        #newfieldentry.pack()
    button_recordcount=tkinter.Button(newfieldentry,text="Total Records apended:{}.\n Click to go Charting".format(recordcount),font=("Times", 12))
    button_recordcount.grid(row=len(fieldvalues),column=0,columnspan=2,rowspan=2)
    button_fieldupdate=tkinter.Button(newfieldentry,text="updatedata",font=("Times", 12),command=lambda:appendtable(a,b,entries,fieldvalues,button_recordcount,newfieldentry,fieldtypes))
    
    button_fieldupdate.grid(row=0,column=2,rowspan=len(fieldvalues),columnspan=2)
    
    newfieldentry.pack()
    
def appendtable(d,t,e,f,bt,nf,qf):
    global recordcount
    global succname
    global succpasswod
    print("d:{}-t:{}-e:{}-f:{}".format(d,t,e,f))
    print(qf)

    con= mysql.connector.connect(user=succuname, password=succpassword,host='127.0.0.1')
    c = con.cursor()
    querystring = "use {}".format(d)
    c.execute(querystring)
    #print("user: {} passwrd: {}".format(succuname,succpassword))
    querystring="insert into {} (".format(t)
    #datapos=0
    for r in range(len(f)):
        querystring=querystring+"{},".format(f[r])
    querystring=querystring[:-1]+") values ("
    #string[:-1]
    datapos=0
    for k in e:
        #print(k.get())
        if (qf[datapos]=="VARCHAR(255)"):
           querystring=querystring+"'{}',".format(k.get())
        elif (qf[datapos]=="INT"):
           querystring=querystring+"{},".format(int(k.get()))
        elif (qf[datapos]=="FLOAT"):
            querystring=querystring+"{},".format(float(k.get()))
    datapos+=1   
    querystring=querystring[:-1]+")"
    print(querystring)
    c.execute(querystring)
    con.commit()
    c.close
    recordcount +=1
    print("recordcount:{}".format(recordcount))    
    bt.configure(text="Total Records apended:{}.\n Click to go Charting".format(recordcount),font=("Times", 12),command=lambda:cleanup())
    nf.pack()
   
    
def cleanup():
    messagebox.showinfo("Data uploaded Successfully", "Use chart menu to draw the chart ")
    for widget in window.winfo_children():
        if isinstance(widget, tkinter.Frame):
           widget.destroy()
    



def gettables(database):
    #connect to database and get 5 records each of existing tables
    #database=str(database)
    print(database)
    con= mysql.connector.connect(user=succuname, password=succpassword,db=database,host='127.0.0.1')
    c = con.cursor()
    tbls=[]
    #"insert into mytable values (%s, %s)"
    querystring = "SHOW tables"
    c.execute(querystring)
    print(c)    
    for widget in window.winfo_children():
        if isinstance(widget, tkinter.Frame):
           widget.destroy()
    #we will create a frame for displaying the tables and the scchema
    t_text="Following are the Availible tables in {} Database we selected '\n' Please select the table and fields for Plotting Charts".format(database)   
    avtables=tkinter.Frame(window)
    tkinter.Label(avtables,text=t_text,justify = tkinter.LEFT,padx = 20).pack()
    avtables.pack()
    gr = tkinter.StringVar()
    gr.set("L")
    for row in c:
        eachtbl =row[0]
        tkinter.Radiobutton(avtables,text=eachtbl,padx = 20,variable=gr,value=eachtbl,command=lambda:getfields(gr.get(),database)).pack(side=tkinter.LEFT)
        #print(city)
        tbls.append(eachtbl)
    #querystring="use %s"
    #c.execute(querystring,(database,))
    avtables.pack()
    c.close()









def getfields(tablename,database):
    print("table name is:",tablename ,"of:",database)
    con= mysql.connector.connect(user=succuname, password=succpassword,db=database,host='127.0.0.1')
    c = con.cursor()
    querystring = "describe {}".format(tablename)
    c.execute(querystring)
    tablefields=[]
    gr1 = tkinter.StringVar()
    gr1.set("L")
    gr2 = tkinter.StringVar()
    gr2.set("M")
    # we will check if previous frames are existing in case they are present we will destroy them and recreate the fames for choosing x and y axis
    #for widget in window.winfo_children():
        #widget.destroy()
        #print (str(widget))   
        
    avfieldsxaxis=tkinter.Frame(window,name="xaxis")
    tkinter.Label(avfieldsxaxis,text="Choose Field for X-axis",justify = tkinter.LEFT,padx = 20).pack()    
    avfieldsxaxis.pack(side=tkinter.LEFT)
    avfieldsyaxis=tkinter.Frame(window,name="yaxis")
    tkinter.Label(avfieldsyaxis,text="Choose Field for Y-axis",justify = tkinter.LEFT,padx = 20).pack()
    avfieldsyaxis.pack(side=tkinter.RIGHT)
    for row in c:
        eachfield=row[0]
        tablefields.append(eachfield)
        #so we now know the field names of the tables contained in the selected database
        # we will now destroy the database selection radio button and in this place we will create the table selection radio button
        # we will now show the schema of the tables to users and let use select the table for plotting
        tkinter.Radiobutton(avfieldsxaxis,text=eachfield,padx = 20,variable=gr1,value=eachfield).pack(anchor=tkinter.W)
        tkinter.Radiobutton(avfieldsyaxis,text=eachfield,padx = 20,variable=gr2,value=eachfield,command=lambda:getdata(gr1.get(),gr2.get(),tablename,database)).pack(anchor=tkinter.W)
    print(tablefields)        
    c.close()
    avfieldsxaxis.pack()
    avfieldsyaxis.pack()
  
def getdata(a,b,tablename,database):
    xaxis=a
    yaxis=b
    print(" i m inside getdata: i see xaxis as:",xaxis," and y axis as:",yaxis)
    con= mysql.connector.connect(user=succuname, password=succpassword,db=database,host='127.0.0.1')
    c = con.cursor()
    querystring = "Select {} , {} from {}  order by {}  desc limit 50".format(xaxis,yaxis,tablename,yaxis)
    print(querystring)
    c.execute(querystring)
    global var1
    global val1
    global axisnames
    var1=[]
    val1=[]
    axisnames=[a,b]
    for row in c:
        #print ("Name:",row[0],"Population:",row[1])
        var1.append(row[0])
        val1.append(int(row[1]))
    c.close
    print (val1)
    print(var1)
    #functionCreateBarChart()
    chart_menu.entryconfigure('Line', state='active')
    chart_menu.entryconfigure('Bar', state='active')
    chart_menu.entryconfigure('Pie', state='active')
    

#######################functions for Chart type Menu###########

def functionCreateLineChart():
    #pass
    global val1
    global var1
    figure = Figure(figsize=(8, 8), dpi=100)
    plot = figure.add_subplot(111)
    #plot.plot(0.5, 0.3, color="red", marker="o", linestyle="")    
    #x = [ 0.1, 0.2, 0.3 ]
    #y = [ -0.1, -0.2, -0.3 ]
    print(axisnames)
    #print("values are:",val1)
    x = var1
    y = val1
    print (x)
    print (y)
    plot.plot(x, y, color="blue", marker=".")
    plot.set_title('Line Chart showing  {} vs {} \nFor More than 50 records the graph is trimmed to top50'.format(axisnames[1],axisnames[0]))
    plot.set_xlabel(axisnames[0])
    plot.set_ylabel(axisnames[1])
    for tick in plot.get_xticklabels():
        tick.set_rotation(90)
    #plot.bar(x, y)
    graphholder = tkinter.Frame(window,highlightbackground="blue", highlightcolor="blue",bd= 0,name="chart")
    graphholder.pack(side='right',expand=True)
    canvas = FigureCanvasTkAgg(figure,graphholder)
    #canvas.get_tk_widget().grid(row=0,column=0)
    #canvas.get_tk_widget()
    canvas.draw()
    canvas._tkcanvas.pack(fill='both',expand=True)
    

def functionCreateBarChart():
    #pass
    global var1
    global val1
    figure = Figure(figsize=(8, 8), dpi=100)
    plot = figure.add_subplot(111)
    x = var1
    print(x)
    y = val1
    print(y)
    #plot.plot(x, y, color="blue", marker="x", linestyle="")
    plot.bar(x, y)
    plot.set_title('BarChart showing  {} vs {} \nFor More than 50 records the graph is trimmed to top50'.format(axisnames[1],axisnames[0]))
    plot.set_xlabel(axisnames[0])
    plot.set_ylabel(axisnames[1])
    for tick in plot.get_xticklabels():
        tick.set_rotation(90)
    #plot.tight_layout()    
    graphholder = tkinter.Frame(window,highlightbackground="blue", highlightcolor="blue",bd= 0,name="chart")
    graphholder.pack(side='right',expand=True)
    canvas = FigureCanvasTkAgg(figure,graphholder)
    #canvas.get_tk_widget().grid(row=0,column=0)
    #canvas.get_tk_widget()
    canvas.draw()
    canvas._tkcanvas.pack(fill='both',expand=True)
    
    pass
def functionCreatePieChart():
    global var1
    global val1
    figure = Figure(figsize=(8, 8), dpi=100)
    plot = figure.add_subplot(111)
    x = var1
    print(x)
    y = val1
    print(y)
    #plot.plot(x, y, color="blue", marker="x", linestyle="")
    plot.pie(y,labels=x,startangle=90,shadow= True,autopct='%1.1f%%')
    plot.set_title('Pie showing  {} vs {} \nFor More than 50 records the graph is trimmed to top50'.format(axisnames[1],axisnames[0]))
    #plot.set_xlabel(axisnames[0])
    #plot.set_ylabel(axisnames[1])
    graphholder = tkinter.Frame(window,highlightbackground="blue", highlightcolor="blue",bd= 0,name="chart")
    graphholder.pack(side='right',expand=True)
    canvas = FigureCanvasTkAgg(figure,graphholder)
    #canvas.get_tk_widget().grid(row=0,column=0)
    #canvas.get_tk_widget()
    canvas.draw()
    canvas._tkcanvas.pack(fill='both',expand=True)    
    pass
def functionCreateHistogram():
    #hist(x, 50, density=1, facecolor='g', alpha=0.75)
    figure = Figure(figsize=(5, 4), dpi=100)
    plot = figure.add_subplot(111)
    x = var1
    y = val1    
    #plot.plot(x, y, color="blue", marker="x", linestyle="")
    plot.hist(y,50, density=1, facecolor='g', alpha=0.75)
    graphholder = tkinter.Frame(window,highlightbackground="blue", highlightcolor="blue",  bd= 0)
    graphholder.pack(side='right',expand=True)
    canvas = FigureCanvasTkAgg(figure,graphholder)
    #canvas.get_tk_widget().grid(row=0,column=0)
    #canvas.get_tk_widget()
    canvas.draw()
    canvas._tkcanvas.pack(fill='both',expand=True)    
    pass
def functionCreateScatterPlot():
    pass
#################functions for help menu##################

def functionShowFaqs():
    pass
def functionShowCredits():
    messagebox.showinfo("Credit list", "Credits for who all helped!")
    # creating a question to get the response from the user [Yes or No Question]
    response = messagebox.askyesno("Support From", "Myself OR Allothers?")
       
    # If user clicks 'Yes' then it returns 1 else it returns 0
    if response == 1:
        #tkinter.Label(window, text = "Rishab and Shubham",relief = tkinter.RIDGE).grid(row=3,column=3)
        tkinter.Label(window, text = "Rishab and Shubham",relief = tkinter.RIDGE).pack(side="top",expand=0)
    else:        
        #tkinter.Label(window, text = "Who else but GOOGLE:)!!!",relief = tkinter.RIDGE).grid(row=3,column=3)
        tkinter.Label(window, text = "Who else but GOOGLE:)!!!",relief = tkinter.RIDGE).pack(side="top",expand=0)
    
                
    #pass
#################################################

#####creating the menus#######################


# creating a root menu to insert all the sub menus
root_menu = tkinter.Menu(window)
window.config(menu = root_menu)

# creating sub menus in the root menu
file_menu = tkinter.Menu(root_menu) # it intializes a new su menu in the root menu
root_menu.add_cascade(label = "Data", menu = file_menu) # it creates the name of the sub menu
file_menu.add_command(label = "Create-Table & Insert Data-(MYSQL) Database", command = functionCreateData) # it adds a option to the sub menu 'command' parameter is used to do some action
file_menu.add_command(label = "Load From File", command = functionLoadData)
file_menu.add_command(label = "Load From Database(MYSQL)", command = functionLoadDatafromdb)
file_menu.add_separator() # it adds a line after the 'Open files' option
file_menu.add_command(label = "Exit", command = window.quit)

# creating another sub menu
chart_menu = tkinter.Menu(root_menu)
root_menu.add_cascade(label = "Chart Types", menu = chart_menu)
chart_menu.add_command(label = "Line",state='disabled' ,command =functionCreateLineChart )
chart_menu.add_command(label = "Bar",state='disabled', command = functionCreateBarChart)
chart_menu.add_command(label = "Pie",state='disabled', command = functionCreatePieChart)
chart_menu.add_command(label = "Histogram",state='disabled', command = functionCreateHistogram)
chart_menu.add_command(label = "ScatterPlot",state='disabled', command = functionCreateScatterPlot)

# creting another sub menu for credits and help section
about_menu = tkinter.Menu(root_menu)
root_menu.add_cascade(label = "About", menu = about_menu)
about_menu.add_command(label="FAQS",command =functionShowFaqs)
about_menu.add_command(label="Credits",command =functionShowCredits)

######################executing over endless loop
window.mainloop()
