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