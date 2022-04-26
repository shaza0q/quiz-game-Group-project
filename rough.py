import json
from re import A
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.togglebutton import ToggleButton

# Builder.load_file('rough.kv')
a=0
class MyLayout(BoxLayout):
    def openquestion(self):
        f=open('questions.json')
        data=json.load(f)
        print(data['category1']['question'])
        global a
        self.ids.ques.text=data['category1']['question'][a]   
        self.ids.opt1.text=data['category1']['options'][a][0]
        self.ids.opt2.text=data['category1']['options'][a][1]
        self.ids.opt3.text=data['category1']['options'][a][2]
        self.ids.opt4.text=data['category1']['options'][a][3]
        a+=1

class rough(App):
    def build(self):
        return MyLayout()

if __name__=='__main__':
    rough().run()