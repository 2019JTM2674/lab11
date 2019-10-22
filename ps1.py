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



#Establishing connection with user and database
mydb = pymysql.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="billing_mgmt"
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
    pass

class EmployeeScreen(Screen):
    pass

class CreateAccountScreen(Screen):
    pass

class ForgetScreen(Screen):
    pass
          
class ScreenManagement(ScreenManager):
    pass


presentation = Builder.load_file("my.kv")
    
# define class simplekivy
class Float_LayoutApp(App):
    def build(self):
        return presentation

if __name__ == "__main__":
#     Window.size = (1366, 768)
#     Window.fullscreen = True
    Float_LayoutApp().run()