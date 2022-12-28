import tkinter as Tk
from tkinter import ttk
import sv_ttk
from i18n import _
kb_flag=0
widget=None
class KeyBoard(Tk.Toplevel):
    def __init__(self, currentWidget):
        super().__init__(width=1024, height=600, bg='white')
        self.geometry("1024x600")
        self.createPad(currentWidget)

    def createPad(self, currentWidget):
        global widget, kb_flag

        self.labelkey = Tk.LabelFrame(self, text=_("Input"), bg='white', fg="red", font="Times 25", borderwidth=0)
        self.labelkey.grid(column=0, row=7, sticky="nw", padx=0, pady=0, columnspan=13)
        self.entry_content = Tk.Label(self.labelkey, text=" ", fg="black", bg="white", font="Times 43")
        self.entry_content.grid(row=0, column=0, columnspan=13, padx=0, pady=5, sticky="sw")
        label1 = Tk.Label(self.labelkey, text=" ", bg='white', fg="white", font="Verdana 14")
        label1.grid(row=2, column=0, padx=0, pady=20, sticky="nw")
        text3 = currentWidget.get()
        self.entry_content.config(text=text3)
        self.Q = Tk.Button(self.labelkey, text='Q', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('Q' if kb_flag == 0 else 'q'))
        self.Q.grid(row=4, column=0, padx=0, pady=0, sticky="nw")

        self.W = Tk.Button(self.labelkey, text='W', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('W' if kb_flag == 0 else 'w'))
        self.W.grid(row=4, column=1, padx=0, pady=0, sticky="nw")

        self.E = Tk.Button(self.labelkey, text='E', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('E' if kb_flag == 0 else 'e'))
        self.E.grid(row=4, column=2, padx=0, pady=0, sticky="nw")

        self.R = Tk.Button(self.labelkey, text='R', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('R' if kb_flag == 0 else 'r'))
        self.R.grid(row=4, column=3, padx=0, pady=0, sticky="nw")

        self.T = Tk.Button(self.labelkey, text='T', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('T' if kb_flag == 0 else 't'))
        self.T.grid(row=4, column=4, padx=0, pady=0, sticky="nw")

        self.Y = Tk.Button(self.labelkey, text='Y', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('Y' if kb_flag == 0 else 'y'))
        self.Y.grid(row=4, column=5, padx=0, pady=0, sticky="nw")

        self.U = Tk.Button(self.labelkey, text='U', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('U' if kb_flag == 0 else 'u'))
        self.U.grid(row=4, column=6, padx=0, pady=0, sticky="nw")

        self.I = Tk.Button(self.labelkey, text='I', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('I' if kb_flag == 0 else 'i'))
        self.I.grid(row=4, column=7, padx=0, pady=0, sticky="nw")

        self.O = Tk.Button(self.labelkey, text='O', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('O' if kb_flag == 0 else 'o'))
        self.O.grid(row=4, column=8, padx=0, pady=0, sticky="nw")

        self.P = Tk.Button(self.labelkey, text='P', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('P' if kb_flag == 0 else 'p'))
        self.P.grid(row=4, column=9, padx=0, pady=0, sticky="nw")

        brk_left = Tk.Button(self.labelkey, text='[', width=5, height=4, font="Verdana 12", activebackground='blue',
                             command=lambda: self.press('['))
        brk_left.grid(row=4, column=10, padx=0, pady=0, sticky="nw")

        brk_right = Tk.Button(self.labelkey, text=']', width=5, height=4, font="Verdana 12", activebackground='blue',
                              command=lambda: self.press(']'))
        brk_right.grid(row=4, column=11, padx=0, pady=0, sticky="nw")

        straight_slash = Tk.Button(self.labelkey, text='|', width=5, height=4, font="Verdana 12",
                                   activebackground='blue', command=lambda: self.press('|'))
        straight_slash.grid(row=4, column=12, padx=0, pady=0)

        self.A = Tk.Button(self.labelkey, text='A', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('A' if kb_flag == 0 else 'a'))
        self.A.grid(row=5, column=0, padx=0, pady=0)

        self.S = Tk.Button(self.labelkey, text='S', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('S' if kb_flag == 0 else 's'))
        self.S.grid(row=5, column=1, padx=0, pady=0)

        self.D = Tk.Button(self.labelkey, text='D', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('D' if kb_flag == 0 else 'd'))
        self.D.grid(row=5, column=2, padx=0, pady=0)

        self.F = Tk.Button(self.labelkey, text='F', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('F' if kb_flag == 0 else 'f'))
        self.F.grid(row=5, column=3, padx=0, pady=0)

        self.G = Tk.Button(self.labelkey, text='G', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('G' if kb_flag == 0 else 'g'))
        self.G.grid(row=5, column=4, padx=0, pady=0)

        self.H = Tk.Button(self.labelkey, text='H', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('H' if kb_flag == 0 else 'h'))
        self.H.grid(row=5, column=5, padx=0, pady=0)

        self.J = Tk.Button(self.labelkey, text='J', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('J' if kb_flag == 0 else 'j'))
        self.J.grid(row=5, column=6, padx=0, pady=0)

        self.K = Tk.Button(self.labelkey, text='K', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('K' if kb_flag == 0 else 'k'))
        self.K.grid(row=5, column=7, padx=0, pady=0)

        self.L = Tk.Button(self.labelkey, text='L', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('L' if kb_flag == 0 else 'l'))
        self.L.grid(row=5, column=8, padx=0, pady=0)

        semicolon = Tk.Button(self.labelkey, text=';', width=5, height=4, font="Verdana 12", activebackground='blue',
                              command=lambda: self.press(';'))
        semicolon.grid(row=5, column=9, padx=0, pady=0)

        colon = Tk.Button(self.labelkey, text=':', width=5, height=4, font="Verdana 12", activebackground='blue',
                          command=lambda: self.press(':'))
        colon.grid(row=5, column=10, padx=0, pady=0)

        clear1 = Tk.Button(self.labelkey, text='Clear', width=13, height=4, font="Verdana 12", activebackground='blue',
                           command=self.clear)
        clear1.grid(row=5, column=11, columnspan=2, padx=0, pady=0)
        ##
        self.Z = Tk.Button(self.labelkey, text='Z', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('Z' if kb_flag == 0 else 'z'))
        self.Z.grid(row=6, column=0, padx=0, pady=0)

        self.X = Tk.Button(self.labelkey, text='X', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('X' if kb_flag == 0 else 'x'))
        self.X.grid(row=6, column=1, padx=0, pady=0)

        self.C = Tk.Button(self.labelkey, text='C', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('C' if kb_flag == 0 else 'c'))
        self.C.grid(row=6, column=2, padx=0, pady=0)

        self.V = Tk.Button(self.labelkey, text='V', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('V' if kb_flag == 0 else 'v'))
        self.V.grid(row=6, column=3, padx=0, pady=0)

        self.B = Tk.Button(self.labelkey, text='B', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('B' if kb_flag == 0 else 'b'))
        self.B.grid(row=6, column=4, padx=0, pady=0)

        self.N = Tk.Button(self.labelkey, text='N', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('N' if kb_flag == 0 else 'n'))
        self.N.grid(row=6, column=5, padx=0, pady=0)

        self.M = Tk.Button(self.labelkey, text='M', width=5, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda: self.press('M' if kb_flag == 0 else 'm'))
        self.M.grid(row=6, column=6, padx=0, pady=0)

        comma = Tk.Button(self.labelkey, text=',', width=5, height=4, font="Verdana 12", activebackground='blue',
                          command=lambda: self.press(','))
        comma.grid(row=6, column=7, padx=0, pady=0)

        dot = Tk.Button(self.labelkey, text='.', width=5, height=4, font="Verdana 12", activebackground='blue',
                        command=lambda: self.press('.'))
        dot.grid(row=6, column=8, padx=0, pady=0)

        quota_mark_left = Tk.Button(self.labelkey, text='(', width=5, height=4, font="Verdana 12",
                                    activebackground='blue', command=lambda: self.press('('))
        quota_mark_left.grid(row=6, column=9, padx=0, pady=0)

        quota_mark_right = Tk.Button(self.labelkey, text=')', width=5, height=4, font="Verdana 12",
                                     activebackground='blue', command=lambda: self.press(')'))
        quota_mark_right.grid(row=6, column=10, padx=0, pady=0)

        back_slash = Tk.Button(self.labelkey, text="\\", width=5, height=4, font="Verdana 12", activebackground='blue',
                               command=lambda: self.press('\\'))
        back_slash.grid(row=6, column=11, padx=0, pady=0)

        brk_nhon_left = Tk.Button(self.labelkey, text='{', width=5, height=4, font="Verdana 12",
                                  activebackground='blue', command=lambda: self.press('{'))
        brk_nhon_left.grid(row=6, column=12, padx=0, pady=0)

        # third line Button

        zero = Tk.Button(self.labelkey, text='0', width=5, height=4, font="Verdana 12", activebackground='blue',
                         command=lambda: self.press('0'))
        zero.grid(row=7, column=0, padx=0, pady=0)

        one = Tk.Button(self.labelkey, text='1', width=5, height=4, font="Verdana 12", activebackground='blue',
                        command=lambda: self.press('1'))
        one.grid(row=7, column=1, padx=0, pady=0)

        two = Tk.Button(self.labelkey, text='2', width=5, height=4, font="Verdana 12", activebackground='blue',
                        command=lambda: self.press('2'))
        two.grid(row=7, column=2, padx=0, pady=0)

        three = Tk.Button(self.labelkey, text='3', width=5, height=4, font="Verdana 12", activebackground='blue',
                          command=lambda: self.press('3'))
        three.grid(row=7, column=3, padx=0, pady=0)

        four = Tk.Button(self.labelkey, text='4', width=5, height=4, font="Verdana 12", activebackground='blue',
                         command=lambda: self.press('4'))
        four.grid(row=7, column=4, padx=0, pady=0)

        five = Tk.Button(self.labelkey, text='5', width=5, height=4, font="Verdana 12", activebackground='blue',
                         command=lambda: self.press('5'))
        five.grid(row=7, column=5, padx=0, pady=0)

        six = Tk.Button(self.labelkey, text='6', width=5, height=4, font="Verdana 12", activebackground='blue',
                        command=lambda: self.press('6'))
        six.grid(row=7, column=6, padx=0, pady=0)

        seven = Tk.Button(self.labelkey, text='7', width=5, height=4, font="Verdana 12", activebackground='blue',
                          command=lambda: self.press('7'))
        seven.grid(row=7, column=7, padx=0, pady=0)

        eight = Tk.Button(self.labelkey, text='8', width=5, height=4, font="Verdana 12", activebackground='blue',
                          command=lambda: self.press('8'))
        eight.grid(row=7, column=8, padx=0, pady=0)

        nine = Tk.Button(self.labelkey, text='9', width=5, height=4, font="Verdana 12", activebackground='blue',
                         command=lambda: self.press('9'))
        nine.grid(row=7, column=9, padx=0, pady=0)

        slash = Tk.Button(self.labelkey, text='/', width=5, height=4, font="Verdana 12", activebackground='blue',
                          command=lambda: self.press('/'))
        slash.grid(row=7, column=10, padx=0, pady=0)

        enter1 = Tk.Button(self.labelkey, text='Enter', width=13, height=4, font="Verdana 12", activebackground='blue',
                           command=lambda :self.close(currentWidget))
        enter1.grid(row=7, column=11, padx=0, columnspan=2, pady=0)
        ##

        cham_than = Tk.Button(self.labelkey, text='!', width=5, height=4, font="Verdana 12", activebackground='blue',
                              command=lambda: self.press('!'))
        cham_than.grid(row=8, column=0, padx=0, pady=0)

        acong = Tk.Button(self.labelkey, text='@', width=5, height=4, font="Verdana 12", activebackground='blue',
                          command=lambda: self.press('@'))
        acong.grid(row=8, column=1, padx=0, pady=0)

        thang = Tk.Button(self.labelkey, text='#', width=5, height=4, font="Verdana 12", activebackground='blue',
                          command=lambda: self.press('#'))
        thang.grid(row=8, column=2, padx=0, pady=0)

        dola = Tk.Button(self.labelkey, text='$', width=5, height=4, font="Verdana 12", activebackground='blue',
                         command=lambda: self.press('$'))
        dola.grid(row=8, column=3, padx=0, pady=0)

        phan_tram = Tk.Button(self.labelkey, text='%', width=5, height=4, font="Verdana 12", activebackground='blue',
                              command=lambda: self.press('%'))
        phan_tram.grid(row=8, column=4, padx=0, pady=0)

        space = Tk.Button(self.labelkey, text='Space', width=21, height=4, font="Verdana 12", activebackground='blue',
                          command=lambda: self.press(' '))
        space.grid(row=8, column=5, columnspan=3, padx=0, pady=0)

        brk_nhon_right = Tk.Button(self.labelkey, text='}', width=5, height=4, font="Verdana 12",
                                   activebackground='blue', command=lambda: self.press('}'))
        brk_nhon_right.grid(row=8, column=8, padx=0, pady=0)

        q_mark1 = Tk.Button(self.labelkey, text='-', width=5, height=4, font="Verdana 12", activebackground='blue',
                            command=lambda: self.press('-'))
        q_mark1.grid(row=8, column=9, padx=0, pady=0)

        nhay_don = Tk.Button(self.labelkey, text='\'', width=5, height=4, font="Verdana 12", activebackground='blue',
                             command=lambda: self.press('\''))
        nhay_don.grid(row=8, column=10, padx=0, pady=0)

        nhay_kep = Tk.Button(self.labelkey, text='\"', width=5, height=4, font="Verdana 12", activebackground='blue',
                             command=lambda: self.press('\"'))
        nhay_kep.grid(row=8, column=11, padx=0, pady=0)

        self.low_up = Tk.Button(self.labelkey, text='LO', width=5, height=4, font="Verdana 12", activebackground='blue',
                                command=self.change_low_up)
        self.low_up.grid(row=8, column=12, padx=0, pady=0)

    def close(self, currentWidget):
        self.update_content(currentWidget)
        try:
            self.destroy()
        except:
            pass

    def press(self, num):
        try:

            exp1 = self.entry_content.cget("text") + str(num)
            if len(exp1) > 23:
                exp1 = exp1[:23]
            self.entry_content.config(text=exp1)
        except Exception:
            pass

    def change_low_up(self):
        """ Change the kb_flag to change the lowercase and upercase of keyboard"""
        global kb_flag
        kb_flag = not kb_flag

        if kb_flag == 0:
            self.low_up.configure(text="LO")
            self.Q.configure(text='Q')
            self.W.configure(text='W')
            self.E.configure(text='E')
            self.R.configure(text='R')
            self.T.configure(text='T')
            self.Y.configure(text='Y')
            self.U.configure(text='U')
            self.I.configure(text='I')
            self.O.configure(text='O')
            self.P.configure(text='P')
            self.A.configure(text='A')
            self.S.configure(text='S')
            self.D.configure(text='D')
            self.F.configure(text='F')
            self.G.configure(text='G')
            self.H.configure(text='H')
            self.J.configure(text='J')
            self.K.configure(text='K')
            self.L.configure(text='L')
            self.Z.configure(text='Z')
            self.X.configure(text='X')
            self.C.configure(text='C')
            self.V.configure(text='V')
            self.B.configure(text='B')
            self.N.configure(text='N')
            self.M.configure(text='M')

        else:
            self.low_up.configure(text="UP")
            self.Q.configure(text='q')
            self.W.configure(text='w')
            self.E.configure(text='e')
            self.R.configure(text='r')
            self.T.configure(text='t')
            self.Y.configure(text='y')
            self.U.configure(text='u')
            self.I.configure(text='i')
            self.O.configure(text='o')
            self.P.configure(text='p')
            self.A.configure(text='a')
            self.S.configure(text='s')
            self.D.configure(text='d')
            self.F.configure(text='f')
            self.G.configure(text='g')
            self.H.configure(text='h')
            self.J.configure(text='j')
            self.K.configure(text='k')
            self.L.configure(text='l')
            self.Z.configure(text='z')
            self.X.configure(text='x')
            self.C.configure(text='c')
            self.V.configure(text='v')
            self.B.configure(text='b')
            self.N.configure(text='n')
            self.M.configure(text='m')

    # function clear button

    def clear(self):
        try:
            current_str = self.entry_content.cget("text")
            new_str = current_str[:len(current_str) - 1]
            self.entry_content.config(text=new_str)
        except Exception:
            pass

    def update_content(self, currentWidget):
        text1 = self.entry_content.cget("text")
        self.insert_to_widget(currentWidget, text1)

    def insert_to_widget(self, currentWidget, text2):
        currentWidget.delete(0, Tk.END)
        currentWidget.insert(0, text2)