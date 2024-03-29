__version__="0.1.2"
# natHex_Gui
# python 3.10.12
import customtkinter


app = customtkinter.CTk() 
app.geometry("400x300")
app.title("natcats hex tool")


#Function that takes the dollar entry input to convert to bitcoin
def button_function():
    global label
    entryState = entry.get()
    e = entryState
    try:
        #First make sure to take out commas from bit numbers if there are any
        a = str(e)
        b = a.replace(',','')
        c = int(b)

        #Now continue hex conversion here
        conversion = (hex(c))
        print(conversion)
        #shows results. Need to show after convert somehow
        label.configure(text=f"Results: {conversion}")
    except:
        label.configure(text=f"Results: failed")



#creates a frame effect in background
frame1 = customtkinter.CTkFrame(master = app)
frame1.pack(pady=10, padx=15, expand=True) #master or placement is the "app" defined

#Bitcoin Label for the current interface showing
label1 = customtkinter.CTkLabel(master=frame1, justify=customtkinter.LEFT,text=f'''
    NatsCats Finder''')
label1.pack(pady=10, padx=10)
label = customtkinter.CTkLabel(master=frame1, text=" ")
label.pack(pady=10, padx=10)

#Entry box for the bit numbers
entry = customtkinter.CTkEntry(master=frame1, placeholder_text="Enter bit #")
entry.pack(padx=25, pady=10)

#used pack to keep button in place instead of using place which lets it move with window
button = customtkinter.CTkButton(master=frame1, text="Convert", command=button_function).pack(padx=25, pady=10)



app.mainloop()