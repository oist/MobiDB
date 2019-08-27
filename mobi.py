from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty
from kivy.core.window import Window
import threading


class designWidget(Widget):
    text = StringProperty()
    color = ListProperty([0, 0, 0, 0])


    def __init__(self, **kwargs):
        super(designWidget, self).__init__(**kwargs)
        self.text = ''
        self.started = threading.Event()
        self.btn_mythread = threading.Thread(target=self.btn_thread)

    def begin(self):
        print("begin")
        self.started.set()

    def end(self):
        self.started.clear()
        print("finish")

    #Event thread of button
    def btnClicked_text(self):
        self.begin()
        self.btn_mythread.start()
        self.btn_mythread.join()
        self.end()

    def btn_thread(self):
        # Connecting to Uniplot
        from bioservices import UniProt
        service = UniProt()

        # Constructing a query
        query = self.ids["text_box"].text
        # Send the query to UniProt, and catch the search result in a variable.
        result = service.search("keyword:" + query)
        print(result)



class designApp(App):
    def __init__(self, **kwargs):
        super(designApp, self).__init__(**kwargs)



if __name__ == '__main__':
    Window.size = (400, 220)
    designApp().run()

