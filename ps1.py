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
import random 
from kivy.uix.popup import Popup



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

class CustomerScreen(Screen):
    username = ObjectProperty(None)
    user_pass = ObjectProperty(None)
    def onuserbtn(self):
        mycursor.execute("select password from customer where name='%s'"%self.username.text)
        user_list = list(mycursor.fetchall())
        #print(emp_list)
        try:
            if str(user_list[0][0]) == self.user_pass.text:
                #print("Login Sucessfull")
                self.user_pass.text = " "
                self.username.text = " "
                presentation.current = "main"
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


class EmployeeScreen(Screen):
    pass

class UpdateScreen(Screen):
    uadd = ObjectProperty(None)
    umob = ObjectProperty(None)
    udob = ObjectProperty(None)
    uacc = ObjectProperty(None)
    def onUaddSubmitBtn(self):
        try:
            mycursor.execute("update customer set address=case when address is not null then '%s' else address End where account_no = '%s'"%(self.uadd.text,self.uacc.text))
            mydb.commit()
        except:
            invalidUser()

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


class ForgetScreen(Screen):
    
    pass

class SelectOptionScreen(Screen):
    pass

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

def success(acc,b):

    content = "You are successfully registered for\n"+str(b)+"with \naccount number "+str(acc)
    pop = Popup(title='Successful Registration',
                  content=Label(text=content),
                  size_hint=(None, None), size=(400, 400))
    pop.open()

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