import kivy
import pygame

import database_functions as dbf

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup

kivy.require('1.9.1')

#arquivo '.kv' feito no builder
Builder.load_string("""
#: import CheckBox kivy.uix.checkbox

<SucessPopup>:
    size_hint: .7, .7
    auto_dismiss: False
    title: "Sucess"
    BoxLayout:
        orientation: "vertical"
        Label:
            color: 1, 1, 1, 1
            text: root.label_text
        Button:
            text: "Close"
            on_press: root.dismiss()

<FailPopup>:
    size_hint: .7, .7
    auto_dismiss: False
    title: "Failure"
    BoxLayout:
        orientation: "vertical"
        Label:
            color: 1, 1, 1, 1
            text: root.label_text
        Button:
            text: "Close"
            on_press: root.dismiss()

<ResultsPopup>:
    auto_dismiss: False
    title: "Resultados"
    BoxLayout:
        orientation: "vertical"
        Label:
            color: 1, 1, 1, 1
            text: root.label_text
        Button:
            text: "Close"
            on_press: root.on_press_dismiss()

<ScreenOne>:
    BoxLayout:
        orientation: "vertical"
        Label:
            color: 0, 0, 0, 1
            text: "Hub"
        Button:
            text: "Add"
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_two'
        Button:
            text: "Search"
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_three'
        Button:
            text: "Delete"
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_four'
        Button:
            text: "Update"
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_five'

<ScreenTwo>:
    name_text_input: input_nome
    author_one_input: input_autorone
    authon_two_input: input_autortwo
    genre_input_one: input_genre_one
    genre_input_two: input_genre_two
    lent_input: input_spinner
    vol_num_input: input_numberofvol
    lenttowho_input: input_lenttowho
    BoxLayout:
        orientation: "vertical"
        padding: 10
        spacing: 10
        Label:
            color: 0, 0, 0, 1
            text: "Adicionar Entrada"
        BoxLayout:
            orientation: "horizontal"
            Label:
                color: 0, 0, 0, 1
                text: "Nome*: "
            TextInput:
                id: input_nome
                font_size: 32
        BoxLayout:
            orientation: "horizontal"
            Label:
                color: 0, 0, 0, 1
                text: "Autor 1*: "
            TextInput:
                id: input_autorone
                font_size: 32
        BoxLayout:
            orientation: "horizontal"
            Label:
                color: 0, 0, 0, 1
                text: "Autor 2: "
            TextInput:
                id: input_autortwo
                font_size: 32
        BoxLayout:
            orientation: "horizontal"
            Label:
                color: 0, 0, 0, 1
                text: "Genero 1*: "
            TextInput:
                id: input_genre_one
                font_size: 32
        BoxLayout:
            orientation: "horizontal"
            Label:
                color: 0, 0, 0, 1
                text: "Genero 2*: "
            TextInput:
                id: input_genre_two
                font_size: 32

        BoxLayout:
            orientation: "horizontal"
            Label:
                color: 0, 0, 0, 1
                text: "Emprestado*: "
            Spinner:
                text: "False"
                values: ["False", "True"]
                id: input_spinner
                on_text: root.spinner_clicked(input_spinner.text)
            Label:
                color: 0, 0, 0, 1
                text: "Emprestado a: "
            TextInput:
                id: input_lenttowho
                font_size: 32

        BoxLayout:
            orientation: "horizontal"
            Label:
                color: 0, 0, 0, 1
                text: "Volume: "
            TextInput:
                id: input_numberofvol
                font_size: 32
        BoxLayout:
            orientation: "horizontal"
            Button:
                text: "Add Manga"
                on_press: root.add_manga()
            Button:
                text: "Add Livro"
                on_press: root.add_book()
            Button:
                text: "Add Graphic Novel"
                on_press: root.add_novel()
            Button:
                text: "Voltar"
                on_press:
                    root.manager.transition.direction = 'left'
                    root.manager.transition.duration = 1
                    root.manager.current = 'screen_one'

<ScreenThree>:
    search_input: input_search
    BoxLayout:
        orientation: "vertical"
        padding: 10
        spacing: 10
        Label:
            color: 0, 0, 0, 1
            text: "Pesquisar Entradas"
        TextInput:
            id: input_search
            font_size: 32
        Label:
            color: 0, 0, 0, 1
            text: "Escolha a opcao de pesquisa"
        BoxLayout:
            orientation: "horizontal"
            Label:
                color: 0, 0, 0, 1
                text: "Autor"
            CheckBox:
                group: "search_opt"
                value: root.opt1
                on_active: root.search_aut(self, self.active)

            Label:
                color: 0, 0, 0, 1
                text: "Titulo"
            CheckBox:
                group: "search_opt"
                value: root.opt2
                on_active: root.search_tit(self, self.active)
            Label:
                color: 0, 0, 0, 1
                text: "Genero"
            CheckBox:
                group: "search_opt"
                value: root.opt3
                on_active: root.search_genre(self, self.active)

        BoxLayout:
            orientation: 'horizontal'
            padding: 10
            spacing: 10
            Button:
                text: "Voltar"
                on_press:
                    root.manager.transition.direction = 'left'
                    root.manager.transition.duration = 1
                    root.manager.current = 'screen_one'

<ScreenFour>:
    del_input_title: input_del_title
    del_input_volume: input_del_volume
    BoxLayout:
        orientation: "vertical"
        padding: 10
        spacing: 10
        Label:
            color: 0, 0, 0, 1
            text: "Deletar Entrada"
        Label:
            color: 0, 0, 0, 1
            text: "Para volumes unicos, digite 0 na aba 'volume'"
        BoxLayout:
            orientation: "horizontal"
            Label:
                color: 0, 0, 0, 1
                text: "Titulo"
            TextInput:
                id: input_del_title
                font_size: 32
        BoxLayout:
            orientation: "horizontal"
            Label:
                color: 0, 0, 0, 1
                text: "Volume"
            TextInput:
                id: input_del_volume
                font_size: 32
        BoxLayout:
            orientation: 'horizontal'
            padding: 10
            spacing: 10
            Button:
                text: "Deletar o item"
                on_press: root.del_one()
            Button:
                text: "Voltar"
                on_press:
                    root.manager.transition.direction = 'left'
                    root.manager.transition.duration = 1
                    root.manager.current = 'screen_one'

<ScreenFive>:
    title_text_input: input_updt_title
    vol_text_input: input_updt_vol
    lent_text_input: input_spinner
    lentw_text_input: input_updt_lentw
    BoxLayout:
        orientation: "vertical"
        Label:
            color: 0, 0, 0, 1
            text: "Atualizar Entrada"
        BoxLayout:
            orientation: "horizontal"
            Label:
                color: 0, 0, 0, 1
                text: "Titulo*"
            TextInput:
                id: input_updt_title
                font_size: 32
        BoxLayout:
            orientation: "horizontal"
            Label:
                color: 0, 0, 0, 1
                text: "Volume*"
            TextInput:
                id: input_updt_vol
                font_size: 32
        BoxLayout:
            orientation: "horizontal"
            Label:
                color: 0, 0, 0, 1
                text: "Emprestado*"
            Spinner:
                text: "False"
                values: ["False", "True"]
                id: input_spinner
                on_text: root.spinner_clicked(input_spinner.text)
            Label:
                color: 0, 0, 0, 1
                text: "Emprestado para"
            TextInput:
                id: input_updt_lentw
                font_size: 32
        BoxLayout:
            orientation: "horizontal"
            Button:
                text: "Update"
                on_press: root.update()
            Button:
                text: "Voltar"
                on_press:
                    root.manager.transition.direction = 'left'
                    root.manager.transition.duration = 1
                    root.manager.current = 'screen_one'
""")

class SucessPopup(Popup):
    label_text = StringProperty('')

class FailPopup(Popup):
    label_text = StringProperty('')

class ResultsPopup(Popup):
    label_text = StringProperty('')

    def on_press_dismiss(self):
        self.label_text = ''
        self.dismiss()

class ScreenOne(Screen):
    dbf.CheckIfTableExists()

class ScreenTwo(Screen):
    name_input = StringProperty()
    author1_input = StringProperty()
    author2_input = StringProperty()
    genero_input_one = StringProperty()
    genero_input_two = StringProperty()
    emprestado_input = StringProperty()
    vol_input = StringProperty()
    emprestadoaq_input = StringProperty()


    def spinner_clicked(self, value):
        print("Spinner Value " + value)

    def add_manga(self):
        #comeco da criacao de my_dict
        my_dict = {'Name': '', 'Autor 1': '', 'Autor 2': '', 'Genre 1': '','Genre 2': '', 'Lent': 'False', 'Lent to who': '', 'Volume': 0}
        self.name_input = '' + self.name_text_input.text
        my_dict['Name'] = self.name_input.lower()
        self.author1_input = '' + self.author_one_input.text
        my_dict['Autor 1'] = self.author1_input.lower()
        self.author2_input = '' + self.authon_two_input.text
        my_dict['Autor 2'] = self.author2_input.lower()
        self.genero_input_one = '' + self.genre_input_one.text
        my_dict['Genre 1'] = self.genero_input_one.lower()
        self.genero_input_two = '' + self.genre_input_two.text
        my_dict['Genre 2'] = self.genero_input_two.lower()
        self.emprestado_input = '' + self.lent_input.text
        if self.emprestado_input.lower() == 'true':
            my_dict['Lent'] = 'True'
            self.emprestadoaq_input = '' + self.lenttowho_input.text
            my_dict['Lent to who'] = self.emprestadoaq_input.lower()
        else:
            my_dict['Lent'] = 'False'
            my_dict['Lent to who'] = 'None'

        self.vol_input = '' + self.vol_num_input.text
        my_dict['Volume'] = int(self.vol_input)
        #fim da criacao de my_dict

        #checa se a entrada ja existe, e se nao existe adiciona a database
        if dbf.EnryExists(my_dict['Name'], my_dict['Volume']) == False:
            dbf.InsertNewEntry(my_dict['Name'], 'manga', my_dict['Autor 1'], my_dict['Autor 2'], my_dict['Genre 1'], my_dict['Genre 2'],
                               my_dict['Lent'], my_dict['Lent to who'], my_dict['Volume'])
            #popup indicando sucesso
            win_popup = SucessPopup()
            win_popup.label_text = my_dict['Name'] + ' volume ' + str(my_dict['Volume']) + ' adicionado com sucesso.'
            win_popup.open()
        else:
            #popup indicando falha
            lose_popup = FailPopup()
            lose_popup.label_text = my_dict['Name'] + ' volume ' + str(my_dict['Volume']) + ' nao foi adicionado.\nA entrada ja existe.'
            lose_popup.open()

        # limpando as janelas de texto
        self.name_text_input.text = ''
        self.author_one_input.text = ''
        self.authon_two_input.text = ''
        self.genre_input_one.text = ''
        self.genre_input_two.text = ''
        self.lenttowho_input.text = ''
        self.vol_num_input.text = ''

    def add_book(self):
        # comeco da criacao de my_dict
        my_dict = {'Name': '', 'Autor 1': '', 'Autor 2': '', 'Genre 1': '', 'Genre 2': '', 'Lent': 'False',
                   'Lent to who': '', 'Volume': 0}
        self.name_input = '' + self.name_text_input.text
        my_dict['Name'] = self.name_input.lower()
        self.author1_input = '' + self.author_one_input.text
        my_dict['Autor 1'] = self.author1_input.lower()
        self.author2_input = '' + self.authon_two_input.text
        my_dict['Autor 2'] = self.author2_input.lower()
        self.genero_input_one = '' + self.genre_input_one.text
        my_dict['Genre 1'] = self.genero_input_one.lower()
        self.genero_input_two = '' + self.genre_input_two.text
        my_dict['Genre 2'] = self.genero_input_two.lower()
        self.emprestado_input = '' + self.lent_input.text
        if self.emprestado_input.lower() == 'true':
            my_dict['Lent'] = 'True'
            self.emprestadoaq_input = '' + self.lenttowho_input.text
            my_dict['Lent to who'] = self.emprestadoaq_input.lower()
        else:
            my_dict['Lent'] = 'False'
            my_dict['Lent to who'] = 'None'

        self.vol_input = '' + self.vol_num_input.text
        my_dict['Volume'] = 0
        # fim da criacao de my_dict

        #checa se a entrada ja existe, e se nao existe adiciona a database
        if dbf.EnryExists(my_dict['Name'], my_dict['Volume']) == False:
            dbf.InsertNewEntry(my_dict['Name'], 'livro', my_dict['Autor 1'], my_dict['Autor 2'], my_dict['Genre 1'],
                               my_dict['Genre 2'], my_dict['Lent'], my_dict['Lent to who'], my_dict['Volume'])
            #popup indicando que foi um sucesso
            win_popup = SucessPopup()
            win_popup.label_text = my_dict['Name'] + ' volume ' + str(my_dict['Volume']) + ' adicionado com sucesso.'
            win_popup.open()
        else:
            #popup indicando que falhou
            lose_popup = FailPopup()
            lose_popup.label_text = my_dict['Name'] + ' volume ' + str(my_dict['Volume']) + ' nao foi adicionado.\nA entrada ja existe.'
            lose_popup.open()
        # limpando as janelas de texto
        self.name_text_input.text = ''
        self.author_one_input.text = ''
        self.authon_two_input.text = ''
        self.genre_input_one.text = ''
        self.genre_input_two.text = ''
        self.lenttowho_input.text = ''
        self.vol_num_input.text = ''

    def add_novel(self):
        #comeco da criacao de my_dict
        my_dict = {'Name': '', 'Autor 1': '', 'Autor 2': '', 'Genre 1': '','Genre 2': '', 'Lent': 'False', 'Lent to who': '', 'Volume': 0}
        self.name_input = '' + self.name_text_input.text
        my_dict['Name'] = self.name_input.lower()
        self.author1_input = '' + self.author_one_input.text
        my_dict['Autor 1'] = self.author1_input.lower()
        self.author2_input = '' + self.authon_two_input.text
        my_dict['Autor 2'] = self.author2_input.lower()
        self.genero_input_one = '' + self.genre_input_one.text
        my_dict['Genre 1'] = self.genero_input_one.lower()
        self.genero_input_two = '' + self.genre_input_two.text
        my_dict['Genre 2'] = self.genero_input_two.lower()
        self.emprestado_input = '' + self.lent_input.text
        if self.emprestado_input.lower() == 'true':
            my_dict['Lent'] = 'True'
            self.emprestadoaq_input = '' + self.lenttowho_input.text
            my_dict['Lent to who'] = self.emprestadoaq_input.lower()
        else:
            my_dict['Lent'] = 'False'
            my_dict['Lent to who'] = 'None'

        self.vol_input = '' + self.vol_num_input.text
        my_dict['Volume'] = int(self.vol_input)
        #fim da criacao de my_dict

        #checa se a entrada ja existe, e se nao existe adiciona a database
        if dbf.EnryExists(my_dict['Name'], my_dict['Volume']) == False:
            dbf.InsertNewEntry(my_dict['Name'], 'graphic novel', my_dict['Autor 1'], my_dict['Autor 2'], my_dict['Genre 1'], my_dict['Genre 2'],
                               my_dict['Lent'], my_dict['Lent to who'], my_dict['Volume'])
            #popup indicando sucesso
            win_popup = SucessPopup()
            win_popup.label_text = my_dict['Name'] + ' volume ' + str(my_dict['Volume']) + ' adicionado com sucesso.'
            win_popup.open()
        else:
            #popup indicando falha
            lose_popup = FailPopup()
            lose_popup.label_text = my_dict['Name'] + ' volume ' + str(my_dict['Volume']) + ' nao foi adicionado.\nA entrada ja existe.'
            lose_popup.open()

        # limpando as janelas de texto
        self.name_text_input.text = ''
        self.author_one_input.text = ''
        self.authon_two_input.text = ''
        self.genre_input_one.text = ''
        self.genre_input_two.text = ''
        self.lenttowho_input.text = ''
        self.vol_num_input.text = ''

class ScreenThree(Screen):
    #1 - autor; 2 - autor; 3 - genre;
    opt1 = ObjectProperty(False)
    opt2 = ObjectProperty(False)
    opt3 = ObjectProperty(False)

    pesq_input = StringProperty()
    info = StringProperty()

    def search_aut(self, instance, value):
        self.pesq_input = '' + self.search_input.text
        entradas = dbf.SearchSimilarAutor(self.pesq_input.lower())
        self.info = ''
        for entrada in entradas:
            self.info = self.info + '' + str(entrada) + '\n'
        else:
            poopup = ResultsPopup()
            poopup.label_text = 'none'
            poopup.open()
            poopup.label_text = self.info
            self.search_input.text = ''

    def search_tit(self, instance, value):
        self.pesq_input = '' + self.search_input.text
        entradas = dbf.SearchSimilarTitles(self.pesq_input.lower())
        self.info = ''
        for entrada in entradas:
            self.info = self.info + '' + str(entrada) + '\n'
        else:
            poopup = ResultsPopup()
            poopup.label_text = 'none'
            poopup.open()
            poopup.label_text = self.info
            self.search_input.text = ''
        #popup com os resultados

    def search_genre(self, instance, value):
        self.pesq_input = '' + self.search_input.text
        entradas = dbf.SearchSimilarGenre(self.pesq_input.lower())
        self.info = ''
        for entrada in entradas:
            self.info = self.info + '' + str(entrada) + '\n'
        else:
            poopup = ResultsPopup()
            poopup.label_text = 'none'
            poopup.open()
            poopup.label_text = self.info
            self.search_input.text = ''
    #popup com os resultados

class ScreenFour(Screen):
    del_text_input = StringProperty()
    del_volm_input = StringProperty()
    def DeleteEntry(self):
        self.del_text_input = '' + self.del_input_title.text
        self.del_volm_input = '' + self.del_input_volume.text
        #checa a existencia da entrada que se deseja deletar na database e a deleta se ela existir
        if dbf.EnryExists(self.del_text_input.lower(), int(self.del_volm_input)) == True:
            dbf.DeleteEntry(self.del_text_input.lower(), int(self.del_volm_input))
            #popup indicando sucesso
            win_popup = SucessPopup()
            win_popup.label_text = self.del_text_input + ' volume ' + self.del_volm_input + ' deletado com sucesso.'
            win_popup.open()
        else:
            #popup indicando falha
            lose_popup = FailPopup()
            lose_popup.label_text = self.del_text_input + ' volume ' + self.del_volm_input + ' nao pode ser deletado.\nA entrada nao existe.'
            lose_popup.open()
        self.del_input_title.text = ''
        self.del_input_volume.text = ''

class ScreenFive(Screen):
    title_input = StringProperty()
    vol_input = StringProperty()
    lent_input = StringProperty()
    lentw_input = StringProperty()
    def spinner_clicked(self, value):
        print("Spinner Value " + value)

    def update(self):
        self.title_input = ('' + self.title_text_input.text).lower()
        self.vol_input = ('' + self.vol_text_input.text)
        self.lent_input = ('' + self.lent_text_input.text).lower()
        if self.lent_input == 'true':
            self.lent_input = 'True'
            self.lentw_input = ('' + self.lentw_text_input.text).lower()
        else:
            self.lent_input = 'False'
            self.lentw_input = 'None'
        if dbf.EnryExists(self.title_input, int(self.vol_input)) == True:
            dbf.UpdateEntry(self.title_input, int(self.vol_input), self.lent_input, self.lentw_input)
            popup = SucessPopup()
            popup.self.del_text_input + ' volume ' + self.del_volm_input + ' atualizado com sucesso.'
            popup.open()
        else:
            popup = FailPopup()
            popup.self.del_text_input + ' volume ' + self.del_volm_input + ' nao pode ser atualizado\nA entrada nao existe.'
            popup.open()
        self.title_text_input.text = ''
        self.vol_text_input.text = ''
        self.lentw_text_input.text = ''


screen_manager = ScreenManager()

screen_manager.add_widget(ScreenOne(name="screen_one"))
screen_manager.add_widget(ScreenTwo(name="screen_two"))
screen_manager.add_widget(ScreenThree(name="screen_three"))
screen_manager.add_widget(ScreenFour(name="screen_four"))
screen_manager.add_widget(ScreenFive(name="screen_five"))

class my_appApp(App):
    def build(self):
        Window.clearcolor = (0.5, 0.5, 0.5, 1)
        return screen_manager

myapp = my_appApp()
myapp.run()

