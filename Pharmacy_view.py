from customtkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
from PIL import Image, ImageTk
from database import selectTable, getClientID, insertIntoTable
#from CTkScrollableDropdown import *
import pandas as pd
#from CTkTable import CTkTable
from time import strftime
import sqlite3
#from tkcalendar import DateEntry
import ttkbootstrap as tkb
#from treeactions import *
from datetime import datetime
#from gspreaddb import getOPData,getClientid, opWS



class pharmacyViewFrame(ttk.Frame):
    def __init__(self, master=NONE):
        super().__init__(master, width=950, height=850, relief = tk.GROOVE)
        self.pack_propagate(0)
        self.grid(column=1, row=0, padx=(30,30), pady=(10,10))

        self.titleFrame = ttk.Frame(master=self)
        self.titleFrame.pack(anchor="w", pady=(29, 0), padx=27)
        
        self.titleLabel = ttk.Label(master=self.titleFrame, text="Pharmacy View", 
                                   font=("Calibri", 25, "bold"), style = "TLabel.success" )
        self.titleLabel.grid(row=0, column=0, sticky="w", padx=(30,30))


        self.timeLabel = ttk.Label(master=self.titleFrame, font=("Calibri", 17, "bold"), style = "TLabel.success" )
        self.timeLabel.grid(row=0, column=1, sticky="e",padx = (350,0))
        def get_time():
            string = strftime('%I:%M:%S %p')
            self.timeLabel.configure(text=string)
            self.timeLabel.after(1000, get_time)
        get_time()

        self.windowWidth = self.winfo_width()
        # Search Section
        
        self.fetchDetGrid = ttk.Frame(master=self)
        self.fetchDetGrid.place(x=self.windowWidth//2)
        self.fetchDetGrid.pack(pady=(20, 0))

        def uidEntryBind(event):
            if self.uidFetchEntry.get() == "Enter UID":
                self.uidFetchEntry.delete(0, END)
            else :
                pass
        self.uidFetchEntry = ttk.Entry(master=self.fetchDetGrid, 
                                         style = "TEntry.success", 
                                          width=15)
        self.uidFetchEntry.grid(row=0,column=0)
        self.uidFetchEntry.insert(0, "Enter UID")
        self.uidFetchEntry.bind("<Button-1>",uidEntryBind)
        #self.clientAmountEntry.grid(row=1, column=3, sticky='w',padx = (0,30))         
        def removeAll():
            for record in self.billTable.get_children():
                self.billTable.delete(record) 
        def fetchDetails():
            selected_date = self.dateFetchEntry.entry.get()
            
            selected_date = datetime.strptime(selected_date, "%d-%m-%Y").strftime("%Y-%m-%d")
            
            rowsWithDate = selectTable('vw_dailyPharmacyDetails', condition=f"InvoiceDate = '{selected_date}'")
            
            removeAll()
            
            #client_id, strftime("%d-%m-%Y, %H:%M:%S"),  currentClientName, currentClientPhone, currentClientGender, currentClientAge, currentOPProc, currentPaymentMode, currentAmount

            for x in rowsWithDate:
                #print(rowsWithDate)
                self.billTable.insert("", END, values=list(x))
            self.dateFetchEntry.entry.delete(0, tk.END)
            self.dateFetchEntry.entry.insert(0, strftime("%d-%m-%Y"))

        dateFetchEntry = StringVar()
        self.dateFetchEntry = tkb.DateEntry(self.fetchDetGrid, bootstyle="success")
        self.dateFetchEntry.grid(row=0,column=1,padx=(80,30))


        self.searchByCbox = ttk.Combobox(master=self.fetchDetGrid, style= 'TCombobox.success',
                                            values=("InvoiceId", "Patient Name", "Phone", "Date" ), state='readonly', 
                                            justify=CENTER, font=("calibri", 12, "bold"), 
                                             cursor='hand2')
        self.searchByCbox.grid(row=0, column=2,sticky="w", pady=20, padx = (0,30))

        self.fetchDetailsButton = ttk.Button(master=self.fetchDetGrid, text="Fetch Details",
                                       style = "TButton.success",
                                      command=fetchDetails)
        self.fetchDetailsButton.grid(row=0, column=3,sticky="w" ,pady=(0,0),padx = (0,30))

        self.billTableFrame = ttk.Frame(master=self, bootstyle="default")
        self.billTableFrame.pack(expand=True, fill="both", padx=27, pady=21)

        self.billTable = ttk.Treeview(master=self.billTableFrame, 
                                  columns=["Time Stamp",  "Patient Name", "Med Name", "MRP", "Quantity", "Med Total","PaymentMode", "Bill Amount"],
                                  show="headings",
                                    #yscrollcommand=self.treeSrollBar,
                                    selectmode="extended",
                                  style="success.Treeview")
        #self.billTable.edit_row(0, text_color="#fff", hover_color="#2A8C55")
        #self.billTable.pack(expand=True)

        self.billTable.column("Time Stamp", width=75)
        self.billTable.column("Med Name", width=75)
        self.billTable.column("Patient Name", width=75)
        self.billTable.column("MRP", width=75)
        self.billTable.column("Quantity", width=75)
        self.billTable.column("Med Total",width=75)
        self.billTable.column("PaymentMode",width=75)
        self.billTable.column("Bill Amount",width=75)


        self.billTable.heading("Time Stamp", text="Time Stamp", anchor=W)
        self.billTable.heading("Med Name", text="Med Name", anchor=W)
        self.billTable.heading("Patient Name", text="Patient Name", anchor=W)
        self.billTable.heading("MRP", text="MRP", anchor=W)
        self.billTable.heading("Quantity", text="Quantity", anchor=W)
        self.billTable.heading("Med Total", text="Med Total", anchor=W)
        self.billTable.heading("PaymentMode", text="PaymentMode", anchor=W)
        self.billTable.heading("Bill Amount", text="Bill Amount", anchor=W)
   
        self.billTable.pack(expand=True, fill='both', pady=(10,0))

        self.billTotalLabel = ttk.Label(master=self.billTableFrame, text="Bill Total: 0",
                                       font=("Calibri", 15, "bold"), 
                                        style="successTLabel."
                                        )
        self.billTotalLabel.pack(anchor="ne", side="right",pady=(20,0))

        fetchDetails()
        
if __name__ == "__main__":
    root = tk.Tk()
    obj = pharmacyViewFrame(root)
    root.mainloop()