import flet as ft
import aiohttp

async def main(page: ft.Page):
    page.title = "MyTube Second Brain"
    page.window.width = 600
    page.window.height = 800
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    api_key_field = ft.TextField(label="Google API Key", password=True, width=500)
    url_field = ft.TextField(label="YouTube URL", width=500)
    question_field = ft.TextField(label="썸네일 질문", width=500)
    
    answer_text = ft.Markdown(
        "",
        selectable=True,
        extension_set=ft.MarkdownExtensionSet.COMMON_MARK,
        on_tap_link=lambda e: page.launch_url(e.data),
        width=600,
        height=600
    )
    
    scrollable_answer = ft.Container(
        content=ft.Column([answer_text], scroll=ft.ScrollMode.ALWAYS),
        border=ft.border.all(1, ft.colors.GREY_300),
        border_radius=5,
        padding=10,
        expand=True
    )

    async def analyze_video(e):
        async with aiohttp.ClientSession() as session:
            async with session.post('http://localhost:8000/api/youtube/analyze', 
                json={'url': url_field.value, 'api_key': api_key_field.value}) as resp:
                result = await resp.json()
                question_field.value = result['question']
                answer_text.value = result['answer']
                page.update()

    async def summarize_video(e):
        async with aiohttp.ClientSession() as session:
            async with session.post('http://localhost:8000/api/youtube/summarize',
                json={'url': url_field.value, 'api_key': api_key_field.value}) as resp:
                result = await resp.json()
                answer_text.value = result['summary']
                page.update()

    page.add(
        api_key_field,
        url_field,
        ft.Row([
            ft.ElevatedButton("정답", on_click=analyze_video),
            ft.ElevatedButton("영상정리", on_click=summarize_video),
        ], alignment=ft.MainAxisAlignment.CENTER),
        question_field,
        ft.Container(content=scrollable_answer, expand=True)
    )