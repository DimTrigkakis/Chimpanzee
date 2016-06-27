# Proper usage of the chimp module from the main thread in an application
# Simply import the module, and construct the event listener
# If in need of dictionary names, just use get_all_names() to obtain the complete dictionaries for actions
import chimp


def custom(event):

    if hasattr(event, 'Ascii'):
        print("CUSTOM:", chr(event.Ascii), event.Message)
    else:
        print("CUSTOM:", event.Message)

# chimp.Chimp.get_all_names()
dict_mouse = {'mouse_middle_release': custom}
dict_keyboard = {'A_release': custom}

my_chimp = chimp.construct_event_listener(event=True, dict_mouse=dict_mouse, dict_keyboard=dict_keyboard)
# Signed ~ Bradley
