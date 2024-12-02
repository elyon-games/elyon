from dearpygui import core, simple

def button_callback(sender, data):
    core.set_value("output", "Bouton cliqué !")

with window("Exemple Dear PyGui"):
    core.add_button("Clique-moi", callback=button_callback)
    core.add_text("", source="output")

core.start_dearpygui()
