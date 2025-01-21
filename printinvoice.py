from reportlab.lib.units import inch
from reportlab.platypus import Image
from datetime import date
import sqlite3
import pandas as pd

import time
import datetime
from database import selectTable


start_time = time.time()


def getBillDetails(billNo):
    

    rowsWithBillNo = selectTable('vw_getPharmacyDetails', condition=f"InvoiceId = '{billNo}'" )
    
    print(rowsWithBillNo)
    return rowsWithBillNo

def my_temp(c):
    # Set A5 size dimensions
    a5_width, a5_height = 5.8 * inch, 8.3 * inch
    c.translate(a5_width - 0.05 * inch, 0.05 * inch)  # Adjust origin to top-left corner
    
    # define a smaller font for A5
    c.setFont("Helvetica", 10)
    
    # Other adjustments...
    c.setStrokeColorRGB(0, 1, 0)
    c.setFillColorRGB(0,0,1)
    c.rotate(90)
    c.drawImage('Images\Logo.jpg',  3.55 * inch, 4.8 * inch, width=60, height=60)
    #c.drawImage('Images\Logo.png', 3.3 * inch, 4.8 * inch)
    c.setFont("Helvetica", 20)
    c.drawString(0.2*inch, 5.4 * inch, "Pranith Medical Store")
    c.setFont("Helvetica", 12)
    c.drawString(0.2*inch, 5.2 * inch, "#25-684-15, TTD Road, Doctor's Lane")
     
    c.drawString(0.2*inch, 5.0 * inch, "Nandyal, 518501")
    c.setFont("Helvetica", 8)
    c.drawString(0.2*inch,4.8 * inch, "D.L.NO20B: AP/23/21/2024-47178")
    c.drawString(0.2*inch,4.6 * inch, "D.L.NO21B: AP/23/21/2024-47179")
    c.drawString(6.2 * inch, 4.6 * inch, f'Doctor: Dr. C Madhu Preethi')

    c.setFont("Helvetica", 10)
    c.setStrokeColorRGB(0, 1, 0)  # line colour
    c.line(0.2, 4.5 * inch, 8.0 * inch, 4.5 * inch)
    
    
    dt = date.today().strftime('30-05-%Y')
    
    
    
    # Other adjustments...
    
    c.setFillColorRGB(1, 0, 0)  # font colour
    c.setFont("Times-Bold", 16)
    c.drawString(3.5 * inch, 4.6 * inch, 'INVOICE')

    
    # Other adjustments...
    
    # Set vertical line color
    c.setStrokeColorCMYK(0, 0, 0, 1)
    
    # Other adjustments...
    
    # Set horizontal line total
    global ProductLine
    global RateLine
    global QtyLine
    global AmtLine
    global billYLine
    global PcodeLine

    PcodeLine = 0.5
    ProductLine = PcodeLine + 0.9
    RateLine = ProductLine + 2.4
    QtyLine = RateLine+0.7
    AmtLine = QtyLine+1.2
    
    billYLine = 1.9
    
    c.setFont("Times-Bold", 12)
    c.drawString(0.2 * inch, 4.3 * inch, 'Id')
    c.line(PcodeLine * inch,4.5* inch, PcodeLine * inch, billYLine * inch)    
    c.drawString((PcodeLine+0.05) * inch, 4.3 * inch, 'P Code')
    c.line(ProductLine * inch,4.5* inch, ProductLine * inch, billYLine * inch)
    c.drawString((ProductLine+0.05) * inch, 4.3 * inch, 'Product')  
    c.line(RateLine * inch,4.5* inch, RateLine * inch, billYLine * inch)
    c.drawString((RateLine+0.05) * inch, 4.3 * inch, 'Rate')
    c.line(QtyLine * inch,4.5* inch, QtyLine * inch, billYLine * inch)
    c.drawString((QtyLine +0.05) * inch, 4.3 * inch, 'Quantity')
    c.line(AmtLine * inch,4.5* inch, AmtLine * inch, billYLine * inch)
    c.drawString((AmtLine+.05) * inch, 4.3 * inch, 'Amount')
    c.line(0.2, 4.2 * inch, 8.0 * inch, 4.2 * inch)
    # Other adjustments...
    
    
    c.drawString(0.5 * inch, -5.5 * inch, 'Discount')
    c.drawString(0.5 * inch, -6.2 * inch, 'Tax')
    
    # Other adjustments...
    
    c.setFont("Times-Bold", 12)
    c.drawString(1 * inch, -6.7 * inch, 'Total')
    
    # Other adjustments...
    
    c.setFont("Times-Roman", 12)
    c.drawString(3.5 * inch, -7.3 * inch, 'Signature')
    
    # Bottom Line color
    c.setStrokeColorRGB(0.1, 0.8, 0.1)
    c.line(0, -7.8 * inch, 5.5 * inch, -7.8 * inch)
    
    c.setFont("Helvetica", 6)  # font size
    c.setFillColorRGB(1, 0, 0)  # font colour
    c.drawString(0, -8 * inch, u"\u00A9" + " plus2net.com")
    
    return c


from reportlab.pdfgen import canvas
#$bill_No = "PM2403404"

from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, A5
#from temp_invoice import my_temp # import the template
#from invoice_data import *  # get all data required for invoice
def printBill(bill_No):
    
    my_prod = getBillDetails(bill_No)
    if my_prod[0][2]:
        ptName = my_prod[0][2]
    else:
        ptName = "   "
    my_path=r'Invoices\{}.pdf'.format(bill_No + "_" + ptName) 
    c = canvas.Canvas(my_path,pagesize=A5)
    c=my_temp(c) # run the template
    
    #print(ProductLine, QtyLine, AmtLine, RateLine)
    c.setFillColorRGB(0,0,0) # font colour

    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0, 0, 1)
    c.drawString(6.2 * inch, 5.0 * inch, f'Invoice No: {bill_No}')

    c.setFont("Helvetica", 8)
    row_gap=0.15 # gap between each row
    line_y=4.05 # location of fist Y position 
    total=0
    i = 1
    for rec in my_prod:
        print(rec)
        c.drawString((0.2+0.05)*inch,line_y*inch,str(i))
        c.drawString((PcodeLine+0.05)*inch,line_y*inch,str(rec[5])) # product Code
        c.drawString((ProductLine+0.05)*inch,line_y*inch,str(rec[3])) # p Name
        c.drawString((RateLine +0.05)*inch,line_y*inch,str(rec[6])) # p Price
        
        c.drawString((QtyLine+0.05)*inch,line_y*inch,str(rec[4])) # p Qant 
        sub_total=float(rec[6])*int(rec[4])
       
        c.drawString((AmtLine+0.05)*inch,line_y*inch,str(sub_total)) # Sub Total 
        total=round(total+sub_total,1)
        line_y=line_y-row_gap
        i+=1
    
    
    #date_object = datetime.datetime.strptime(my_prod[0][1], '%d/%m/%Y, %H:%M:%S')
    billDate = str(my_prod[0][1].strftime('%d-%b-%Y'))
    c.setFont("Times-Bold", 10)
    c.setFillColorRGB(0,0,1)
    c.drawString(6.8 * inch, 5.25 * inch, billDate)
    c.setFillColorRGB(0,0,0)
    c.drawRightString((AmtLine -0.05)*inch, (billYLine-row_gap) * inch, 'Bill Amount: ')
    c.drawString((AmtLine+0.05)*inch,(billYLine-row_gap)*inch,str(float(total))) # Total
    c.drawString(0.2 * inch, (billYLine-row_gap) * inch, 'Name: ')
    c.drawString((PcodeLine+0.08)*inch,(billYLine-row_gap)*inch,ptName)
    #discount=round((discount_rate/100) * total,1)
    #c.drawRightString(4*inch,1.8*inch,str(discount_rate)+'%') # discount
    #c.drawRightString(7*inch,1.8*inch,'-'+str(discount)) # discount
    #tax=round((tax_rate/100) * (total-discount),1)
    #c.drawRightString(4*inch,1.2*inch,str(tax_rate)+'%') # tax 
    #c.drawRightString(7*inch,1.2*inch,str(tax)) # tax 
    total_final=total
    c.setFont("Times-Bold", 22)
    c.setFillColorRGB(1,0,0) # font colour
    #c.drawRightString(2*inch,0.8*inch,str(total_final)) # tax 
    c.rotate(90)
    c.showPage()
    c.save()

"""
billNo = 'PM2500808'
#ptName = 'Arshiya'
#billData = getBillDetails(billNo)
printBill(billNo)"""