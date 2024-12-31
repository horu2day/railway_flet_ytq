import flet as ft
import aiohttp
from google_auth_oauthlib.flow import InstalledAppFlow

class AuthPage:
    def __init__(self, auth_callback):
        self.auth_callback = auth_callback

    async def build(self, page: ft.Page):
        page.title = "로그인"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.window.width = 400
        page.window.height = 600

        self.status_text = ft.Text("", size=16)
        self.login_button = ft.ElevatedButton(
            text="Google로 로그인",
            icon=ft.Icons.LOGIN,
            on_click=self.handle_google_login,
            style=ft.ButtonStyle(
                color={
                    ft.MaterialState.DEFAULT: ft.colors.WHITE,
                    ft.MaterialState.HOVERED: ft.colors.WHITE,
                },
                bgcolor={
                    ft.MaterialState.DEFAULT: ft.colors.BLUE,
                    ft.MaterialState.HOVERED: ft.colors.BLUE_700,
                },
            )
        )

        main_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Login", size=32, weight=ft.FontWeight.BOLD),
                    self.status_text,
                    self.login_button,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            padding=ft.padding.all(30),
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLUE_GREY_100,
            )
        )

        page.add(main_container)
        page.update()

    async def handle_google_login(self, e):
        self.status_text.value = "로그인 중..."
        self.status_text.update()
        
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secrets.json",
                ['openid', 'https://www.googleapis.com/auth/userinfo.email']
            )
            credentials = flow.run_local_server(port=8080)
            
            async with aiohttp.ClientSession() as session:
                async with session.post('http://localhost:8000/api/auth/google',
                    json={'id_token': credentials.id_token}) as resp:
                    result = await resp.json()
                    if result.get('token'):
                        self.auth_callback(result['token'])
                    else:
                        self.status_text.value = "로그인 실패"
                        self.status_text.update()
        except Exception as e:
            print(f"Google 로그인 에러: {str(e)}")
            self.status_text.value = "로그인 실패"
            self.status_text.update()