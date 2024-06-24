# Prova Experimental | Oak Tecnologia
# Candidato: Luan de Oliveira Azevedo

from dataclasses import dataclass
import re

import flet as ft


@dataclass
class Product:
	"""
	Class to model a product.
	"""
	name: str
	description: str
	value: float
	is_available: bool


class ProductDatabase:
	"""
	Class to represent a database for the application.
	"""

	def __init__(self):
		self.items = []

	def add_item(self, product):
		self.items.append(product)
		self.items = sorted(self.items, key=lambda prod: prod.value)


def main(page: ft.Page):
	productsDB = ProductDatabase()

	def register(e):
		_name = name_component.value
		if not _name:
			name_component.error_text = 'Insira o nome do produto'
			page.update()
			return
		else:
			_description = description_component.value
			if not _description:
				description_component.error_text = 'Insira a descrição do produto'
				return
			else:
				_value = value_component.value
				_is_available = availability_component.value
				if not _is_available:
					availability_component.error_text = 'Escolha uma opção'
					return
				else:
					product = Product(name=_name, description=_description, value=_value, is_available=_is_available)
					productsDB.add_item(product)
					products_table.rows = [
						ft.DataRow(
							cells=[ft.DataCell(ft.Text(_item.name)), ft.DataCell(ft.Text(_item.value))]
						) for _item in productsDB.items
					]

					name_component.value = ''
					description_component.value = ''
					value_component.value = '0,00'
					availability_component.value = None
					page_tabs.selected_index = 1
					page.update()

	def focus_name_component(e):
		name_component.error_text = ''
		name_component.value = ''
		page.update()

	def focus_description_component(e):
		description_component.error_text = ''
		page.update()

	def focus_value_component(e):
		if value_component.error_text:
			value_component.error_text = ''
		else:
			value_component.value = ''

		page.update()

	def focus_availability_component(e):
		availability_component.error_text = ''

		page.update()

	def validate_input(e):
		pattern = r'^\d+(,\d{1,2})?$'
		_value = value_component.value
		if not re.match(pattern, _value):
			value_component.error_text = 'Valor inválido'
			page.update()

	page.title = "Cadastro de Produtos"
	page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
	page.theme_mode = ft.ThemeMode.LIGHT
	page.window_center = True
	page.window.maximized = True
	page.scroll = 'always'

	page_tabs = ft.Tabs(
		selected_index=0,
		animation_duration=300,
		tabs=[
		]
	)

	registry_content = []

	listing_content = []

	registry_tab = ft.Tab(
		text='Cadastro'
	)

	listing_tab = ft.Tab(
		text='Listagem'
	)

	registry_title = ft.Text(
		value="Cadastro de Produtos",
		size=36,
		weight='bold'
	)

	listing_title = ft.Text(
		value="Listagem de Produtos",
		size=36,
		weight='bold'
	)

	name_component = ft.TextField(
		label='Nome do Produto',
		width=550,
		on_focus=focus_name_component
	)

	description_component = ft.TextField(
		label='Descrição do Produto',
		multiline=True,
		width=550,
		on_focus=focus_description_component
	)

	value_component = ft.TextField(
		label='Valor do Produto',
		value='0,00',
		width=550,
		prefix_text='R$ ',
		input_filter=ft.InputFilter(regex_string=r'[0-9]|,'),
		on_blur=validate_input,
		on_focus=focus_value_component
	)

	availability_component = ft.Dropdown(
		width=550,
		label='Está disponível?',
		options=[
			ft.dropdown.Option("Sim"),
			ft.dropdown.Option("Não")
		],
		on_focus=focus_availability_component
	)
	submit_btn = ft.CupertinoFilledButton(
		text='Cadastrar',
		width=200,
		on_click=register
	)

	products_table = ft.DataTable(
		columns=[
			ft.DataColumn(ft.Text("Nome")),
			ft.DataColumn(ft.Text("Valor")),
		]
	)

	registry_content.extend(
		[
			registry_title,
			name_component,
			description_component,
			value_component,
			availability_component,
			submit_btn,
		]
	)

	listing_content.extend([listing_title, products_table])

	registry_tab.content = ft.Container(
		content=ft.Column(
			controls=registry_content,
			horizontal_alignment='center'
		)
	)

	listing_tab.content = ft.Container(
		content=ft.Column(
			controls=listing_content,
			horizontal_alignment='center'
		)
	)

	page_tabs.tabs.append(registry_tab)
	page_tabs.tabs.append(listing_tab)

	page.add(
		page_tabs
	)



