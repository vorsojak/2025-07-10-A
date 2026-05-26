import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._categoryValue = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        cat = self._categoryValue
        d1 = self._view._dp1.value
        d2 = self._view._dp2.value
        self._model.buildGraph(cat, d1, d2)
        self._view.txt_result.controls.append(
            ft.Text("Date selezionate:", color="orange")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"{self._view._dp1.value.date()}", color="orange")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"{self._view._dp2.value.date()}", color="orange")
        )
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato", color="orange"))
        n, edeges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {n}", color="orange")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {edeges}", color="orange")
        )
        self.fillDDProducts()
        self._view.update_page()

    def handleBestProdotti(self, e):
        self._view.txt_result.controls.clear()

        bestProd = self._model.getNodiPiuProfitt()
        self._view.txt_result.controls.append(
            ft.Text("Di seguito i prodotti più profittevoli")
        )
        for p in bestProd:
            self._view.txt_result.controls.append(ft.Text(f"{p[0]} - score: {p[1]}"))

        self._view.update_page()

    def handleCercaCammino(self, e):
        self._view.txt_result.controls.clear()

        lun = self._view._txtInLun.value
        try:
            lun = int(lun)
        except:
            self._view.txt_result.controls.append(
                ft.Text(
                    f"Attenzione! La lunghezza deve essere un numero intero",
                    color="red",
                )
            )
            self._view.update_page()
            return

        p1 = self._view._ddProdStart.value
        p2 = self._view._ddProdEnd.value
        if p1 is None or p2 is None:
            self._view.txt_result.controls.append(
                ft.Text(f"Attenzione! Scegliere entrambi i prodotti", color="red")
            )
            self._view.update_page()
            return

        bestPath, bestScore = self._model.getBestPath(
            lun, self._productValueStart, self._productValueEnd
        )

        if len(bestPath) == 0:
            self._view.txt_result.controls.append(
                ft.Text(f"Non ho trovato un cammino tra {p1} e {p2}")
            )
            self._view.update_page()
            return
        for p in bestPath:
            self._view.txt_result.controls.append(ft.Text(p))
        self._view.txt_result.controls.append(ft.Text(f"Score: {bestScore}"))
        self._view.update_page()

    def fillDDCategories(self):
        categories = self._model.getCategories()
        categorieDDoptions = list(
            map(
                lambda x: ft.dropdown.Option(
                    data=x, key=x.category_name, on_click=self.choice_dd_cat
                ),
                categories,
            )
        )

        self._view._ddcategory.options = categorieDDoptions
        self._view.update_page()

    def fillDDProducts(self):
        allProdotti = self._model.getProdotti()
        allProdotti.sort(key=lambda x: x.product_name)
        prodottiStartDDoptions = list(
            map(
                lambda x: ft.dropdown.Option(
                    data=x, key=x.product_name, on_click=self.choice_dd_prod_start
                ),
                allProdotti,
            )
        )
        prodottiEndDDoptions = list(
            map(
                lambda x: ft.dropdown.Option(
                    data=x, key=x.product_name, on_click=self.choice_dd_prod_end
                ),
                allProdotti,
            )
        )

        self._view._ddProdStart.options = prodottiStartDDoptions
        self._view._ddProdEnd.options = prodottiEndDDoptions

        self._view.update_page()

    def choice_dd_cat(self, e):
        self._categoryValue = e.control.data

    def choice_dd_prod_start(self, e):
        self._productValueStart = e.control.data

    def choice_dd_prod_end(self, e):
        self._productValueEnd = e.control.data

    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
