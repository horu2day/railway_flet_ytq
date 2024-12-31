import flet as ft
from src.pages.main import main

def handler(event, context):
    page = ft.Page()
    main(page)
    return {
        'statusCode': 200,         'body': "Flet app initialized"
    }

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)