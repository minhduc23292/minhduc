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
        self.attributes('-fullscreen', True)
        self.createPad(currentWidget)
        self.keystyle = ttk.Style()
        self.keystyle.configure('key.TButton', font=('Chakra Petch', 12), justify=Tk.CENTER)

    def createPad(self, currentWidget):
        global widget, kb_flag
        self.labelFrame = Tk.Frame(self, name="key", bd=1, bg='white', width=1024, height=145)
        self.labelFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.labelFrame.pack_propagate(0)

        self.keyFrame = Tk.Frame(self, name="key", bd=1, bg='white', width=1024, height=425)
        self.keyFrame.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.keyFrame.pack_propagate(0)
        
        self.labelkey1 = Tk.LabelFrame(self.labelFrame, text=_("Input"), bg='white', font=('Chakra Petch', 20), borderwidth=0)
        self.labelkey1.grid(column=0, row=7, sticky="nw", padx=0, pady=0)
        self.entry_content = Tk.Label(self.labelkey1, text=" ", fg="black", bg="white", font=('Chakra Petch', 40))
        self.entry_content.grid(row=0, column=0, columnspan=13, padx=0, pady=5, sticky="sw")
        labelkey2 = Tk.Label(self.labelkey1, text=" ", bg='white', fg="white")
        labelkey2.grid(row=2, column=0, padx=0, pady=10, sticky="nw")
        text3 = currentWidget.get()
        self.entry_content.configure(text=text3)

        self.Q = ttk.Button(self.keyFrame, text='Q', style="key.TButton",
                           command=lambda: self.press('Q' if kb_flag == 0 else 'q'))
        self.Q.place(x=15, y=196, height=70, width=70)
        # self.Q.grid()
        self.W = ttk.Button(self.keyFrame, text='W', style="key.TButton",
                           command=lambda: self.press('W' if kb_flag == 0 else 'w'))
        self.W.place(x=92, y=196, height=70, width=70)

        self.E = ttk.Button(self.keyFrame, text='E', style="key.TButton",
                           command=lambda: self.press('E' if kb_flag == 0 else 'e'))
        self.E.place(x=169, y=196, height=70, width=70)

        self.R = ttk.Button(self.keyFrame, text='R', style="key.TButton",
                           command=lambda: self.press('R' if kb_flag == 0 else 'r'))
        self.R.place(x=246, y=196, height=70, width=70)

        self.T = ttk.Button(self.keyFrame, text='T', style="key.TButton",
                           command=lambda: self.press('T' if kb_flag == 0 else 't'))
        self.T.place(x=323, y=196, height=70, width=70)

        self.Y = ttk.Button(self.keyFrame, text='Y', style="key.TButton",
                           command=lambda: self.press('Y' if kb_flag == 0 else 'y'))
        self.Y.place(x=400, y=196, height=70, width=70)

        self.U = ttk.Button(self.keyFrame, text='U', style="key.TButton",
                           command=lambda: self.press('U' if kb_flag == 0 else 'u'))
        self.U.place(x=477, y=196, height=70, width=70)

        self.I = ttk.Button(self.keyFrame, text='I', style="key.TButton",
                           command=lambda: self.press('I' if kb_flag == 0 else 'i'))
        self.I.place(x=554, y=196, height=70, width=70)

        self.O = ttk.Button(self.keyFrame, text='O', style="key.TButton",
                           command=lambda: self.press('O' if kb_flag == 0 else 'o'))
        self.O.place(x=631, y=196, height=70, width=70)

        self.P = ttk.Button(self.keyFrame, text='P', style="key.TButton",
                           command=lambda: self.press('P' if kb_flag == 0 else 'p'))
        self.P.place(x=708, y=196, height=70, width=70)

        brk_left = ttk.Button(self.keyFrame, text='[', style="key.TButton",
                             command=lambda: self.press('['))
        brk_left.place(x=785, y=196, height=70, width=70)

        brk_right = ttk.Button(self.keyFrame, text=']', style="key.TButton",
                              command=lambda: self.press(']'))
        brk_right.place(x=862, y=196, height=70, width=70)

        straight_slash = ttk.Button(self.keyFrame, text='|', style="key.TButton",
                            command=lambda: self.press('|'))
        straight_slash.place(x=939, y=196, height=70, width=70)

        self.A = ttk.Button(self.keyFrame, text='A', style="key.TButton",
                           command=lambda: self.press('A' if kb_flag == 0 else 'a'))
        self.A.place(x=15, y=274, height=70, width=70)

        self.S = ttk.Button(self.keyFrame, text='S', style="key.TButton",
                           command=lambda: self.press('S' if kb_flag == 0 else 's'))
        self.S.place(x=92, y=274, height=70, width=70)

        self.D = ttk.Button(self.keyFrame, text='D', style="key.TButton",
                           command=lambda: self.press('D' if kb_flag == 0 else 'd'))
        self.D.place(x=169, y=274, height=70, width=70)

        self.F = ttk.Button(self.keyFrame, text='F', style="key.TButton",
                           command=lambda: self.press('F' if kb_flag == 0 else 'f'))
        self.F.place(x=246, y=274, height=70, width=70)

        self.G = ttk.Button(self.keyFrame, text='G', style="key.TButton",
                           command=lambda: self.press('G' if kb_flag == 0 else 'g'))
        self.G.place(x=323, y=274, height=70, width=70)

        self.H = ttk.Button(self.keyFrame, text='H', style="key.TButton",
                           command=lambda: self.press('H' if kb_flag == 0 else 'h'))
        self.H.place(x=400, y=274, height=70, width=70)

        self.J = ttk.Button(self.keyFrame, text='J', style="key.TButton",
                           command=lambda: self.press('J' if kb_flag == 0 else 'j'))
        self.J.place(x=477, y=274, height=70, width=70)

        self.K = ttk.Button(self.keyFrame, text='K', style="key.TButton",
                           command=lambda: self.press('K' if kb_flag == 0 else 'k'))
        self.K.place(x=554, y=274, height=70, width=70)

        self.L = ttk.Button(self.keyFrame, text='L', style="key.TButton",
                           command=lambda: self.press('L' if kb_flag == 0 else 'l'))
        self.L.place(x=631, y=274, height=70, width=70)

        semicolon = ttk.Button(self.keyFrame, text=';', style="key.TButton",
                              command=lambda: self.press(';'))
        semicolon.place(x=708, y=274, height=70, width=70)

        colon = ttk.Button(self.keyFrame, text=':', style="key.TButton",
                          command=lambda: self.press(':'))
        colon.place(x=785, y=274, height=70, width=70)

        clear1 = ttk.Button(self.keyFrame, text='Clear', style="key.TButton",
                           command=self.clear)
        clear1.place(x=862, y=274, height=70, width=147)
        ##
        self.Z = ttk.Button(self.keyFrame, text='Z', style="key.TButton",
                           command=lambda: self.press('Z' if kb_flag == 0 else 'z'))
        self.Z.place(x=15, y=352, height=70, width=70)

        self.X = ttk.Button(self.keyFrame, text='X', style="key.TButton",
                           command=lambda: self.press('X' if kb_flag == 0 else 'x'))
        self.X.place(x=92, y=352, height=70, width=70)

        self.C = ttk.Button(self.keyFrame, text='C', style="key.TButton",
                           command=lambda: self.press('C' if kb_flag == 0 else 'c'))
        self.C.place(x=169, y=352, height=70, width=70)

        self.V = ttk.Button(self.keyFrame, text='V', style="key.TButton",
                           command=lambda: self.press('V' if kb_flag == 0 else 'v'))
        self.V.place(x=246, y=352, height=70, width=70)

        self.B = ttk.Button(self.keyFrame, text='B', style="key.TButton",
                           command=lambda: self.press('B' if kb_flag == 0 else 'b'))
        self.B.place(x=323, y=352, height=70, width=70)

        self.N = ttk.Button(self.keyFrame, text='N', style="key.TButton",
                           command=lambda: self.press('N' if kb_flag == 0 else 'n'))
        self.N.place(x=400, y=352, height=70, width=70)

        self.M = ttk.Button(self.keyFrame, text='M', style="key.TButton",
                           command=lambda: self.press('M' if kb_flag == 0 else 'm'))
        self.M.place(x=477, y=352, height=70, width=70)

        comma = ttk.Button(self.keyFrame, text=',', style="key.TButton",
                          command=lambda: self.press(','))
        comma.place(x=554, y=352, height=70, width=70)

        dot = ttk.Button(self.keyFrame, text='.', style="key.TButton",
                        command=lambda: self.press('.'))
        dot.place(x=631, y=352, height=70, width=70)

        quota_mark_left = ttk.Button(self.keyFrame, text='(', style="key.TButton",
                                    command=lambda: self.press('('))
        quota_mark_left.place(x=708, y=352, height=70, width=70)

        quota_mark_right = ttk.Button(self.keyFrame, text=')', style="key.TButton",
                                     command=lambda: self.press(')'))
        quota_mark_right.place(x=785, y=352, height=70, width=70)

        back_slash = ttk.Button(self.keyFrame, text="\\", style="key.TButton",
                               command=lambda: self.press('\\'))
        back_slash.place(x=862, y=352, height=70, width=70)

        brk_nhon_left = ttk.Button(self.keyFrame, text='{', style="key.TButton",
                            command=lambda: self.press('{'))
        brk_nhon_left.place(x=939, y=352, height=70, width=70)

        # third line Button

        zero = ttk.Button(self.keyFrame, text='0', style="key.TButton",
                         command=lambda: self.press('0'))
        zero.place(x=15, y=430, height=70, width=70)

        one = ttk.Button(self.keyFrame, text='1', style="key.TButton",
                        command=lambda: self.press('1'))
        one.place(x=92, y=430, height=70, width=70)

        two = ttk.Button(self.keyFrame, text='2', style="key.TButton",
                        command=lambda: self.press('2'))
        two.place(x=169, y=430, height=70, width=70)

        three = ttk.Button(self.keyFrame, text='3', style="key.TButton",
                          command=lambda: self.press('3'))
        three.place(x=246, y=430, height=70, width=70)

        four = ttk.Button(self.keyFrame, text='4', style="key.TButton",
                         command=lambda: self.press('4'))
        four.place(x=323, y=430, height=70, width=70)

        five = ttk.Button(self.keyFrame, text='5', style="key.TButton",
                         command=lambda: self.press('5'))
        five.place(x=400, y=430, height=70, width=70)

        six = ttk.Button(self.keyFrame, text='6', style="key.TButton",
                        command=lambda: self.press('6'))
        six.place(x=477, y=430, height=70, width=70)

        seven = ttk.Button(self.keyFrame, text='7', style="key.TButton",
                          command=lambda: self.press('7'))
        seven.place(x=554, y=430, height=70, width=70)

        eight = ttk.Button(self.keyFrame, text='8', style="key.TButton",
                          command=lambda: self.press('8'))
        eight.place(x=631, y=430, height=70, width=70)

        nine = ttk.Button(self.keyFrame, text='9', style="key.TButton",
                         command=lambda: self.press('9'))
        nine.place(x=708, y=430, height=70, width=70)

        slash = ttk.Button(self.keyFrame, text='/', style="key.TButton",
                          command=lambda: self.press('/'))
        slash.place(x=785, y=430, height=70, width=70)

        enter1 = ttk.Button(self.keyFrame, text='Enter', style="key.TButton",
                           command=lambda :self.close(currentWidget))
        enter1.place(x=862, y=430, height=70, width=147)
        ##

        cham_than = ttk.Button(self.keyFrame, text='!', style="key.TButton",
                              command=lambda: self.press('!'))
        cham_than.place(x=15, y=508, height=70, width=70)

        acong = ttk.Button(self.keyFrame, text='@', style="key.TButton",
                          command=lambda: self.press('@'))
        acong.place(x=92, y=508, height=70, width=70)

        thang = ttk.Button(self.keyFrame, text='#', style="key.TButton",
                          command=lambda: self.press('#'))
        thang.place(x=169, y=508, height=70, width=70)

        dola = ttk.Button(self.keyFrame, text='$', style="key.TButton",
                         command=lambda: self.press('$'))
        dola.place(x=246, y=508, height=70, width=70)

        phan_tram = ttk.Button(self.keyFrame, text='%', style="key.TButton",
                              command=lambda: self.press('%'))
        phan_tram.place(x=323, y=508, height=70, width=70)

        space = ttk.Button(self.keyFrame, text='Space', style="key.TButton",
                          command=lambda: self.press(' '))
        space.place(x=400, y=508, height=70, width=224)

        brk_nhon_right = ttk.Button(self.keyFrame, text='}',style="key.TButton",
                            command=lambda: self.press('}'))
        brk_nhon_right.place(x=631, y=508, height=70, width=70)

        q_mark1 = ttk.Button(self.keyFrame, text='-', style="key.TButton",
                            command=lambda: self.press('-'))
        q_mark1.place(x=708, y=508, height=70, width=70)

        nhay_don = ttk.Button(self.keyFrame, text='\'', style="key.TButton",
                             command=lambda: self.press('\''))
        nhay_don.place(x=785, y=508, height=70, width=70)

        nhay_kep = ttk.Button(self.keyFrame, text='\"', style="key.TButton",
                             command=lambda: self.press('\"'))
        nhay_kep.place(x=862, y=508, height=70, width=70)

        self.low_up = ttk.Button(self.keyFrame, text='LO', style="key.TButton",
                                command=self.change_low_up)
        self.low_up.place(x=939, y=508, height=70, width=70)

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