from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

import requests

Window.clearcolor = (0.6, 0.6, 0.6, 1)


def komunikacja():
    response = requests.get('http://ormiel.pythonanywhere.com/api/Device/')

    if (response.status_code != requests.codes.ok):
        print('coś poszło nie tak')
    else:
        lista = response.json()
        #print(lista)
        return lista


bd_reci = komunikacja()


class MainScrollWindow(ScrollView):

    def __init__(self, **kwargs):
        super(MainScrollWindow, self).__init__(**kwargs)

        self.bt2 = Button(text='Connect', size_hint=(1, 0.2), on_press=self.press2)
        self.add_widget(self.bt2)

    def press2(self, event):

        self.remove_widget(self.bt2)
        self.add_widget(Gridlayout(size_hint=(1, None)))


class Box(BoxLayout):
    a = None
    b = None
    c = None
    d = None

    def __init__(self,  **kwargs):

        super(Box, self).__init__(**kwargs)

        self.add_widget(Label(text='[b]'+self.a+'[/b]', color=(0.2, 0.2, 0.7), markup=True))
        self.add_widget(Label(text=self.b, color=(0, 0, 0)))
        if self.c == 'True':
            self.st_lab = Label(text=self.c, color=(0, 1, 0))
        else:
            self.st_lab = Label(text=self.c, color=(1, 0, 0))
        self.add_widget(self.st_lab)
        self.add_widget(Button(text='On', on_press=self.update, color=(0, 1, 0), background_color=(0, 0.5, 0, 1)))
        self.add_widget(Button(text='Off', on_press=self.update1, color=(1, 0, 0), background_color=(0.5, 0, 0, 1)))
        self.dev_url = 'http://ormiel.pythonanywhere.com/api/Device/' + str(self.a) + '/'
        self.dev_id = self.a
        self.dev_name = self.b
        self.dev_status = self.c
        self.dev_slug = self.d

    def update(self, event):

        self.st_lab.text = "True"
        responce = requests.put(self.dev_url, json={"id": self.dev_id, "name": str(self.dev_name),
                                                    "slug": str(self.dev_slug), "status": True})
        self.st_lab.color = (0, 1, 0)

    def update1(self, event):
        self.st_lab.text = "False"
        response = requests.put(self.dev_url, json={"id": self.dev_id, "name": str(self.dev_name),
                                                    "slug": str(self.dev_slug), "status": False})
        self.st_lab.color = (1, 0, 0)


class Gridlayout(GridLayout):

    def __init__(self, **kwargs):
        super(Gridlayout, self).__init__(**kwargs)
        self.cols = 1
        response = requests.get('http://ormiel.pythonanywhere.com/api/Device/')
        lista = response.json()
        for i in range(len(lista)):
            Box.a = str(lista[i]['id'])
            Box.b = str(lista[i]['name'])
            Box.c = str(lista[i]['status'])
            Box.d = str(lista[i]['slug'])
            self.add_widget(Box())


class MainWindow(BoxLayout):

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        self.add_widget(Header())
        self.add_widget(MainScrollWindow())


class Header(BoxLayout):

    def __init__(self, **kwargs):
        super(Header, self).__init__(**kwargs)

        self.add_widget(Label(text="[b]Ormiel App[/b]", size_hint=(.6, 1), color=(0, 0, 0),
                              markup=True, font_size='40dp'))


class DesktopApp(App):

    def build(self):
        return MainWindow()


DesktopApp().run()
