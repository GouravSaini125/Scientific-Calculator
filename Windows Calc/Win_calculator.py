from tkinter import *
from math import *
import tkinter.messagebox as msg


class Calc(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.frames = {}

        MainMenu(self)

        winmain = Frame(self)
        winmain.pack(side=TOP, fill=BOTH, expand=TRUE)
        winmain.grid_rowconfigure(0, weight=1)
        winmain.grid_columnconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        for F in (Regular, Scientific):
            frame = F(winmain, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_calc(Regular,'Regular')

    def show_calc(self, frame,current):
        if current=='Regular':
            self.geometry('285x400')
            self.resizable(0,0)
        else:
            self.geometry('350x520')
            self.resizable(0, 0)
        calc = self.frames[frame]
        calc.tkraise()
        calc.entry.focus()

    def on_closing(self):
        ans = msg.askyesnocancel('History', 'Do you want to clear the history?')
        if ans:
            file = open('history.txt', 'w')
            file.close()
            self.destroy()
        elif ans == None:
            pass
        else:
            file = open('history.txt', 'r')
            file.close()
            self.destroy()

    def history(self):
        file = open('history.txt', 'r')
        msg._show('History', file.read())


class Regular(Frame):
    def __init__(self, winmain, current):
        Frame.__init__(self, winmain)

        topframe = Frame(self)
        topframe.pack()
        self.switch = Button(topframe, text='Scientific',
                        command=lambda: current.show_calc(Scientific,'Scientific'),
                        width=7)
        self.switch.pack(pady=6, side=LEFT,padx=30)
        self.switch.bind('<Enter>',lambda event:self.entcolor(event,button=self.switch))
        self.switch.bind('<Leave>',lambda event:self.retcolor(event,'blue','white',button=self.switch))
        self.switch.configure(background='blue', foreground='white')

        self.file_btn = Button(topframe, text='History', command=current.history,
                          width=7)
        self.file_btn.pack(pady=6, side=LEFT,padx=30)
        self.file_btn.bind('<Enter>',lambda event:self.entcolor(event,button=self.file_btn))
        self.file_btn.bind('<Leave>',lambda event:self.retcolor(event,'green','white',button=self.file_btn))
        self.file_btn.configure(background='green', foreground='white')

        self.btns = ['1', '2', '3', 'AC', '4', '5', '6', '<-', '7', '8', '9',
                '/', '0', '.', '+', '*', '00', '%', '-', '=']
        self.exp = StringVar()
        self.exp.set("")

        self.butn=[]

        entframe = Frame(self)
        entframe.pack(fill=X)

        self.entry = Entry(entframe, textvariable=self.exp, justify=RIGHT,
                           font="verdana 20 bold",validate='key',
                           validatecommand=(self.register(self.char_len),'%S'))
        self.entry.pack(pady=8, padx=15)

        self.entry.bind('<Return>', self.equal)
        self.entry.bind('<Escape>', self.clear)
        self.entry.bind('<KP_Enter>', self.equal)
        #self.entry.icursor(1)

        if len(self.exp.get()) > 13:
            self.entry['font'] = 'verdana 15 bold'
        else:
            self.entry['font'] = 'verdana 20 bold'
        self.entry.update()

        row, column = 0, 0
        btnframe = Frame(self)
        btnframe.pack()

        for btn,i in zip(self.btns,range(20)):
            if btn == '4' or btn == '7' or btn == '0' or btn == '00':
                row += 1
                column = 0

            if btn == 'AC':
                self.butn.append ( Button(btnframe, text=btn, height=3, width=7, command=self.clear))
                self.butn[i].grid(row=row, column=column, pady=2, padx=3)
                self.butn[i].bind('<Enter>',lambda event:self.entcolor(event))
                self.butn[i].bind('<Leave>',lambda event:self.retcolor(event,'yellow'))
                self.butn[i].configure(background="yellow")
                column += 1

            elif btn == '<-':
                self.butn.append ( Button(btnframe, text=btn, height=3, width=7, command=self.delete))
                self.butn[i].grid(row=row, column=column, pady=2, padx=3)
                self.butn[i].bind('<Enter>',lambda event:self.entcolor(event))
                self.butn[i].bind('<Leave>',lambda event:self.retcolor(event,'red'))
                self.butn[i].configure(background="red")
                column += 1

            elif btn == '=':
                self.butn.append ( Button(btnframe, text=btn, height=3, width=7, command=self.equal))
                self.butn[i].grid(row=row, column=column, pady=2, padx=3)
                self.butn[i].bind('<Enter>',lambda event:self.entcolor(event))
                self.butn[i].bind('<Leave>',lambda event:self.retcolor(event,'yellow'))
                self.butn[i].configure(background="yellow")
                column += 1

            else:
                self.butn.append ( Button(btnframe, text=btn, height=3, width=7,
                              command=lambda char=btn: self.addch(char)))
                self.butn[i].grid(row=row, column=column, pady=2, padx=3)
                self.butn[i].bind('<Enter>',lambda event:self.entcolor(event))
                self.butn[i].bind('<Leave>',lambda event:self.retcolor(event,'cyan'))
                self.butn[i].configure(background="cyan")
                column += 1

    def clear(self,event=None):
        self.exp.set("")
        self.entry.update()

    def delete(self):
        self.exp.set(self.exp.get()[0:-1])
        if len(self.exp.get()) > 13:
            self.entry['font'] = 'verdana 15 bold'
        else:
            self.entry['font'] = 'verdana 20 bold'
        self.entry.update()

    def entcolor(self,event,button=False):
        if button:
            button.configure(background='white',fg='black')
        else:
            self.butn[self.btns.index(event.widget.cget('text'))].configure(background='white',fg='black')

    def retcolor(self,event,color,fg='black',button=False):
        if button:
             button.configure(background=color,fg=fg)
        else:
            self.butn[self.btns.index(event.widget.cget('text'))].configure(background=color,fg=fg)

    def addch(self, char):
        self.exp.set(self.exp.get() + str(char))
        if len(self.exp.get()) > 13:
            self.entry['font'] = 'verdana 15 bold'
        else:
            self.entry['font'] = 'verdana 20 bold'
        self.entry.update()
        self.entry.icursor(len(self.exp.get()))

    def equal(self, event=None):
        file = open('history.txt', 'a')
        file.write(self.exp.get() + '=')
        try:
            if isinstance(eval(self.exp.get()), float):
                self.exp.set("{0:.4f}".format(eval(self.exp.get())))
                if len(self.exp.get()) > 13:
                    self.entry['font'] = 'verdana 15 bold'
                else:
                    self.entry['font'] = 'verdana 20 bold'
                self.entry.update()
            else:
                self.exp.set(eval(self.exp.get()))
            self.entry.update()
        except Exception:
            self.exp.set("Error")
            self.entry.update()

        self.entry.icursor(len(self.exp.get()))

        file.write(self.exp.get() + '\n')

    def char_len(self,char):
        if not(char in self.btns):
            return False
        if len(self.exp.get()) >13:
            self.entry['font'] = 'verdana 15 bold'
        else:
            self.entry['font'] = 'verdana 20 bold'
        return True

class Scientific(Frame):
    def __init__(self, winmain, current):
        Frame.__init__(self, winmain)

        self.degrees = True

        topframe = Frame(self)
        topframe.pack()

        self.switch = Button(topframe, text='Regular',
                        command=lambda: current.show_calc(Regular,'Regular'),
                        width=8)
        self.switch.pack(pady=7, side=LEFT,padx=10)
        self.switch.bind('<Enter>',lambda event:self.entcolor(event,button=self.switch))
        self.switch.bind('<Leave>',lambda event:self.retcolor(event,'blue','white',button=self.switch))
        self.switch.configure(background='blue', foreground='white')

        self.file_btn = Button(topframe, text='History', command=current.history,
                          width=8)
        self.file_btn.pack(pady=7, side=LEFT,padx=10)
        self.file_btn.bind('<Enter>',lambda event:self.entcolor(event,button=self.file_btn))
        self.file_btn.bind('<Leave>',lambda event:self.retcolor(event,'green','white',button=self.file_btn))
        self.file_btn.configure(background='green', foreground='white')

        self.angle_btn = Button(topframe, text='Radians',
                                command=self.angle_button,width=8)
        self.angle_btn.pack(pady=7, side=LEFT,padx=10)
        self.angle_btn.bind('<Enter>',lambda event:self.entcolor(event,button=self.angle_btn))
        self.angle_btn.bind('<Leave>',lambda event:self.retcolor(event,'brown','white',button=self.angle_btn))
        self.angle_btn.configure(background='brown', foreground='white')

        self.mode_btn = Button(topframe, text='Sci. Notation',
                               command=self.mode,width=10)
        self.mode_btn.pack(pady=7, side=LEFT,padx=10)
        self.mode_btn.bind('<Enter>',lambda event:self.entcolor(event,button=self.mode_btn))
        self.mode_btn.bind('<Leave>',lambda event:self.retcolor(event,'black','white',button=self.mode_btn))
        self.mode_btn.configure(background='black', foreground='white')
        self.normal = True

        self.btns = ['1', '2', '3', '÷', 'AC', '4', '5', '6', 'x', '←', '7', '8', '9',
                '+', '=', '0', '.', 'x²', '-', 'x³', 'log(', '%', '√x', 'xⁿ', 'x!', 'sin(', 'cos(',
                'tan(', 'eⁿ', '(', 'π', 'sin⁻¹(', 'cos⁻¹(', 'tan⁻¹(', ')']

        self.exp = StringVar()
        self.butn=[]

        self.exp.set("")

        entframe = Frame(self)
        entframe.pack(fill=X)

        self.entry = Entry(entframe, textvariable=self.exp, justify=RIGHT,
                           font="verdana 20 bold",validate='key',
                           validatecommand=(self.register(self.char_len),'%S'))
        self.entry.pack(pady=10, padx=10)
        self.entry.bind('<KP_Enter>', self.equal)
        self.entry.bind('<Return>', self.equal)
        self.entry.bind('<Escape>', self.clear)
        #self.entry.icursor(1)
        self.entry.focus()

        row, column = 0, 0
        btnframe = Frame(self)
        btnframe.pack()

        for btn,i in zip(self.btns,range(35)):
            if btn == '4' or btn == '7' or btn == '0' or btn == 'log(' or btn == 'sin(' or btn == 'π':
                row += 1
                column = 0

            if btn == 'AC':
                self.butn.append( Button(btnframe, text=btn, height=3, width=7, command=self.clear))
                self.butn[i].grid(row=row, column=column, pady=1, padx=2)
                self.butn[i].bind('<Enter>',lambda event:self.entcolor(event))
                self.butn[i].bind('<Leave>',lambda event:self.retcolor(event,'yellow'))
                self.butn[i].configure(background="yellow")
                column += 1

            elif btn == '←':
                self.butn.append( Button(btnframe, text=btn, height=3, width=7, command=self.delete))
                self.butn[i].grid(row=row, column=column, pady=1, padx=2)
                self.butn[i].bind('<Enter>',lambda event:self.entcolor(event))
                self.butn[i].bind('<Leave>',lambda event:self.retcolor(event,'red'))
                self.butn[i].configure(background="red")
                column += 1

            elif btn == '=':
                self.butn.append( Button(btnframe, text=btn, height=3, width=7, command=self.equal))
                self.butn[i].grid(row=row, column=column, pady=1, padx=2)
                self.butn[i].bind('<Enter>',lambda event:self.entcolor(event))
                self.butn[i].bind('<Leave>',lambda event:self.retcolor(event,'yellow'))
                self.butn[i].configure(background="yellow")
                column += 1

            elif btn == '+' or btn == '-' or btn == 'x' or btn == '÷':
                self.butn.append( Button(btnframe, text=btn, height=3, width=7,
                              command=lambda char=btn: self.addch(char)))
                self.butn[i].grid(row=row, column=column, pady=1, padx=2)
                self.butn[i].configure(background="orange")
                self.butn[i].bind('<Enter>',lambda event:self.entcolor(event))
                self.butn[i].bind('<Leave>',lambda event:self.retcolor(event,'orange'))
                column += 1

            elif btn.isdigit():
                self.butn.append( Button(btnframe, text=btn, height=3, width=7,
                              command=lambda char=btn: self.addch(char)))
                self.butn[i].grid(row=row, column=column, pady=1, padx=2)
                self.butn[i].configure(background="sky blue")
                self.butn[i].bind('<Enter>',lambda event:self.entcolor(event))
                self.butn[i].bind('<Leave>',lambda event:self.retcolor(event,'sky blue'))
                column += 1

            elif btn == 'x²':
                self.butn.append( Button(btnframe, text=btn, height=3, width=7,
                              command=lambda char='²': self.addch(char)))
                self.butn[i].grid(row=row, column=column, pady=1, padx=2)
                self.butn[i].configure(background="cyan")
                self.butn[i].bind('<Enter>',lambda event:self.entcolor(event))
                self.butn[i].bind('<Leave>',lambda event:self.retcolor(event,'cyan'))
                column += 1

            elif btn == 'xⁿ':
                self.butn.append( Button(btnframe, text=btn, height=3, width=7,
                              command=lambda char='^': self.addch(char)))
                self.butn[i].grid(row=row, column=column, pady=1, padx=2)
                self.butn[i].configure(background="cyan")
                self.butn[i].bind('<Enter>',lambda event:self.entcolor(event))
                self.butn[i].bind('<Leave>',lambda event:self.retcolor(event,'cyan'))
                column += 1

            elif btn == '√x':
                self.butn.append( Button(btnframe, text=btn, height=3, width=7,
                              command=lambda char='√(': self.addch(char)))
                self.butn[i].grid(row=row, column=column, pady=1, padx=2)
                self.butn[i].configure(background="cyan")
                self.butn[i].bind('<Enter>',lambda event:self.entcolor(event))
                self.butn[i].bind('<Leave>',lambda event:self.retcolor(event,'cyan'))
                column += 1

            elif btn == 'eⁿ':
                self.butn.append(  Button(btnframe, text=btn, height=3, width=7,
                              command=lambda char='e^': self.addch(char)))
                self.butn[i].grid(row=row, column=column, pady=1, padx=2)
                self.butn[i].configure(background="cyan")
                self.butn[i].bind('<Enter>',lambda event:self.entcolor(event))
                self.butn[i].bind('<Leave>',lambda event:self.retcolor(event,'cyan'))
                column += 1


            elif btn == 'x³':
                self.butn.append( Button(btnframe, text=btn, height=3, width=7,
                              command=lambda char='³': self.addch(char)))
                self.butn[i].grid(row=row, column=column, pady=1, padx=2)
                self.butn[i].configure(background="cyan")
                self.butn[i].bind('<Enter>',lambda event:self.entcolor(event))
                self.butn[i].bind('<Leave>',lambda event:self.retcolor(event,'cyan'))
                column += 1

            elif btn == 'x!':
                self.butn.append( Button(btnframe, text=btn, height=3, width=7,
                              command=lambda char='!': self.addch(char)))
                self.butn[i].grid(row=row, column=column, pady=1, padx=2)
                self.butn[i].configure(background="cyan")
                self.butn[i].bind('<Enter>',lambda event:self.entcolor(event))
                self.butn[i].bind('<Leave>',lambda event:self.retcolor(event,'cyan'))
                column += 1

            else:
                self.butn.append( Button(btnframe, text=btn, height=3, width=7,
                              command=lambda char=btn: self.addch(char)))
                self.butn[i].grid(row=row, column=column, pady=1, padx=2)
                self.butn[i].configure(background="cyan")
                self.butn[i].bind('<Enter>',lambda event:self.entcolor(event))
                self.butn[i].bind('<Leave>',lambda event:self.retcolor(event,'cyan'))
                column += 1

    def clear(self,event=None):
        self.exp.set("")

        self.entry.update()

    def delete(self):
        self.exp.set(self.exp.get()[0:-1])

        if len(self.exp.get()) > 17:
            self.entry['font'] = 'verdana 15 bold'
        else:
            self.entry['font'] = 'verdana 20 bold'
        self.entry.update()

    def addch(self, char):
        self.exp.set(self.exp.get() + str(char))

        if len(self.exp.get()) > 17:
            self.entry['font'] = 'verdana 15 bold'
        else:
            self.entry['font'] = 'verdana 20 bold'
        self.entry.update()
        self.entry.icursor(len(self.exp.get()))

    def equal(self,event=None):
        self.strexp = str(self.exp.get())
        if self.degrees:
            index = self.strexp.find('sin(')
            if index != -1:
                self.set_trig(index, 'sin')
            index = self.strexp.find('cos(')
            if index != -1:
                self.set_trig(index, 'cos')
            index = self.strexp.find('tan(')
            if index != -1:
                self.set_trig(index, 'tan')

        for i in range(self.strexp.count('!')):
            index = self.strexp.find('!')
            if index != -1:
                self.factorial(index)

        self.replace_char()

        self.chk_bracket()

        file = open('history.txt', 'a')
        file.write(self.exp.get() + '=')
        try:
            if self.strexp.find('tan(radians(90') != -1:
                raise Exception
            if isinstance(eval(self.strexp), float):
                self.exp.set("{0:.4f}".format(eval(self.strexp)))
                if len(self.exp.get()) > 17:
                    self.entry['font'] = 'verdana 15 bold'
                else:
                    self.entry['font'] = 'verdana 20 bold'

                self.notation()

                self.entry.update()
            else:
                if not self.normal:
                    self.exp.set(float(eval(self.strexp)))
                else:
                    self.exp.set(eval(self.strexp))

                if len(self.exp.get()) > 17:
                    self.entry['font'] = 'verdana 15 bold'
                else:
                    self.entry['font'] = 'verdana 20 bold'

                self.notation()

                self.entry.update()

        except Exception:
            self.exp.set("Error")
            self.entry.update()
        self.entry.icursor(len(self.exp.get()))

        file.write(self.exp.get() + '\n')

    def set_trig(self, index, name):

        self.strexp = self.strexp.replace(f'{name}(', f'{name}(radians(')
        opened, closed = 0, 0
        for i in range(index + 11, len(self.strexp)):
            if self.strexp[i] == '(':
                opened += 1
            elif self.strexp[i] == ')':
                closed += 1
            if opened == closed:
                self.strexp = self.strexp[:i] + ')' + self.strexp[i:]
                break

    def chk_bracket(self):
        opened, closed, previous = 0, 0, ""
        for char in self.strexp:
            if char == '(':
                opened += 1
                if previous.isdigit():
                    self.strexp = self.strexp[:self.strexp.find(char)] \
                                  + '*' + self.strexp[self.strexp.find(char):]
            elif char == ')':
                closed += 1
            previous = char

        if opened == closed:
            return
        else:
            self.strexp = self.strexp + ')' * (opened - closed)

    def replace_char(self):
        self.strexp = self.strexp.replace('÷', '/')
        self.strexp = self.strexp.replace('x', '*')
        self.strexp = self.strexp.replace('²', '**2')
        self.strexp = self.strexp.replace('³', '**3')
        self.strexp = self.strexp.replace('^', '**')
        self.strexp = self.strexp.replace('π', 'pi')
        if self.degrees:
            self.strexp = self.strexp.replace('sin⁻¹(', '180/pi*asin(')
            self.strexp = self.strexp.replace('cos⁻¹(', '180/pi*acos(')
            self.strexp = self.strexp.replace('tan⁻¹(', '180/pi*atan(')
        else:
            self.strexp = self.strexp.replace('sin⁻¹(', 'asin(')
            self.strexp = self.strexp.replace('cos⁻¹(', 'acos(')
            self.strexp = self.strexp.replace('tan⁻¹(', 'atan(')
        self.strexp = self.strexp.replace('√(', 'sqrt(')

    def factorial(self, index):
        str = self.strexp[:index]

        exp, i = False, -1
        for i in range(-1, -len(str), -1):
            if not str[i].isdigit():
                exp = True
                str = str[-len(str):i + 1] + 'factorial(' + str[i + 1:] + ')'
                break
        if not exp:
            str = str[-len(str):i + 1] + 'factorial(' + str[i + 1:] + ')'
        self.strexp = str + self.strexp[index + 1:]

    def angle_button(self):
        if self.degrees:
            self.degrees = False
            self.radians = True
            self.angle_btn['text'] = 'Degrees'
        else:
            self.degrees, self.radians = self.radians, self.degrees
            self.angle_btn['text'] = 'Radians'

    def mode(self):
        if self.normal:
            self.normal,self.sci=False,True
            self.mode_btn['text']='Normal'
        else:
            self.normal,self.sci=self.sci,self.normal
            self.mode_btn['text'] = 'Sci. Notation'

    def notation(self):
        if self.normal:
            pass
        else:
            exp = self.exp.get()
            exp=exp.split('.')
            if exp[0][0] == '-':
                exp = exp[0][0:2] + '.' + exp[0][2:len(exp[0])] + exp[1] + f'x10^{len(exp[0]) - 2}'
            else:
                exp = exp[0][0]+'.'+exp[0][1:len(exp[0])]+exp[1]+f'x10^{len(exp[0])-1}'
            self.exp.set(exp)

    def char_len(self,char):
        if not(char in self.btns):
            return False
        if len(self.exp.get()) > 17:
            self.entry['font'] = 'verdana 15 bold'
        else:
            self.entry['font'] = 'verdana 20 bold'
        return True

    def entcolor(self,event,button=False):
        if button:
            button.configure(background='white',fg='black')
        else:
            self.butn[self.btns.index(event.widget.cget('text'))].configure(background='white',fg='black')

    def retcolor(self,event,color,fg='black',button=False):
        if button:
             button.configure(background=color,fg=fg)
        else:
            self.butn[self.btns.index(event.widget.cget('text'))].configure(background=color,fg=fg)


class MainMenu:
    def __init__(self,parent):
        menu = Menu(parent)
        parent.config(menu=menu)
        submenu = Menu(menu, tearoff=0)
        menu.add_cascade(label='Mode', menu=submenu)
        #submenu.add_command(label="Scientific", command=lambda: parent.show_calc(Scientific, 'Scientific'))
        #submenu.add_separator()
        #submenu.add_command(label="Regular", command=lambda: parent.show_calc(Regular, 'Regular'))
        submenu.add_radiobutton(label="Regular", command=lambda: parent.show_calc(Regular, 'Regular'))
        submenu.add_radiobutton(label="Scientific", command=lambda: parent.show_calc(Scientific, 'Scientific'))


if __name__=='__main__':
    calc = Calc()
    calc.mainloop()
