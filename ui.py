# 2026 NXFORGE nx.messenger v0.1

import flet as ft
import asyncio


# Main Program
def main(page: ft.Page):
    async def view_pop(e):
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)


    def route_change():
        page.views.clear()
        page.views.append(ViewHome)

        if page.route.startswith("/chat/"):
            _, _, name, ip = page.route.split("/")
            page.views.append(chat(page.route, name, ip))

        page.update()


    def show_indev():
        page.show_dialog(ft.SnackBar(ft.Text("It's in development!")))


    # Page
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.title = "NXMessenger - NXFORGE"
    page.window.icon = "C:\\Users\\sachu\\Documents\\NXMessanger\\icons\\icon_light.ico"
    page.window.min_height = 400
    page.window.min_width = 300


    # Home Page
    def home(route: str):
        async def handle_confirm_dismiss(e: ft.DismissibleDismissEvent):
            if e.direction == ft.DismissDirection.END_TO_START:
                await e.control.confirm_dismiss(True)
            else:
                await e.control.confirm_dismiss(False)
                show_indev()


        def gen_elements_chats(DictChats: dict):
            ListChat = list()

            for chat in DictChats.items():
                ListChat.append(CardChat(chat[0], chat[1]))

            return ListChat
        
        view = ft.View(route=route)

        CardChat = lambda name, ip: ft.Dismissible(
            ft.Card(
                ft.Container(
                    ft.ListTile(
                        title=name,
                        subtitle=ip,
                        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                        mouse_cursor=ft.MouseCursor.CLICK
                    ),
                    padding=ft.Padding.all(10),
                    on_click=lambda: asyncio.create_task(page.push_route(f"/chat/{name}/{ip}"))
                ),
            ),
            dismiss_direction=ft.DismissDirection.HORIZONTAL,
            background=ft.Container(ft.ListTile(title="Call", leading=ft.Icon(ft.Icons.CALL)), bgcolor=ft.Colors.GREEN, border_radius=16, align=ft.Alignment.CENTER),
            secondary_background = ft.Container(ft.ListTile(title=ft.Text("Block", text_align=ft.TextAlign.RIGHT), trailing=ft.Icon(ft.Icons.BLOCK)), bgcolor=ft.Colors.RED_700, border_radius=16, align=ft.Alignment.CENTER),
            dismiss_thresholds={
                ft.DismissDirection.END_TO_START: 0.2,
                ft.DismissDirection.START_TO_END: 0.2,
            },
            on_confirm_dismiss=handle_confirm_dismiss,
        )

        view.appbar = ft.AppBar(
            title=ft.Row(controls=[ft.Image("icons/icon_transparent.png", width=45), ft.Text("NXMessenger")]),
            bgcolor=ft.Colors.SURFACE_CONTAINER,
        )

        ListChat = ft.ListView(
            controls=gen_elements_chats({"Chat 1": "1.1.1.1", "Chat 2": "1.0.1.0", "Chat 3": "1.1.1.1", "Chat 4": "1.0.1.0", "Chat 5": "1.1.1.1", "Chat 6": "1.0.1.0", "Chat 7": "1.1.1.1", "Chat 8": "1.0.1.0",})
        )
        view.controls = [
            ft.Column([
                    ft.Container(ListChat, expand=True)
                ],
                expand=True
            )
        ]

        view.floating_action_button = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=show_indev)

        return view
    

    # Chat Page
    def chat(route: str, name="test", ip="0.0.0.0"):
        def gen_messages(json: list):
            ListMessages = list()

            for DictMessage in json:
                DictMessage: dict
                for message in DictMessage.items():
                    ListMessages.append(CardMessage(message[0], message[1]))

            return ListMessages

        view = ft.View(route=route)

        view.appbar = ft.AppBar(
            title=ft.ListTile(
                title=name,
                subtitle=ip,
                bgcolor=ft.Colors.TRANSPARENT,
                subtitle_text_style=ft.TextStyle(size=12, weight=ft.FontWeight.W_400),
                title_text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_400),
                content_padding=0,
                margin=0,
            ),
            actions_padding=8,
            actions=[
                ft.IconButton(ft.Icons.SEARCH, on_click=show_indev),
                ft.IconButton(ft.Icons.MORE_VERT, on_click=show_indev),
            ],
            bgcolor=ft.Colors.SURFACE_CONTAINER,
        )

        CardMessage = lambda name, message: ft.Card(
            ft.Container(
                ft.ListTile(
                    title=name,
                    subtitle=message,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                    subtitle_text_style=ft.TextStyle(
                        size=18,
                        weight=ft.FontWeight.W_400,
                        color=ft.Colors.WHITE
                    ),
                    title_text_style=ft.TextStyle(
                        size=16,
                        weight=ft.FontWeight.W_400,
                        color=ft.Colors.GREY_400
                    ),
                    content_padding=0,
                    trailing=ft.IconButton(ft.Icons.MORE_VERT_ROUNDED, on_click=show_indev),
                ),
                padding=ft.Padding.only(left=16, top=8, right=16, bottom=8),
            )
        )

        JsonMessages = [{"NXFORGE": "Hello, World!"}, {"Python": "Hello, NXFORGE!"}, {"NXFORGE": "Oh, Python, Its you!"}, {"Python": "Yes, NXFORGE!"}, {"Python": "Its me!"}, {"NXFORGE": "Bye, Python!"}, {"Python": "Bye, Bye!"}]

        view.controls = [
            ft.Column(
                [
                    ft.Container(ft.ListView(gen_messages(JsonMessages), auto_scroll=True), expand=True),
                    ft.Card(
                        ft.Container(
                            ft.Row([
                                ft.TextField(expand=True, border_color=ft.Colors.TRANSPARENT, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH, border_radius=8, label="Message", text_vertical_align=ft.VerticalAlignment.CENTER),
                                ft.IconButton(ft.Icons.SEND_ROUNDED, on_click=show_indev),
                            ], expand=True),
                            expand=True,
                            padding=ft.Padding.all(8),
                        ),
                    )
                ],
                alignment=ft.MainAxisAlignment.END,
                expand=True,
            )
        ]

        return view
    

    ViewHome = home("/")

    route_change()



if __name__ == "__main__":
    ft.run(main)
