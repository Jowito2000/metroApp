import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import metro as m
from data import coor
import tkinter.font as tkFont

root = tk.Tk()
root.configure(background='white')
root.resizable(False,False)
root.wm_title('metroApp')
font = tkFont.Font(family='Franklin Gothic Medium', size=14, weight='bold')
font1 = tkFont.Font(family='Franklin Gothic Medium', size=14)
font2 = tkFont.Font(family = 'Calibri', size=14, weight = 'bold') # Verdana funciona. Georgia esta curiosa. 'Franklin Gothic Medium' esta fancy. Calibri en negrita la mejor en Windows
# Si cambias el tamaño de la letra, hay que reducir o ampliar el weight y el height de la ruta_list

# Datos
data = list(coor.keys())
data.sort()

# Funciones
def calcularRuta():
    ruta_list.configure(state=tk.NORMAL)
    ruta_list.delete('1.0',tk.END)
    value_o = origen_drop.get()
    value_d = destino_drop.get()
    if(value_o != '' and value_d != '' and value_o == value_d):
        ruta_list.insert(tk.END, 'Ya estás en tu estación de destino')
    elif(value_o == '' and value_d == '' ):
        ruta_list.insert(tk.END, 'Introduzca una estación de origen y otra de destino')
    elif(value_o == ''):
        ruta_list.insert(tk.END, 'Introduzca una estación de origen')
    elif(value_d == ''):
        ruta_list.insert(tk.END, 'Introduzca una estación de destino')
    else:
        ruta = m.astarPrint(m.astar(value_o, value_d))
        ruta_list.insert(tk.END, ruta)
    ruta_list.configure(state=tk.DISABLED)
            

# Partes
# Buscar Ruta ------
buscarRuta = tk.LabelFrame(root, text='Elija la ruta', font=font, background = 'white')
buscarRuta.grid(row=0, columnspan=3, sticky=tk.W+tk.N, 
                padx=5, pady=5, ipadx=5, ipady=5)

# Origen ------
origen_Label = tk.Label(buscarRuta, text='Origen', font=font1, background = 'white')
origen_Label.grid(row=0, column=0, sticky='E', padx=5, pady=2)

origen_drop = ttk.Combobox(buscarRuta, width=31, font=('',13), state='readonly')
origen_drop['values'] = data
origen_drop.grid(row=0,column=1)


# Destino ------------
destino_Label = tk.Label(buscarRuta, text='Destino', font=font1, background = 'white')
destino_Label.grid(row=0, column=2, sticky='E', padx=5, pady=2)

destino_drop = ttk.Combobox(buscarRuta, width=31, font=('',13), state='readonly')
destino_drop['values'] = data
destino_drop.grid(row=0,column=3)

# Calcular Ruta Optima boton
button_r = tk.Button(buscarRuta, text=' ▶ ', font=('bold',17), command = calcularRuta, activebackground = 'gray70', background = 'gray95', activeforeground = 'white')
button_r.grid(row=0, column=4, padx=5, sticky='E')

# Ruta -----------------------------------------
# Definir listbox de ruta y su scrollbar
ruta_list = tk.Text(root, bd=0, font=font2, width=35, height=15, foreground = 'gray20')
scrollbar_r = tk.Scrollbar(root, command=ruta_list.yview)
ruta_list.configure(yscrollcommand=scrollbar_r.set, state=tk.DISABLED)
ruta_list.grid(row=2, column=1, padx=20, pady=2, sticky='nsw')
scrollbar_r.grid(row=2, column=2, sticky='nse')


ruta_list.configure(state=tk.DISABLED)

# Imagen del mapa
athens = Image.open('athens-metro-map.png')
athens = athens.resize((400,414), Image.ANTIALIAS)
athens = ImageTk.PhotoImage(athens)
athens_label = tk.Label(root, image=athens)

athens_label.grid(row=2,column=0)

root.mainloop()