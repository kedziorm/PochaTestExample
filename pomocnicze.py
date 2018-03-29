# -*- coding: utf-8 -*-


def czyJestSelenium():
	try:
		from selenium import webdriver
	except ImportError:
		print 'Proszę zainstalować Selenium, wpisując polecenie: {0}'.format(
			'pip install selenium')
		return False
	try:
		driver = webdriver.Firefox()
		driver.close()
		return True
	except:
		print 'Wystąpił błąd - czy pobrano geckodriver?'
		print 'https://github.com/mozilla/geckodriver/releases'
		print 'Czy GeckoDriver jest w domyślnej ścieżce?'
		return False


def zaloguj(driver, email, haslo):
	import time

	def wypelnij(nazwa, wartosc):
		element = driver.find_element_by_name(nazwa)
		element.clear()
		element.send_keys(wartosc)

	wypelnij("email", email)
	wypelnij("password", haslo)
	driver.find_element_by_name("submit").click()
	# ToDo: Lepiej użyć WebDriverWait lub sprawdzić status strony,
	# aby upewnić się, czy strona załadowała się po kliknięciu przycisku.
	time.sleep(2)


def czyJestTakiElement(driver, klasaLubNazwa, czyKlasa=True):
	# Wyszukuje i sprawdza, czy element jest widoczny.
	from selenium.common.exceptions import NoSuchElementException
	try:
		myElem = (
			driver.find_element_by_class_name(klasaLubNazwa) if czyKlasa
			else driver.find_element_by_name(klasaLubNazwa)
		)
		return myElem.is_displayed()
	except NoSuchElementException:
		return False


def bledyLogowania(driver):
	# Zwraca tablicę z wyświetlonymi na stronie błędami: hasłem i e-mailem.
	l = driver.find_element_by_name("login")
	bledy = []
	for val in [1, 2]:
		try:
			sel = "div.form__error:nth-child({0})".format(val)
			elem = l.find_element_by_css_selector(sel)
			text = elem.get_attribute("data-message")
		except:
			text = ''
		finally:
			bledy.append(text)
	return bledy