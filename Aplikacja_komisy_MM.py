from tkinter import *
from tkinter import messagebox
import tkintermapview
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

dealerships: list = []
geolocator = Nominatim(user_agent="applikacja_Komisy")
current_dealership_index = None
class Dealership:
    def __init__(self, name, address, phone, website, map_widget=None):
        self.name = name
        self.address = address
        self.phone = phone
        self.website = website
        self.coordinates = self.get_coordinates()
        self.marker = None
        if map_widget and self.coordinates:
            self.marker = map_widget.set_marker(
                self.coordinates[0],
                self.coordinates[1],
                text=f'{self.name}',
                command=self.show_details
            )
        self.cars = []
    def get_coordinates(self) -> list:
        try:
            time.sleep(0.1)
            location = geolocator.geocode(self.address, timeout = 10)
            if location:
                print(f"Znaleziono współrzędne dla {self.address}: {location.latitude},{location.longitude}")
                return [location.latitude, location.longitude]
            else:
                print(f"Nie znaleziono współrzędnych dla: {self.address}")
            messagebox.showwarning("Uwaga", f"nie udało się znaleść lokalizacji dla adresu: {self.address}\nUstawienie domyślnej lokalizacji (Warszawa).")
            return [52.2297, 21.0122]
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Błąd geokodowania: {e}")
            messagebox.showwarning("Uwaga", f"Błąd podczas wyszukiwania lokalizacji: {e}\nUstawienie domyślnej lokazlizacji (Warszawa).")
            return [52.2297, 21.0122]
        except Exception as e:
            print(f"Nieoczekiwany błąd: {e}")
            return [52.2297, 21.0122]

    def add_car(self, marka, model, rok, cena, przebieg):
        self.cars.append({
            'marka': marka,
            'model': model,
            'rok': rok,
            'cena': cena,
            'przebieg': przebieg
        })

    def remove_car(self, index):
        if 0 <= index < len(self.cars):
            self.cars.pop(index)
            return True
        return False

    def show_details(self):
        for idx, dealer in enumerate(dealerships):
            if dealer == self:
                select_dealership(idx)
                break

def select_dealership(index):
    global current_dealership_index
    if 0 <= index < len(dealerships):
        current_dealership_index = index
        listbox_lista_komisow.selection_clear(0, END)
        listbox_lista_komisow.selection_set(index)
        listbox_lista_komisow.activate(index)
        show_dealership_details()
    else:
        current_dealership_index = None
        clear_dealership_details()

def add_dealership() -> None:
    name = entry_nazwa.get().strip()
    address = entry_adres.get().strip()
    phone = entry_telefon.get().strip()
    website = entry_website.get().strip()

    if not name or not address:
        messagebox.showerror("Błąd", "Nazwa i adres są wymagane!")
        return

    dealership = Dealership(
        name=name,
        address=address,
        phone=phone,
        website=website,
        map_widget=map_widget
    )
    dealerships.append(dealership)

    entry_nazwa.delete(0, END)
    entry_adres.delete(0, END)
    entry_telefon.delete(0, END)
    entry_website.delete(0, END)

    entry_nazwa.focus()
    show_dealerships()

    listbox_lista_komisow.selection_clear(0, END)
    listbox_lista_komisow.selection_set(END)
    listbox_lista_komisow.activate(END)
    show_dealership_details()

    select_dealership(len(dealerships) - 1)

def show_dealerships() -> None:
    listbox_lista_komisow.delete(0, END)
    for idx, dealership in enumerate(dealerships):
        listbox_lista_komisow.insert(idx, f'{idx + 1}. {dealership.name}')

def remove_dealership():
    global current_dealership_index
    if current_dealership_index is None or not listbox_lista_komisow.curselection():
        messagebox.showerror("Błąd", "Wybierz komis do usunięcia")
        return

    i = current_dealership_index
    if i < len(dealerships) and dealerships[i].marker:
        dealerships[i].marker.delete()
    dealerships.pop(i)
    show_dealerships()
    if dealerships:
        new_index = min(i, len(dealerships) - 1)
        select_dealership(new_index)
    else:
        current_dealership_index = None
        clear_dealership_details()

def edit_dealership():
    if current_dealership_index is None:
        messagebox.showerror("Błąd", "Wybierz komis do edycji")
        return

    i = current_dealership_index
    dealership = dealerships[i]

    entry_nazwa.delete(0, END)
    entry_adres.delete(0, END)
    entry_telefon.delete(0, END)
    entry_website.delete(0, END)

    entry_nazwa.insert(0, dealership.name)
    entry_adres.insert(0, dealership.address)
    entry_telefon.insert(0, dealership.phone)
    entry_website.insert(0, dealership.website)

    button_dodaj_komis.config(text='Zapisz zmiany', command=lambda: update_dealership(i))

def update_dealership(i):
    name = entry_nazwa.get().strip()
    address = entry_adres.get().strip()
    phone = entry_telefon.get().strip()
    website = entry_website.get().strip()

    if not name or not address:
        messagebox.showerror("Błąd", "Nazwa i adres są wymagane!")
        return
    dealerships[i].name = name
    dealerships[i].address = address
    dealerships[i].phone = phone
    dealerships[i].website = website

    old_coords = dealerships[i].coordinates
    dealerships[i].coordinates = dealerships[i].get_coordinates()

    if dealerships[i].marker:
        dealerships[i].marker.delete()
        if map_widget and dealerships[i].coordinates:
            dealerships[i].marker = map_widget.set_marker(
                dealerships[i].coordinates[0],
                dealerships[i].coordinates[1],
                text=f'{dealerships[i].name}',
                command=dealerships[i].show_details
            )
    show_dealerships()
    button_dodaj_komis.config(text='Dodaj komis', command=add_dealership)

    entry_nazwa.delete(0, END)
    entry_adres.delete(0, END)
    entry_telefon.delete(0, END)
    entry_website.delete(0, END)
    entry_nazwa.focus()
    select_dealership(i)

    listbox_lista_komisow.selection_clear(0, END)
    listbox_lista_komisow.selection_set(i)
    listbox_lista_komisow.activate(i)
    show_dealership_details()

def show_dealership_details() -> None:
    global current_dealership_index

    if current_dealership_index is None or current_dealership_index >= len(dealerships):
        clear_dealership_details()
        return

    dealership = dealerships[current_dealership_index]

    label_szczegoly_nazwa_wartosc.config(text=dealership.name)
    label_szczegoly_adres_wartosc.config(text=dealership.address)
    label_szczegoly_telefon_wartosc.config(text=dealership.phone)
    label_szczegoly_website_wartosc.config(text=dealership.website)

    listbox_samochody.delete(0, END)
    for car in dealership.cars:
        listbox_samochody.insert(END,f"{car['marka']} {car['model']} ({car['rok']}) - {car['cena']} PLN, {car['przebieg']} km")

    if dealership.coordinates:
        map_widget.set_zoom(15)
        map_widget.set_position(dealership.coordinates[0], dealership.coordinates[1])

def clear_dealership_details():
    label_szczegoly_nazwa_wartosc.config(text="...")
    label_szczegoly_adres_wartosc.config(text="...")
    label_szczegoly_telefon_wartosc.config(text="...")
    label_szczegoly_website_wartosc.config(text="...")
    listbox_samochody.delete(0, END)
    button_usun_samochod.config(state=DISABLED)


def add_car_to_dealership():
    global current_dealership_index
    try:
        if current_dealership_index is None:
            messagebox.showerror("Błąd", "Wybierz komis z listy przed dodaniem samochodu")
            return

        i = listbox_lista_komisow.curselection()[0]
        marka = entry_marka.get().strip()
        model = entry_model.get().strip()
        rok = entry_rok.get().strip()
        cena = entry_cena.get().strip()
        przebieg = entry_przebieg.get().strip()

        if not all([marka, model, rok, cena, przebieg]):
            messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione")
            return

        rok_int = int(rok)
        cena_float = float(cena)
        przebieg_int = int(przebieg)

        if rok_int < 1900 or rok_int > 2025:
            messagebox.showerror("Błąd", "Podaj poprawny rok produkcji(1900-2025)")
            return

        if cena_float <= 0:
            messagebox.showerror("Błąd", "Cena musi być większa od zera")
            return

        if przebieg_int < 0:
            messagebox.showerror("Błąd", "Przebieg nie może być ujemny")
            return

        dealerships[current_dealership_index].add_car(
            marka=marka,
            model=model,
            rok=rok_int,
            cena=cena_float,
            przebieg=przebieg_int
        )

        entry_marka.delete(0, END)
        entry_model.delete(0, END)
        entry_rok.delete(0, END)
        entry_cena.delete(0, END)
        entry_przebieg.delete(0, END)

        show_dealership_details()
        messagebox.showinfo("Dodano samochód")

    except ValueError as e:
        messagebox.showerror("Błąd", "Rok, cena i przebieg muszą być poprawnymi liczbami")
    except Exception as e:
        messagebox.showerror("Błąd", f"Wybierz komis z listy: {str(e)}")


def remove_car_from_dealership():
    global current_dealership_index

    if current_dealership_index is None:
        messagebox.showerror("Bład wybierz komis z listy")
        return

    if not listbox_samochody.curselection():
        messagebox.showerror("Wybierz samochód do usunięcia")
        return

    try:
        i_samochodu = listbox_samochody.curselection()[0]

        dealership = dealerships[current_dealership_index]

        # Sprawdź czy indeks samochodu jest poprawny
        if i_samochodu < 0 or i_samochodu >= len(dealership.cars):
            messagebox.showerror("Błąd", "Wybrany samochód nie istnieje")
            return

        car_to_remove = dealership.cars[i_samochodu]

        # Potwierdzenie usunięcia
        confirm = messagebox.askyesno(
            "Potwierdzenie usunięcia",
            f"Czy na pewno chcesz usunąć samochód:\n{car_to_remove['marka']} {car_to_remove['model']} ({car_to_remove['rok']})?"
        )

        if confirm:
            success = dealership.remove_car(i_samochodu)
            if success:
                # Wyczyść zaznaczenie po usunięciu
                listbox_samochody.selection_clear(0, END)
                button_usun_samochod.config(state=DISABLED)

                show_dealership_details()
                messagebox.showinfo("Sukces", "Samochód został usunięty pomyślnie")
            else:
                messagebox.showerror("Błąd", "Nie udało się usunąć samochodu")

    except IndexError:
        messagebox.showerror("Błąd", "Wybrany samochód nie istnieje")
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił nieoczekiwany błąd: {str(e)}")

def on_dealership_select(event):
    if listbox_lista_komisow.curselection():
        try:
            index = listbox_lista_komisow.curselection()[0]
            select_dealership(index)
        except IndexError:
            current_dealership_index = None
            clear_dealership_details()


def on_car_select(event):
    try:
        if listbox_samochody.curselection() and current_dealership_index is not None:
            i_samochodu = listbox_samochody.curselection()[0]
            dealership = dealerships[current_dealership_index]
            # Sprawdź czy indeks jest poprawny
            if 0 <= i_samochodu < len(dealership.cars):
                button_usun_samochod.config(state=NORMAL)
            else:
                button_usun_samochod.config(state=DISABLED)
        else:
            button_usun_samochod.config(state=DISABLED)
    except (IndexError, TypeError):
        button_usun_samochod.config(state=DISABLED)
root = Tk()
root.geometry("1200x800")
root.title("System zarządzania komisami samochodowymi")


ramka_lista_komisow = Frame(root)
ramka_formularz_komis = Frame(root)
ramka_formularz_samochod = Frame(root)
ramka_szczegoly = Frame(root)
ramka_mapa = Frame(root)
ramka_lista_samochodow = Frame(root)

ramka_lista_komisow.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
ramka_formularz_komis.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
ramka_formularz_samochod.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")
ramka_szczegoly.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
ramka_lista_samochodow.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
ramka_mapa.grid(row=2, column=2, padx=10, pady=5, sticky="nsew")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=2)
root.grid_rowconfigure(2, weight=1)



label_lista_komisow = Label(ramka_lista_komisow, text="Lista komisów:")
label_lista_komisow.grid(row=0, column=0)

listbox_lista_komisow = Listbox(ramka_lista_komisow, width=30, height=15)
listbox_lista_komisow.grid(row=1, column=0, columnspan=3, sticky="nsew")
listbox_lista_komisow.bind('<<ListboxSelect>>', on_dealership_select)

button_pokaz_szczegoly = Button(ramka_lista_komisow, text="Pokaż szczegóły", command=show_dealership_details)
button_pokaz_szczegoly.grid(row=2, column=0, pady=5)

button_usun_komis = Button(ramka_lista_komisow, text="Usuń", command=remove_dealership)
button_usun_komis.grid(row=2, column=1, pady=5)

button_edytuj_komis = Button(ramka_lista_komisow, text="Edytuj", command=edit_dealership)
button_edytuj_komis.grid(row=2, column=2, pady=5)

label_formularz_komis = Label(ramka_formularz_komis, text="Dodaj komis:")
label_formularz_komis.grid(row=0, column=0, columnspan=2)

label_nazwa = Label(ramka_formularz_komis, text="Nazwa:")
label_nazwa.grid(row=1, column=0, sticky=W)
entry_nazwa = Entry(ramka_formularz_komis)
entry_nazwa.grid(row=1, column=1,sticky='ew')

label_adres = Label(ramka_formularz_komis, text="Adres:")
label_adres.grid(row=2, column=0, sticky=W)
entry_adres = Entry(ramka_formularz_komis)
entry_adres.grid(row=2, column=1, sticky='ew')

label_telefon = Label(ramka_formularz_komis, text="Telefon:")
label_telefon.grid(row=3, column=0, sticky=W)
entry_telefon = Entry(ramka_formularz_komis)
entry_telefon.grid(row=3, column=1, sticky='ew')

label_website = Label(ramka_formularz_komis, text="Strona:")
label_website.grid(row=4, column=0, sticky=W)
entry_website = Entry(ramka_formularz_komis)
entry_website.grid(row=4, column=1, sticky='ew')

button_dodaj_komis = Button(ramka_formularz_komis, text="Dodaj komis", command=add_dealership)
button_dodaj_komis.grid(row=5, column=0, columnspan=2, pady=5)

label_formularz_samochod = Label(ramka_formularz_samochod, text="Dodaj samochód:")
label_formularz_samochod.grid(row=0, column=0, columnspan=2)

label_marka = Label(ramka_formularz_samochod, text="Marka:")
label_marka.grid(row=1, column=0, sticky=W)
entry_marka = Entry(ramka_formularz_samochod)
entry_marka.grid(row=1, column=1, sticky="ew")

label_model = Label(ramka_formularz_samochod, text="Model:")
label_model.grid(row=2, column=0, sticky=W)
entry_model = Entry(ramka_formularz_samochod)
entry_model.grid(row=2, column=1, sticky='ew')

label_rok = Label(ramka_formularz_samochod, text="Rok produkcji:")
label_rok.grid(row=3, column=0, sticky=W)
entry_rok = Entry(ramka_formularz_samochod)
entry_rok.grid(row=3, column=1, sticky='ew')

label_cena = Label(ramka_formularz_samochod, text="Cena (PLN):")
label_cena.grid(row=4, column=0, sticky=W)
entry_cena = Entry(ramka_formularz_samochod)
entry_cena.grid(row=4, column=1, sticky='ew')

label_przebieg = Label(ramka_formularz_samochod, text="Przebieg (km):")
label_przebieg.grid(row=5, column=0, sticky=W)
entry_przebieg = Entry(ramka_formularz_samochod)
entry_przebieg.grid(row=5, column=1, sticky='ew')

button_dodaj_samochod = Button(ramka_formularz_samochod, text="Dodaj samochód", command=add_car_to_dealership)
button_dodaj_samochod.grid(row=6, column=0, columnspan=2, pady=5)


label_szczegoly = Label(ramka_szczegoly, text="Szczegóły komisu:")
label_szczegoly.grid(row=0, column=0, sticky=W)

label_szczegoly_nazwa = Label(ramka_szczegoly, text="Nazwa:")
label_szczegoly_nazwa.grid(row=1, column=0)
label_szczegoly_nazwa_wartosc = Label(ramka_szczegoly, text="...")
label_szczegoly_nazwa_wartosc.grid(row=1, column=1)

label_szczegoly_adres = Label(ramka_szczegoly, text="Adres:")
label_szczegoly_adres.grid(row=1, column=2)
label_szczegoly_adres_wartosc = Label(ramka_szczegoly, text="...")
label_szczegoly_adres_wartosc.grid(row=1, column=3)

label_szczegoly_telefon = Label(ramka_szczegoly, text="Telefon:")
label_szczegoly_telefon.grid(row=1, column=4)
label_szczegoly_telefon_wartosc = Label(ramka_szczegoly, text="...")
label_szczegoly_telefon_wartosc.grid(row=1, column=5)

label_szczegoly_website = Label(ramka_szczegoly, text="Strona:")
label_szczegoly_website.grid(row=1, column=6)
label_szczegoly_website_wartosc = Label(ramka_szczegoly, text="...")
label_szczegoly_website_wartosc.grid(row=1, column=7)

ramka_lista_samochodow_controls = Frame(ramka_lista_samochodow)
ramka_lista_samochodow_controls.grid(row=0, column=0, sticky="ew")

label_lista_samochodow = Label(ramka_lista_samochodow_controls, text="Lista samochodów:")
label_lista_samochodow.grid(row=0, column=0, sticky=W)

button_usun_samochod = Button(ramka_lista_samochodow_controls, text="Usuń samochód", command=remove_car_from_dealership, state=DISABLED)
button_usun_samochod.grid(row=0, column=1, padx=10)

listbox_samochody = Listbox(ramka_lista_samochodow, width=80, height=10)
listbox_samochody.grid(row=1, column=0,sticky="nsew")
listbox_samochody.bind('<<ListboxSelect>>', on_car_select)

map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=500, height=500, corner_radius=0)
map_widget.grid(row=0, column=0, sticky="nsew")
map_widget.set_position(52.2297, 21.0122)  # Warszawa
map_widget.set_zoom(6)

ramka_lista_komisow.grid_rowconfigure(1, weight=1)
ramka_lista_komisow.grid_columnconfigure(0, weight=1)

ramka_formularz_komis.grid_columnconfigure(1, weight=1)
ramka_formularz_samochod.grid_columnconfigure(1, weight=1)

ramka_lista_samochodow.grid_rowconfigure(1, weight=1)
ramka_lista_samochodow.grid_columnconfigure(0, weight=1)

ramka_mapa.grid_rowconfigure(0, weight=1)
ramka_mapa.grid_columnconfigure(0, weight=1)


root.mainloop()