import eel


@eel.expose
def hello():
    print("Hello world!")


eel.init("www")
eel.start("login.html")
