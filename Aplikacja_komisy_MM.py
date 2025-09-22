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
    current_dealership_index = index
    listbox_lista_komisow.selection_clear(0, END)
    listbox_lista_komisow.selection_set(index)
    listbox_lista_komisow.activate(index)
    show_dealership_details()

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
    if not listbox_lista_komisow.curselection():
        messagebox.showerror("Błąd", "Wybierz komis do usunięcia")
        return

    i = listbox_lista_komisow.index(ACTIE)
    if i < len(dealerships) and dealerships[i].marker:
        dealerships[i].marker.delete()
    dealerships.pop(i)
    show_dealerships()
    current_dealership_index = None
    clear_dealership_details()

def edit_dealership():
    if not listbox_lista_komisow.curselection():
        messagebox.showerror("Błąd", "Wybierz komis do edycji")
        return

    i = listbox_lista_komisow.index(ACTIVE)
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

    dealerships[i].update_marker(map_widget)
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

