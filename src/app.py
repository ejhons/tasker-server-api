from tkinter import *

app = Tk(screenName='Calculadora de vazão')

app.title('Calculadora')

l1 = Label(app, text='Calculadora de Vazão').grid(row=0)
l2 = Label(app, text='Coeficiente de escoamento: ').grid(row=1, sticky=W)
l3 = Label(app, text='Intensidade (mm/h): ').grid(row=2, sticky=W)
l4 = Label(app, text='Área (ha)').grid(row=3, sticky=W)

v1 = DoubleVar()
e1 = Entry(app)
e2 = Entry(app)
e3 = Entry(app)

e1.grid(row=1, column=1)
e2.grid(row=2, column=1)
e3.grid(row=3, column=1)

lr = Label(app, text='A vazão calculada é: ').grid(row=4)

bt = Button(app, text='Calcular', width=30, command=app.destroy)
bt.grid(row=5)


# Run application
try:
    mainloop()
except ():
    print('Comando encerrado.')

print(e1.get())

# quadroGrid = LabelFrame(app, text='Contatos')
