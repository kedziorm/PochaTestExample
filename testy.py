# -*- coding: utf-8 -*-
# Przykładowe testy wykorzystujące Pocha i Selenium.
# Proszę zainstalować pocha (`pip install pocha`) i uruchamiać:
# wpisując polecenie 'pocha testy.py'
from pomocnicze import *
from pocha import after, before, describe, it


@describe('Czy na komputerze zainstalowano Selenium?')
def Podstawowy():
	@it('Selenium i Gecko muszą być zainstalowane w celu uruchomienia testów')
	def CzyMamySelenium():
		assert czyJestSelenium()


@describe('Testy logowania')
def _():
	@before
	def najpierw():
		from selenium import webdriver
		from selenium.webdriver.support.ui import WebDriverWait
		from selenium.webdriver.common.by import By
		from selenium.webdriver.support import expected_conditions as EC
		global WebDriverWait, By, EC
		driver = webdriver.Firefox()
		global driver
		driver.get("https://staging.uptowork.workz.it/login")

	@after
	def pozniej():
		driver.close()

	@describe('Strona logowania wyświetla się prawidłowo')
	def CzySaNaStronie():
		# ToDo: Sprawdzanie wyświetlonych etykiet, czy pola są puste?
		@it('Wyświetlone jest pole do wprowadzenia adresu e-mail')
		def Email():
			assert czyJestTakiElement(driver, "email", False)

		@it('Wyświetlone jest pole do wprowadzenia hasła')
		def Haslo():
			assert czyJestTakiElement(driver, "password", False)

		@it('Nie ma okienka modalnego z ostrzeżeniem')
		def Okienko():
			assert not (czyJestTakiElement(driver, "modal--warning"))

	@describe('Ścieżki niepoprawne')
	def Niepoprawne():
		@it('Informacja przy pustym e-mailu i haśle')
		def PusteDane():
			zaloguj(driver, "", "")
			assert "Wrong e-mail address" in bledyLogowania(driver)[0]
			assert "Wrong password" in bledyLogowania(driver)[1]

		@it('Informacja przy nieprawidłowym e-mailu i pustym haśle')
		def NiepoprawnyEmail():
			zaloguj(driver, "NiepoprawnyEmail", "")
			assert "Wrong e-mail address" in bledyLogowania(driver)[0]
			assert "Wrong password" in bledyLogowania(driver)[1]

		@it('Informacja przy próbie zalogowania się niezarejestrowanym kontem')
		def NieistniejaceKonto():
			zaloguj(driver, "Selenium@pocha.com", "4fg45854")
			elem = WebDriverWait(driver, 10).until(
				EC.visibility_of_element_located(
					(By.CLASS_NAME, "modal--warning")
					)
			)
			msg = elem.find_element_by_class_name("msg").text
			expected = "Wrong e-mail address or password. "\
			"If you don't have an account, please sign up first."
			assert expected == msg
			# Zamknięcie okienka modalnego
			elem.find_element_by_class_name("modal-close").click()
			WebDriverWait(driver, 10).until_not(
				EC.visibility_of_element_located(
					(By.CLASS_NAME, "modal--warning")
					)
			)

	@describe('Ścieżki poprawne')
	def Poprawne():
		@it('Logowanie tradycyjne - można się zalogować i wylogować')
		def Tradycyjne():
			# ToDo: Przechowywać dane do konta w bezpiecznym miejscu
			import time
			email = "beb4wh+d1tx5xejjx9ss@spam4.me"
			zaloguj(driver, email, "SkasujcieMnie4@")
			emailElem = WebDriverWait(driver, 10).until(
				EC.visibility_of_element_located(
					(By.ID, "navbarUserEmail")
					)
			)
			assert "beb4wh+d1tx5xejjx9ss@spam4.me" == emailElem.text
			emailElem.click()
			driver.find_element_by_link_text("Logout").click()
			time.sleep(2)
			assert driver.current_url == "https://staging.uptowork.workz.it/"

		@it('do zaimplementowania - logowanie przez Gmail')
		def PrzezGmail():
			# ToDo: do zaimplementowania
			assert True
