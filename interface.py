from Tkinter import *
import psycopg2
import csv
import webbrowser
from time import sleep
from time import strftime
from pandas import DataFrame
import subprocess
import Tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

conn = psycopg2.connect(host='192.168.42.100', user='hu', database='ptw', password='password')
cur = conn.cursor()
window = Tk()
window.title("Interface")
window.geometry('800x300')
def tekst():
    lbl = Label(window, text="Hiernaast is een tabel met"
                "de metingen van de laatste 10 minuten.")
    lbl.grid(column=5, row=0)
    
def tabel():
    lbl = Label(window, text="Datum")
    lbl.grid(column=1, row=1)
    lbl = Label(window, text="Tijd")
    lbl.grid(column=2, row=1)
    lbl = Label(window, text="Decibel")
    lbl.grid(column=3, row=1)
    lbl = Label(window, text="Locatie")
    lbl.grid(column=4, row=1)
    query = """SELECT * FROM metingen WHERE tijd < %s AND datum=%s ORDER BY tijd DESC;"""
    values = (strftime("%H:%M:%S"), strftime("%Y-%m-%d"))
    cur.execute(query, values)
    height = 1
    for row in cur.fetchall():
        height = height + 1
        width = 0
        if height == 11:
            break
        else:
            for meting in row:
                width = width + 1
                lbl = Label(window, text=meting)
                lbl.grid(column=width, row=height)
def sluit():
    window.destroy()
    
def grafiek():
    newwin= Toplevel(window)
    newwin.geometry("500x300")
    Data2 = {'Tijd': [08.00, 09.00, 10.00, 11.00, 12.00, 13.00, 14.00, 15.00, 16.00, 17.00, 18.00],
             'Decibel': [19, 36, 20, 15, 50, 45, 30, 25, 30, 27, 20]}
    df2 = DataFrame(Data2, columns=['Tijd', 'Decibel'])
    df2 = df2[['Tijd', 'Decibel']].groupby('Tijd').sum()
    figure2 = plt.Figure(figsize=(5, 3), dpi=100)
    ax2 = figure2.add_subplot(111)
    line2 = FigureCanvasTkAgg(figure2, newwin)
    line2.get_tk_widget().grid(row=2, column=10)
    df2.plot(kind='line', legend=True, ax=ax2, color='g', marker='o', fontsize=10)
    ax2.set_title('de grafiek')
tekst()
tabel()
print(strftime("%Y-%m-%d"))
btn1 = tk.Button(window, text='Update tabel', command=tabel)
btn2 = tk.Button(window, text='sluit window', command=sluit)
btn3 = tk.Button(window, text='open grafiek', command=grafiek)
btn1.grid(row=0, column=1)
btn2.grid(row=0, column=2)
btn3.grid(row=0, column=3)

window.mainloop()