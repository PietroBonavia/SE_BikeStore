from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def set_category(self):
        category = self._model.get_category()
        for c in category:
            self._view.dd_category.options.append(ft.dropdown.Option(c[1]))

        self._view.update()

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        # TODO
        self._model.G.clear()
        self._view.txt_risultato.controls.clear()
        category = self._model.get_category()
        id = ''
        for c in category:
            if c[1] == self._view.dd_category.value:
                id = c[0]
        self._model.build_graph(id, self._view.dp1.value, self._view.dp2.value)
        self._view.txt_risultato.controls.append(ft.Text(f'Date selezionate:'))
        self._view.txt_risultato.controls.append(ft.Text(f'Start date: {(self._view.dp1.value)}'))
        self._view.txt_risultato.controls.append(ft.Text(f'End date: {self._view.dp2.value}'))
        self._view.txt_risultato.controls.append(ft.Text(f'Numero di nodi {len(self._model.G.nodes)},'
                                                         f' Numero di archi {len(self._model.G.edges)}'))



        self._model.G.clear()
        self._view.update()

    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        # TODO
        category = self._model.get_category()

        id = ''
        for c in category:
            if c[1] == self._view.dd_category.value:
                id = c[0]
        best_prod = self._model.best_prodotti(id,self._view.dp1.value, self._view.dp2.value)
        print(len(best_prod))

        self._view.txt_risultato.controls.append(ft.Text(f'I cinque prodotti più venduti sono'))

        for p in best_prod:
            self._view.txt_risultato.controls.append(ft.Text(f'{p[0].product_name} - {p[0].model_year} with score {p[1]}'))

        self._view.update()

    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
