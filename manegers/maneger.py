from dal.dal import Dal
from ui.menu import Menu

class Maneger:

    def __init__(self):
        self.model = None
        self.suggestions=None


    def run(self):
        running=True

        while running:
            user_selecrion=Menu.show_menu()

            if user_selecrion=="1":


                # need to build the option to select specific data from our local data in the mnu class

                raw_data=Dal.load_data("../data")






    def handle_raw_df(self):
        pass



mangger=Maneger()
mangger.run()