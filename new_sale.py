from customtkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image
from database import selectTable, insertIntoTable
#from CTkScrollableDropdown import *
import pandas as pd
#from CTkTable import CTkTable
from time import strftime
#from new_client import ClientMainViewFrame
import ttkbootstrap as ttb
#from autocomplete import AutoComplete
import sqlite3
from datetime import date
from printinvoice import printBill

"""medData = selectTable('MedicineList', column_names="MId, MName,  CurrentStock, MType, MRP,  GST, Weight")
medicineDf=pd.DataFrame(medData, columns=['MId', 'MName',  'CurrentStock', 'MType', 'MRP',  'GST', 'Weight'])
medSuggestionList = [med[1] for med in medData]"""


class MainViewFrame(ttk.Frame):
    def __init__(self, master=NONE):
        super().__init__(master,  width=1050, height=850, relief=tk.GROOVE)
        self.pack_propagate(0)
        self.grid(column=1, row=0, pady = (10,10), padx=(25,25))
        today = date.today().strftime("%Y-%m-%d")

        global medSuggestionList
        global medicineDf
        medData = selectTable('MedicineList', column_names="MId, MName,  CurrentStock, MType, MRP,  GST, Weight")
        medicineDf=pd.DataFrame(medData, columns=['MId', 'MName',  'CurrentStock', 'MType', 'MRP',  'GST', 'Weight'])
        medSuggestionList = [med[1] for med in medData]
       
        def clearBillTable():
            
            numRows = self.billTable.rows
            self.billTable.delete_rows(range(1,numRows))
            self.billTotalLabel.configure(text = "Bill Total: 0")

        
        # Title Section     
        padx_values = (35,35)
        gridPadding = 30
        self.titleFrame = ttk.Frame(master=self)
        self.titleFrame.pack(anchor="w", pady=(29, 0), padx=27)
        
        self.titleLabel = ttk.Label(master=self.titleFrame, text="New Bill", 
                                   font=("Calibri", 25, "bold"), style="success.TLabel" )
        self.titleLabel.grid(row=0, column=0, sticky="w", padx = padx_values)


        self.timeLabel = ttk.Label(master=self.titleFrame, font=("Calibri", 17, "bold"), style="success.TLabel" )
        self.timeLabel.grid(row=0, column=1, sticky="e",padx = (520,0))
        def get_time():
            string = strftime('%I:%M:%S %p')
            self.timeLabel.configure(text=string)
            self.timeLabel.after(1000, get_time)
        get_time()

        # Client Details Section
        self.clientGrid = ttk.Frame(master=self)
        self.clientGrid.pack(fill="both", padx=gridPadding, pady=(31, 0))
        
        self.clientUIDLabel = ttk.Label(master=self.clientGrid, text="Patient UID", 
                                        font=("Calibri", 15, "bold"), style="success.TLabel", 
                                        justify="left")
        self.clientUIDLabel.grid(row=0, column=0, sticky="w",padx = padx_values) 
        self.clientUIDEntry = ttk.Entry(master=self.clientGrid, 
                                        style="success.TEntry", 
                                        width=25
                                        
                                        )
        
        self.clientUIDEntry.grid(row=1, column=0, sticky='w', padx = padx_values)        
        

        def getCurrentDayPatients():

            condition = f"Date = '{today}'"
            Patients = selectTable('Patients', condition=condition )
            PatientNames = [pat[2] for pat in Patients]
            Patientdf=pd.DataFrame(Patients, columns=['UHId', 'Date', 'PName', 'PhoneNo', 'Age', 'Gender'])
            
            return Patientdf, PatientNames
        
        currentDayPatientNames = getCurrentDayPatients()[1]
        
        self.option_add("*TCombobox*Listbox*Font", ("calibri", 13, "bold"))
        self.clientNameLabel = ttk.Label(master=self.clientGrid, text="Patient Name", 
                                         
                                        font=("Calibri", 15, "bold"), style="success.TLabel", 
                                        justify="left")
        self.clientNameLabel.grid(row=0, column=1, sticky="w",padx = padx_values) 
        currentPatientName = tk.StringVar()
        self.clientNameEntry = ttk.Combobox(master=self.clientGrid, values=currentDayPatientNames,
                                            textvariable= currentPatientName,
                                          style='success.TCombobox',
                                          justify=LEFT, 
                                          font=("calibri", 12, "bold"), 
                                             cursor='hand2')

        def on_name_select(event):
            currentDayPatients = getCurrentDayPatients()[0]
            currentPatientPhone = currentDayPatients.loc[currentDayPatients["PName"] == currentPatientName.get()]["PhoneNo"].tolist()
            currentPatientGender = currentDayPatients.loc[currentDayPatients["PName"] == currentPatientName.get()]["Gender"].tolist()
            currentPatientUID = currentDayPatients.loc[currentDayPatients["PName"] == currentPatientName.get()]["UHId"].tolist()
            self.clientPhoneEntry.delete(0, END)
            self.clientGenderCbox.set("")
            self.clientUIDEntry.delete(0, END)
            self.clientPhoneEntry.insert(0, str(currentPatientPhone[0]))
            self.clientGenderCbox.set(currentPatientGender[0])
            self.clientUIDEntry.insert(0,currentPatientUID[0] )

        self.clientNameEntry.bind('<<ComboboxSelected>>', on_name_select)


        #self.clientNameEntry.bind("<KeyRelease>", autofillNames)

        self.clientNameEntry.grid(row=1, column=1, sticky='w', padx = padx_values)
        #self.clientNameEntry.bind("<KeyRelease>", getUID)
        
        self.clientPhoneLabel = ttk.Label(master=self.clientGrid, 
                                      text="Phone No:", font=("Calibri", 15, "bold"), 
                                      style="success.Tlabel", justify="left")
        self.clientPhoneLabel.grid(row=0, column=2, sticky="w",padx = padx_values) 
        self.clientPhoneEntry = ttk.Entry(master=self.clientGrid, 
                                         style="success.TEntry", width=25
                                         )
        
        self.clientPhoneEntry.grid(row=1, column=2, sticky='w', padx = padx_values)    

        

        self.clientGenderLabel  = ttk.Label(master=self.clientGrid,
                                           text = "Gender",font=("Calibri", 15, "bold"), 
                                      style="success.TLabel", justify="left" )
        self.clientGenderLabel.grid(row=0, column=3, sticky="w",padx = padx_values)
        self.clientGenderCbox = ttk.Combobox(master=self.clientGrid, style="success.TCombobox",
                                            values=("Male", "Female", "Other"), state='readonly', 
                                            justify=CENTER, font=("calibri", 12, "bold"), 
                                             cursor='hand2')
        self.clientGenderCbox.grid(row=1, column=3,sticky="w", padx = padx_values)

        self.radioSelect = StringVar()

        self.clientRadioButton = ttk.Checkbutton(master=self.clientGrid, text="Medicine Only",variable=self.radioSelect, style="success.TCheckbutton" )
        self.clientRadioButton.grid(row=2, column=1,sticky="w", padx = padx_values, pady=(15,0))
        

        
        # Search Section
        self.searchGrid = ttk.Frame(master=self, bootstyle="default")
        self.searchGrid.pack(fill="both", padx=gridPadding, pady=(31, 0))

        self.itemNameLabel = ttk.Label(master=self.searchGrid, 
                                      text="Item Name", font=("Calibri", 15, "bold"), 
                                      style="success.TLabel")
        self.itemNameLabel.grid(row=0, column=0, sticky="w", padx = padx_values)


        #Update Quantity Label on medicine option select
        def onMedNameSelect(event):
            global currentMedQty
            global currentMedPrice
            global currentMedType
            #global currentMedId

            currentMedName = self.itemNameEntry.get()
            #print(medicineDf.loc[medicineDf["MName"] == currentMedName])
            currentMedQty = int(medicineDf.loc[medicineDf["MName"] == currentMedName]["CurrentStock"].iloc[0])
            currentMedPrice = float(medicineDf.loc[medicineDf["MName"] == currentMedName]["MRP"].iloc[0])
            currentMedType = str(medicineDf.loc[medicineDf["MName"] == currentMedName]["MType"].iloc[0])
            
            
            self.qtyInStockLabel.configure(text="Quantity in Stock:"+ str(currentMedQty))  
        
        def autofillMeds(event):
            currChar = self.itemNameEntry.get()
            updatedList=[med for med in medSuggestionList if med.lower().startswith(currChar.lower())]
            self.itemNameEntry.configure(values=updatedList)


        style = ttk.Style()
        style.configure(
            "success.TButton",
            font=("Helvetica", 14),  # Set a larger font size
        )
        
        #style.configure("custom.TCombobox", font=("Helvetica", 18))

        self.itemNameEntry = ttk.Combobox(master=self.searchGrid, values=medSuggestionList,
                                          style='success.TCombobox',
                                          justify=LEFT, 
                                          font=("calibri", 12, "bold"), 
                                             cursor='hand2')
        self.itemNameEntry.grid(row=1, column=0, sticky='w', padx = padx_values)

        self.itemNameEntry.bind('<<ComboboxSelected>>', onMedNameSelect)
        self.itemNameEntry.bind("<KeyRelease>", autofillMeds)

                   
            


        

    
        
        def addToBill():
            #global currentMedQty 
            #global currentMedPrice
            #global currentMedType 
            global currentMedName
            global billTotal 
            
            
            currentMedName = self.itemNameEntry.get()
            currentSaleQty = self.qtySaleEntry.get()
            #currentMedQty,currentMedType,currentMedPrice = getMedDetails(currentMedName)

            
            totalSalePrice = int(currentSaleQty)*float(currentMedPrice)
            
            #numRows=self.billTable.rows
  
            self.billTable.insert("",END, values=[strftime("%d/%m/%Y, %H:%M:%S"),currentMedName, currentMedType, currentMedPrice, currentSaleQty, totalSalePrice])
            self.itemNameEntry.delete(0,len(currentMedName))
            self.qtySaleEntry.delete(0,len(currentSaleQty))
            #print("number of rows:",self.billTable.rows)
            if len(self.billTable.get_children()) ==  1: #If there is one entry in table
                billTotal = int(totalSalePrice)
            elif len(self.billTable.get_children()) > 1: #If there are multiple entries in table
                billTotal = int(billTotal)+int(totalSalePrice)
            self.billTotalLabel.configure(text= "Bill Total: " + str(billTotal))
            self.qtyInStockLabel.configure(text="Quantity in Stock:")
            
            #print("Bill Total:",billTotal)
        
        def clearBillTable():
            for record in self.billTable.get_children():
                self.billTable.delete(record)   
        
        

        self.addToBillButton = ttk.Button(master=self.searchGrid, text="Add to Bill", 
                                      style="success.TButton",# width=20, 
                                      command=addToBill)
        self.addToBillButton.grid(row=1, column=2, sticky='e', padx = padx_values)
        
        #self.addToBillButton.configure(style="Large.TButton")

        self.payModeLabel = ttk.Label(master=self.searchGrid, 
                                      text="Payment Mode", font=("Calibri", 15, "bold"), 
                                      style="success.TLabel")
        self.payModeLabel.grid(row=0, column=3, sticky="w", padx = padx_values)
        self.payModeCombobox = ttk.Combobox(master=self.searchGrid, values=["Cash", "UPI", "Both","Card"],
                                          style='success.TCombobox',
                                          justify=LEFT, 
                                          font=("calibri", 12, "bold"), 
                                             cursor='hand2')
        self.payModeCombobox.grid(row=1, column=3, sticky='w', padx = padx_values)
        
        """def activateBothEntries(event):
            if self.payModeCombobox.get() == 'Both':
                self.commentEntry.configure(state=NORMAL)
                
                self.commentEntry.insert(0,"Cash")
                self.upiAmtEntry.configure(state=NORMAL)
                self.upiAmtEntry.insert(0,"UPI")
        self.payModeCombobox.bind('<<ComboboxSelected>>', activateBothEntries )"""

        quantity_frame = ttk.Frame(master=self.searchGrid, bootstyle="default")
        quantity_frame.grid(row=1, column=1, padx=(15,15), pady=(0,0), sticky="w")

        def quantityIncrease():
            currentEntry = self.qtySaleEntry.get()
            #print("type is ", type(currentEntry))
            if currentEntry == "":
                currentEntry = 0
                self.qtySaleEntry.insert(0,1)
            else: currentEntry = int(self.qtySaleEntry.get())
            if currentEntry > 0 :
                
                self.qtySaleEntry.delete(0,currentEntry)         
                self.qtySaleEntry.insert(0,currentEntry+1)
        def quantityDecrease():
            currentEntry = self.qtySaleEntry.get()
            #print("type is ", type(currentEntry))
            if currentEntry == "":
                currentEntry = 0
            else: currentEntry = int(self.qtySaleEntry.get())
            if currentEntry > 1 :
                self.qtySaleEntry.delete(0,currentEntry)
                self.qtySaleEntry.insert(0,currentEntry-1)
                    

        
        self.qtyDecreaseButton = ttk.Button(master=quantity_frame, text="-", 
                                            width=5, style="success.TButton",
                                            command=quantityDecrease
                                            )
        self.qtyDecreaseButton.pack(side="left", anchor="w")
        self.qtySaleEntry = ttk.Entry(master=quantity_frame, #placeholder_text=0,
                                       style="success.TEntry", font=("Arial Black", 16),
                                       width=5
                                        )
        self.qtySaleEntry.pack(side="left", anchor="w", padx=10)
        self.qtyIncreaseButton = ttk.Button(master=quantity_frame, text="+", width=5,  
                                           style="success.TButton",
                                           command=quantityIncrease
                                           )
        self.qtyIncreaseButton.pack(side="left", anchor="w")
        
        #self.detailsFrame = ttk.Frame(master=self.searchGrid, fg_color="transparent")
        self.qtyInStockLabel = ttk.Label(master=self.searchGrid, text = "Quantity in Stock: 0",
                                        font=("Calibri", 15, "bold"), 
                                        style="success.TLabel",
                                        )
        self.qtyInStockLabel.grid(row=3, column=0, sticky="w", padx = padx_values, pady=30)
        
        self.update()
        self.windowWidth = self.winfo_width()

        self.warningLabel = ttk.Label(master=self,
                                    text = "",font=("Calibri", 17), 
                                style="TLabel.success" )
        
        
        self.warningLabel.place(x=self.windowWidth//2, y = 300)
        self.warningLabel.pack()

        self.billTableFrame = ttk.Frame(master=self, bootstyle="default")
        self.billTableFrame.pack(expand=True, fill="both", padx=gridPadding, pady=21)

        self.clearTableButton = ttk.Button(master=self.billTableFrame, text="Clear Table",
                                      
                                      style="success.TButton", 
                                      
                                      command=clearBillTable)
        self.clearTableButton.pack(side="top",  anchor = "ne")

        self.billTable = ttk.Treeview(master=self.billTableFrame, 
                                  columns=["Time Stamp", "Med Name", "Type", "MRP", "Quantity", "Total Price"],
                                  show="headings",
                                    #yscrollcommand=self.treeSrollBar,
                                    selectmode="extended",
                                  style="success.Treeview")
        #self.billTable.edit_row(0, text_color="#fff", hover_color="#2A8C55")
        #self.billTable.pack(expand=True)

        self.billTable.column("Time Stamp", width=75)
        self.billTable.column("Med Name", width=75)
        self.billTable.column("Type", width=75)
        self.billTable.column("MRP", width=75)
        self.billTable.column("Quantity", width=75)
        self.billTable.column("Total Price",width=75)


        self.billTable.heading("Time Stamp", text="Time Stamp", anchor=W)
        self.billTable.heading("Med Name", text="Med Name", anchor=W)
        self.billTable.heading("Type", text="Type", anchor=W)
        self.billTable.heading("MRP", text="MRP", anchor=W)
        self.billTable.heading("Quantity", text="Quantity", anchor=W)
        self.billTable.heading("Total Price", text="Total Price", anchor=W)
   
        self.billTable.pack(expand=True, fill='both', pady=(10,0))

        self.billTotalLabel = ttk.Label(master=self.billTableFrame, text="Bill Total: 0",
                                       font=("Calibri", 15, "bold"), 
                                        style="successTLabel."
                                        )
        self.billTotalLabel.pack(anchor="ne", side="right",pady=(20,0))

        def addToInvoices():
            
            #insLastRowNo = len(inoviceWS.col_values(insDateColNo))+1
            clientName = self.clientNameEntry.get()
            clientPhone = self.clientPhoneEntry.get()
            comment = self.commentEntry.get()
            
            payMode = self.payModeCombobox.get()
            clientUId = self.clientUIDEntry.get()
            invDate = strftime("%Y-%m-%d %H:%M")
            condition = f"Date_format(InvoiceDate, '%Y-%m-%d')  = '{today}'"
            Invcount = selectTable('MedicineInvoices', column_names='count(*)', condition=condition )
            Invcount = f"{Invcount[0][0]+1:02}"
            if self.discountEntry.get():
                discountAmount = int(self.discountEntry.get())
                #billTotal = billTotal-discountAmount
            else:
                discountAmount = 0

            InvoiceId = 'PM'+str(date.today().strftime("%y"))+str(f"{date.today().timetuple().tm_yday:03}")+str(Invcount)

            if self.warningLabel.cget("text") == "Warning: Invalid Name" or self.warningLabel.cget("text") == "Warning: Phone number needs 10 digits":
                self.warningLabel.configure(text = "")
            
            if len(clientName)==0:
                self.warningLabel.configure(text = "Warning: Invalid Name")
                messagebox.showwarning("Warning", "Invalid Name")

            
            elif len (clientPhone) != 10:
                self.warningLabel.configure(text = "Warning: Phone number needs 10 digits")
                messagebox.showwarning("Warning", " Phone number needs 10 digits.")

            elif len(payMode) == 0:
                self.warningLabel.configure(text = "Warning: Select the payment mode for this bill")
                messagebox.showwarning("Warning", "Select the payment mode for this bill.")
            else:
                insertIntoTable('MedicineInvoices', f"('{invDate}','{InvoiceId}' , '{clientUId}','{billTotal}','{discountAmount}','{payMode}','{clientName}', '{clientPhone}', '{comment}')", 
                                column_names= "InvoiceDate,	InvoiceId,	UHId,	TotalAmount,	DiscountAmount,	PaymentMode, PName, PhoneNo, Comments" )
                #InvoiceDate	InvoiceId	UHId	TotalAmount	DiscountAmount	PaymentMode
            return InvoiceId    





        def confirmDetails():
            
            currInvoiceNo = addToInvoices() 
            #clientUId = self.clientUIDEntry.get()
            
            if self.warningLabel.cget("text") == "Warning: Invalid Name" or self.warningLabel.cget("text") == "Warning: Phone number needs 10 digits":
                pass

            else:                
                
                billData = []
                billItems = len(self.billTable.get_children())
                
                BTotal = 0
                for record in self.billTable.get_children():
                    
                    recValues = list(self.billTable.item(record,'values'))
                    
                    billData.append(recValues)
                    saleId = currInvoiceNo+str(f"{len(billData):02}")
                    currentMedName = recValues[1]
                    currentMedId = str(medicineDf.loc[medicineDf["MName"] == currentMedName]["MId"].iloc[0])
                    MTotal = float(recValues[5])
                    BTotal = float(BTotal)+float(MTotal)
                    insertIntoTable('Pharmacy', f"('{saleId}','{currentMedId}','{currInvoiceNo}' , '{recValues[4]}','{MTotal}','{BTotal}')", 
                                column_names= "SaleId,	MId,	InvoiceId,	Mstock,	MTotal,	BTotal" )
                    

                printBill(currInvoiceNo)

                for record in self.billTable.get_children():
                    self.billTable.delete(record)

                self.clientUIDEntry.delete(0,END)
                self.clientNameEntry.delete(0,END)     
                self.clientPhoneEntry.delete(0,END)
                self.clientGenderCbox.set("")   
                self.payModeCombobox.set("")
                self.commentEntry.delete(0,END)
                self.discountEntry.delete(0,END)

                  
                                 
            



        def selectRecord(event):
            # Clear entry boxes
            self.itemNameEntry.delete(0,END)
            self.qtySaleEntry.delete(0,END)
            
            
            # Grab record Number
            selected = self.billTable.focus()
            # Grab record values
            values = self.billTable.item(selected,'values')
            values = list(values)
            self.billTable.delete(selected)
            global billTotal
            #print(values)
            # outpus to entry boxes
            self.itemNameEntry.insert(0,values[1])
            self.qtySaleEntry.insert(0,values[4])
            billTotal = int(billTotal)-float(values[5])
            self.billTotalLabel.configure(text= "Bill Total: " + str(billTotal))
            #self.qtyInStockLabel.configure(text="Quantity in Stock:")
            #self..insert(0, values[6])"""
            onMedNameSelect(event)

        #def update_record():
        self.billTable.bind("<Double-Button-1>", selectRecord)

        self.billConfirmButton = ttk.Button(master=self.billTableFrame, text="Confirm Details",
                                      style="success.TButton",
                                      command=confirmDetails)
        
        self.billConfirmButton.pack(anchor="ne", side="right",padx = (0,20), pady=(20,0))

        self.discountLabel = ttk.Label(master=self.billTableFrame, text="Discount",
                                       font=("Calibri", 15, "bold"), 
                                        style="success.TLabel"
                                        )
        self.discountLabel.pack(anchor="ne", side="left",pady=(20,0))
        
        discountAmount = IntVar()
        self.discountEntry = ttk.Entry(master=self.billTableFrame, text="Discount",
                                       textvariable=discountAmount,
                                       font=("Calibri", 12, "bold"),
                                       width=8,style="success.TEntry")
        self.discountEntry.pack(anchor="ne", side="left",padx=(15,0), pady=(20,0))

        
        def applyDiscount():
            discountedBillTotal = float(billTotal) - discountAmount.get()
            self.billTotalLabel.configure(text= "Bill Total: " + str(discountedBillTotal))

        self.applyDiscountButton = ttk.Button(master=self.billTableFrame, text="Apply Discount",
                                style="success.TButton",
                                command=applyDiscount)
        
        self.applyDiscountButton.pack(anchor="ne", side="left",padx=(15,0), pady=(20,0))

        def focusEntry(event):
           fw = master.focus_get()
           fw.delete(0,END)

        
        self.commentLabel = ttk.Label(master=self.billTableFrame, text="Comments",
                                      font=("Calibri", 15, "bold"), 
                                        style="success.TLabel")
        self.commentLabel.pack(anchor="ne", side="left",padx=(15,0),pady=(20,0))
        self.commentEntry = ttk.Entry(master=self.billTableFrame,                                        
                                       font=("Calibri", 12, "bold"),
                                       width=30,style="success.TEntry")
        self.commentEntry.pack(anchor="ne", side="left",padx=(10,0), pady=(20,0))
        
        #self.commentEntry.bind("<Button-1>", focusEntry)
        



if __name__ == "__main__":
    app = tk.Tk()
    MainViewFrame(app)
    app.mainloop()
