from customtkinter import *
import tkinter as tk
from tkinter import ttk
from database import selectTable, getClientID, insertIntoTable
import pandas as pd
from time import strftime
from datetime import datetime
import ttkbootstrap as tkb
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *




class pharmacyViewFrame(ttk.Frame):
    def __init__(self, master=NONE):
        super().__init__(master, width=1050, height=850, relief = tk.GROOVE)
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
            for i,record in enumerate(self.billTable.get_rows()):
                self.billTable.delete_row(i) 
        def fetchDetails():
            removeAll()
            selected_date = self.dateFetchEntry.entry.get()
            print(selected_date)
            selected_date = datetime.strptime(selected_date, "%d-%m-%Y").strftime("%Y-%m-%d")
            print(selected_date)
            rowsWithDate = selectTable('vw_dailyPharmacyDetails', condition=f"Date(InvoiceDate) = '{selected_date}'")
            self.billTable.build_table_data(coldata,rowsWithDate)
            
            Totals = selectTable('vw_cashUPI_split', column_names='PaymentMode, Totals', condition=f"Date_format(InvoiceDate, '%Y-%m-%d') = '{selected_date}' order by 1")



            #client_id, strftime("%d-%m-%Y, %H:%M:%S"),  currentClientName, currentClientPhone, currentClientGender, currentClientAge, currentOPProc, currentPaymentMode, currentAmount

            """for i,x in enumerate(rowsWithDate):
                #print(rowsWithDate)
                row_color = "white" if i % 2 == 0 else "#f0f0f0"
                self.billTable.insert_row(index= END, values=list(x))#,tags={"style": {"background": row_color}})"""
            self.billTable.load_table_data()
            self.billTotalLabel.configure(text=f"Cash : {Totals[1][1]}   UPI: {Totals[2][1]}  Both: {Totals[0][1]}       Total: {Totals[1][1]+Totals[2][1]+Totals[0][1]}")
            self.dateFetchEntry.entry.delete(0, tk.END)
            self.dateFetchEntry.entry.insert(0, strftime("%d-%m-%Y"))
        style = ttk.Style()
        style.configure(
            "success.TButton",
            font=("Helvetica", 14),  # Set a larger font size
        )
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

        self.billTableFrame = ttk.Frame(master=self)
        self.billTableFrame.pack(expand=True, fill="both", padx=27, pady=21)

        style = ttk.Style()
        #style.theme_use("default")  # Ensure the theme supports custom styles
        style.configure("Custom.Treeview", font=("Helvetica", 13), rowheight=25,borderwidth=1) 
                          # Set row font size and height
        style.configure("Custom.Treeview.Heading", font=("Helvetica", 13, "bold"), borderwidth=1)  # Set heading font size
        #style.map("Custom.Treeview", background=[("alternate", "#E8E8E8")])  # Striped rows

        

        
        coldata= [{"text":"Time Stamp","stretch": TRUE} ,
                  {"text":"Patient Name","stretch": TRUE} ,
                  {"text":"Med Name","stretch": TRUE},
                  {"text":"MRP","stretch": TRUE},
                  {"text":"Quantity","stretch": FALSE} ,
                  {"text":"Med Total","stretch": TRUE},
                  {"text":"PayMode","stretch": TRUE} ,
                  {"text":"Bill Total","stretch": TRUE},
                  {"text":"Discount","stretch": TRUE},
                  {"text":"Comments","stretch": TRUE}]
        
        # Create the Treeview
        self.billTable = Tableview(
            master=self.billTableFrame,
            coldata=coldata,
            pagesize = 200,
            autofit = True,
            #selectmode="extended",
            paginated=True,
            #rowcolors=("white", "#f0f0f0"),
            #style="Custom.Treeview",  # Apply the custom style

            bootstyle = SUCCESS,
            stripecolor=('#02b875', 'black')

        )
        self.billTable.configure(style="Custom.Treeview")

        # Configure headings and columns
        #for col in ["Time Stamp", "Patient Name", "Med Name", "MRP", "Quantity", "Med Total", "PaymentMode", "Bill Amount"]:
        #    self.billTable.heading(col, text=col, anchor=tk.W)
        #    self.billTable.column(col, width=150, anchor=tk.W)  # Adjust width for better readability

        # Pack the Treeview
        self.billTable.pack(expand=True, fill="both", pady=(10, 0))
        
        
        def set_column_widths():
        # Set explicit widths for each column
            column_widths = {
                "Time Stamp": 150,
                "Patient Name": 150,
                "Med Name": 150,
                "MRP": 100,
                "Qty": 100,
                "Med Total": 150,
                "PayMode": 200,
                "Bill Amount": 100,
                "Discout":75,
                "Comments": 200
    
            }

        #for col_name, width in column_widths.items():
        #self.billTable.Ta(width=200, stretch=FALSE)
        #set_column_widths()
        selected_date = '2025-01-06'
        
        self.billTotalLabel = ttk.Label(master=self.billTableFrame, text="Totals: 0",
                                       font=("Calibri", 15, "bold"), 
                                        style="successTLabel."
                                        )
        self.billTotalLabel.pack(anchor="c", side="right",pady=(20,0))

        fetchDetails()
        
if __name__ == "__main__":
    root = tk.Tk()
    obj = pharmacyViewFrame(root)
    root.mainloop()