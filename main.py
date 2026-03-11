# 2026 NXFORGE nx.messenger v0.1

import flet as ft
import asyncio
import data
import client
import server
import threading
import time

data.init()

# Main Program
def main(page: ft.Page):
    async def view_pop(e):
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(str(top_view.route))


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
    page.title = "NXMessenger"
    page.window.icon = data.abspath("icons\\icon_light.ico")
    page.window.min_height = 400
    page.window.min_width = 300


    # Home Page
    def home(route: str):
        async def handle_confirm_dismiss(e: ft.DismissibleDismissEvent):
            if e.direction == ft.DismissDirection.END_TO_START:
                await e.control.confirm_dismiss(True)
                DataChats.remove(e.control.key)
            else:
                await e.control.confirm_dismiss(False)
                show_indev()


        def update_elements_chats() -> None:
            ListChats = DataChats.load()
            ElementChats = list()

            for i, chat in enumerate(ListChats):
                ElementChats.append(CardChat(i, chat.get("name"), chat.get("ip")))

            ListChat.controls = ElementChats

            page.update()
        

        def dialog_add_chat_add():
            ip = DialogTextIP.value + ":" + DialogTextPort.value
            DataChats.add({"name": "Name", "ip": ip})

            page.pop_dialog()
            
            update_elements_chats()


        DataChats = data.DataBaseChats()

        view = ft.View(route=route)

        DialogTextIP = ft.TextField(border_color=ft.Colors.GREY, label="IP address", width=200)
        DialogTextPort = ft.TextField(border_color=ft.Colors.GREY, label="Port", width=80)
        DialogAddChat = lambda: ft.AlertDialog(
            title=ft.Text("Adding a chat:"),
            content=ft.Row([DialogTextIP, DialogTextPort]),
            actions=[ft.TextButton("Cancel", on_click=lambda e: page.pop_dialog()), ft.TextButton("Add", on_click=dialog_add_chat_add)],
            modal=True,
        )

        CardChat = lambda id, name, ip: ft.Dismissible(
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
            key=id
        )

        view.appbar = ft.AppBar(
            title=ft.Row(controls=[ft.Image(data.abspath("icons\\icon_transparent.png"), width=45), ft.Text("NXMessenger")]),
            bgcolor=ft.Colors.SURFACE_CONTAINER,
        )

        print(data.abspath("icons\\icon_transparent.png"))

        ListChat = ft.ListView()

        update_elements_chats()

        view.controls = [
            ft.Column([
                    ft.Container(ListChat, expand=True)
                ],
                expand=True
            )
        ]

        view.floating_action_button = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=lambda: page.show_dialog(DialogAddChat()))

        return view
    

    # Chat Page
    def chat(route: str, name="test", ip="0.0.0.0"):
        def gen_messages(element: ft.ListView):
            ListMessages = list()

            try:
                for message in server.get_messages(ip):
                    ListMessages.append(CardMessage(name, message))
            except:
                for DictMessage in JsonMessages:
                    DictMessage: dict
                    for n, msg in DictMessage.items():
                        ListMessages.append(CardMessage(n, msg))

            if element.controls != ListMessages:
                element.controls = ListMessages
                page.update()
                print("page updated")

            time.sleep(2)
            gen_messages(element)


        def send_msg(e):
            if TextFieldMessage.value != "":
                client.post(ip, TextFieldMessage.value)
                TextFieldMessage.value = ""


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

        JsonMessages = [{"NXFORGE": "Hello, World!"}, {"Python": "Hello, NXFORGE!"}, {"NXFORGE": "Oh, Python, Its you!"}, {"Python": "Yes, NXFORGE!"}, {"Python": "Its me!"}, {"NXFORGE": "Bye, Python!"}, {"Python": "Bye, Bye!"}, {"NXFORGE": "You have a bug, tell the developer!"}]
        BoxMessages = ft.ListView([], auto_scroll=True)

        TextFieldMessage = ft.TextField(expand=True, border_color=ft.Colors.TRANSPARENT, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH, border_radius=8, label="Message", text_vertical_align=ft.VerticalAlignment.CENTER, on_submit=send_msg)

        view.controls = [
            ft.Column(
                [
                    ft.Container(BoxMessages, expand=True),
                    ft.Card(
                        ft.Container(
                            ft.Row([
                                TextFieldMessage,
                                ft.IconButton(ft.Icons.SEND_ROUNDED, on_click=send_msg),
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

        threading.Thread(target=lambda: gen_messages(BoxMessages), daemon=True).start()

        return view
    

    ViewHome = home("/")

    route_change()



if __name__ == "__main__":
    threading.Thread(target=server.run, daemon=True, args=[63323]).start()
    ft.app(main)
