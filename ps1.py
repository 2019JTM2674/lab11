# Import libary for kivy
import kivy 
from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen , FadeTransition
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import ObjectProperty
import pymysql
from getpass import getpass
from kivy.uix.floatlayout import FloatLayout 
from random import randint
from kivy.uix.popup import Popup
from datetime import datetime




now = datetime.now()
acc_num = ''
flag = ''

#Establishing connection with user and database
mydb = pymysql.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="bank_db"
)
#Setting up the cursorfrom kivy.uix.floatlayout import FloatLayout 
mycursor = mydb.cursor()

class Widgets(Widget):
    pass
        
class MainScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

#CustomerScreen for validation
class CustomerScreen(Screen):
    username = ObjectProperty(None)
    user_pass = ObjectProperty(None)
    def onuserbtn(self):
        try:
            mycursor.execute("select password from customer where name='%s'"%self.username.text)
            user_list = list(mycursor.fetchall())
            mycursor.execute("select account_no from customer where name='%s'"%self.username.text)
            new = list(mycursor.fetchall())
            global acc_num
            acc_num = str(new[0][0])
            print(acc_num)
            #print(emp_list)
            if str(user_list[0][0]) == self.user_pass.text:
                print("Login Sucessfull")
                self.user_pass.text = " "
                self.username.text = " "
                presentation.current = "select"
            else:
                invalidUser()
                presentation.current = "main"
                self.user_pass.text = " "
                self.username.text = " "
        except:
            presentation.current = "main"
            invalidUser()
            self.user_pass.text = " "
            self.username.text = " "

#EmployeeScreen to view customer account details
class EmployeeScreen(Screen):
    accdet = ObjectProperty(None)
    i=0
    def onaccdet(self):
        mycursor.execute("select * from customer")
        acc_list = list(mycursor.fetchall())
        for cus in acc_list:
            for i in cus:
                #print(i)
                self.accdet.text = self.accdet.text + str(i) +'  '
            self.accdet.text = self.accdet.text +'\n'

#UpdateScreen for updating details
class UpdateScreen(Screen):
    uadd = ObjectProperty(None)
    umob = ObjectProperty(None)
    udob = ObjectProperty(None)
    uacc = ObjectProperty(None)
    def onUaddSubmitBtn(self):
        try:
            mycursor.execute("update customer set address='%s' where account_no = '%s'"%(self.uadd.text,self.uacc.text))
            mycursor.execute("update customer set mobile_no = '%s' where account_no = '%s'"%(self.umob.text,self.uacc.text))
            mycursor.execute("update customer set dob= '%s' where account_no = '%s'"%(self.udob.text,self.uacc.text))
            mydb.commit()
            content = "Details of AccNo."+str(self.uacc.text)+"\nare successfully updated on\n"+str(now)
            pop = Popup(title='Updte Details',
                  content=Label(text=content),
                  size_hint=(None, None), size=(400, 400))
            pop.open()
            self.uadd.text = ""
            self.umob.text = ""
            self.udob.text=" "
            self.uacc.text=""
            presentation.current = 'main'
        except:
            pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid data.'),
                  size_hint=(None, None), size=(400, 400))
            pop.open()


#CreateAccountScreen to create account
class CreateAccountScreen(Screen):
    custName = ObjectProperty(None)
    dob = ObjectProperty(None)
    address = ObjectProperty(None)
    country = ObjectProperty(None)
    bank = ObjectProperty(None)
    mobile = ObjectProperty(None)

    def onSubmitBtn(self):
        #print(self.custName.text,"\n",self.bank.text)
        try:
            mycursor.execute("Insert into customer (name,dob,address,country,bank,mobile_no) values ('%s','%s','%s','%s','%s','%s')"%(self.custName.text,self.dob.text,self.address.text,self.country.text,self.bank.text,self.mobile.text))
            mydb.commit()
            mycursor.execute("select account_no, bank from customer where name='%s'"%self.custName.text)
            select_list = list(mycursor.fetchall())
            #print(select_list[0][0],select_list[0][1])
            success(select_list[0][0],select_list[0][1])
            self.custName.text = ""
            self.dob.text = ""
            self.address.text = ""
            self.country.text = ""
            self.bank.text = ""
            self.mobile.text= ""
        except:
            invalidUser()
            self.custName.text = ""

# For forget password
class ForgetScreen(Screen):
    global rand_num
    rand_num = randint(1000,9999)
    fgname = ObjectProperty(None)
    fgacc = ObjectProperty(None)
    otp = ObjectProperty(None)

    def onotp(self):
        
        content = "OTP for forget password is:"+str(rand_num)
        pop = Popup(title='OTP',
                    content=Label(text=content),
                    size_hint=(None, None), size=(400, 400))
        pop.open()
    def forgetbtn(self):
        
        global for_accno
        for_accno = self.fgacc.text
        #print(for_accno)
        if self.otp.text == str(rand_num) :
            presentation.current = 'forpass'
        else:
            invalidUser()
            presentation.current = 'forpass'

#for resetting password
class ForgetPassScreen(Screen):
    forpassword = ObjectProperty(None)
    
    def onnewpass(self):
        print(for_accno)
        mycursor.execute("update customer set password='%s' where account_no=%d"%(self.forpassword.text,int(for_accno)))
        mydb.commit()
        content = "Password Changed Successfully"
        pop = Popup(title='Password Change',
                    content=Label(text=content),
                    size_hint=(None, None), size=(400, 400))
        pop.open()
        presentation.current = 'Customer'
    

#For customer to select option
class SelectOptionScreen(Screen):
    bal = ObjectProperty(None)
    five = ObjectProperty(None)
    k=0
    p=''
    #print(acc_num)
    def onbal(self,*args):
        mycursor.execute("select max(id) from balance where acc_no='%s'"%str(acc_num))
        max_id = list(mycursor.fetchall())
        k=max_id[0][0]
        mycursor.execute("select updated_balance from balance where id=%d"%k)
        cur_bal = list(mycursor.fetchall())
        p = str(cur_bal[0][0])
        #print(p)
        self.bal.text = self.bal.text+ "RS"+ p

    def onfive(self):
        mycursor.execute("select * from balance where acc_no = '%s' order by id desc limit 5"%str(acc_num))
        five_list = list(mycursor.fetchall())
        for t in five_list:
            for i in t:
                #print(i)
                self.five.text = self.five.text + str(i) +'  '
            self.five.text = self.five.text +'\n'
    def onback(self):
        self.bal.text = ' ' 
        self.five.text = ' '
    
    def ondelete(self):
        try:
            mycursor.execute("delete from customer where account_no=%d"%int(acc_num))
            mydb.commit()
            content = "Your Account is deleted\n"+str(acc_num)
            pop = Popup(title='Delete Account',
                    content=Label(text=content),
                    size_hint=(None, None), size=(400, 400))
            pop.open()
            presentation.current = 'main'
        except:
            content = "You doesn't have account in this bank"
            pop = Popup(title='Delete Account',
                    content=Label(text=content),
                    size_hint=(None, None), size=(400, 400))
            pop.open()
            presentation.current = 'main'

#To transfer money
class MoneyTransferScreen(Screen):
    tran_acc = ObjectProperty(None)
    tran_mob = ObjectProperty(None)
    tran_name = ObjectProperty(None)
    tran_amt = ObjectProperty(None)
    def onClickMT(self):
        mycursor.execute("select name,mobile_no from customer where account_no=%d"%int(self.tran_acc.text))
        tran_list = list(mycursor.fetchall())
        self.tran_name.text = self.tran_name.text+str(tran_list[0][0])
        self.tran_mob.text = self.tran_mob.text+str(tran_list[0][1])
    def onTransfer(self):
        amt = int(self.tran_amt.text)
        mycursor.execute("select updated_balance from balance where acc_no='%s'"%self.tran_acc.text)
        q_list = list(mycursor.fetchall())
        
        amt = amt+int(q_list[0][0])
        #print(amt)
        mycursor.execute("Insert into balance (acc_no,cur_balance,debit,credit,updated_balance) values ('%s','%s','%s','%s','%s')"%(self.tran_acc.text,str(q_list[0][0]),'0',self.tran_amt.text,str(amt)))
        mycursor.execute("select updated_balance from balance where acc_no='%s'"%str(acc_num))
        a_list = list(mycursor.fetchall())
        #print(a_list)
        u_amt = int(a_list[len(a_list)-1][0])-int(self.tran_amt.text)
        #print(u_amt)
        mycursor.execute("Insert into balance (acc_no,cur_balance,debit,credit,updated_balance) values ('%s','%s','%s','%s','%s')"%(str(acc_num),str(a_list[len(a_list)-1][0]),self.tran_amt.text,'0',str(u_amt)))
        mydb.commit()
        content = "Amount Transfered successfully on\n"+str(now)
        pop = Popup(title='Alert',
                  content=Label(text=content),
                  size_hint=(None, None), size=(400, 400))
        pop.open()
        presentation.current = 'main'

class SelectBankScreen(Screen):
    pass

class EmployeeLoginScreen(Screen):
    empname = ObjectProperty(None)
    emp_pass = ObjectProperty(None)
    def onEmpSubmitBtn(self):
        try:
            mycursor.execute("select password from employee where user_id='%s'"%self.empname.text)
            emp_list = list(mycursor.fetchall())
            #print(emp_list)
            if str(emp_list[0][0]) == self.emp_pass.text:
                #print("Login Sucessfull")
                self.empname.text = ""
                self.emp_pass.text = " "
                presentation.current = "Employee"
            else:
                invalidUser()
                self.empname.text = ""
                self.emp_pass.text = " "
                presentation.current = "main"
        except:
            invalidUser()
            self.empname.text = ""
            self.emp_pass.text = " "
            presentation.current = "main"

class ScreenManagement(ScreenManager):
    pass


#Popup after success
def success(acc,b):

    content = "You are successfully registered for\n"+str(b)+"with \naccount number "+str(acc)
    pop = Popup(title='Successful Registration',
                  content=Label(text=content),
                  size_hint=(None, None), size=(400, 400))
    pop.open()

#Popup after failure
def invalidUser():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


presentation = Builder.load_file("my.kv")
    
# define class simplekivy
class Float_LayoutApp(App):
    def build(self):
        return presentation

if __name__ == "__main__":
#     Window.size = (1366, 768)
#     Window.fullscreen = True
    Float_LayoutApp().run()
    #global acc_num