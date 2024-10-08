import flet as ft
import os


class Task(ft.UserControl):
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete

    def build(self):
        self.display_task = ft.Checkbox(
            value=False, label=self.task_name, on_change=self.status_changed
        )
        self.edit_name = ft.TextField(expand=1)

        self.display_view = ft.Row(
            #alignment="spaceBetween",
            alignment="Espaço",
            vertical_alignment="center",
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            #tooltip="Edit To-Do",
                            tooltip="Editar tarefas",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE_OUTLINE,
                            #tooltip="Delete To-Do",
                            tooltip="Excluir tarefas",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = ft.Row(
            visible=False,
            #alignment="spaceBetween",
            alignment="Espaço",
            vertical_alignment="center",
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN, 
                    #tooltip="Update To-Do",
                    tooltip="Atualizar tarefas",
                    on_click=self.save_clicked,
                ),
            ],
        )
        return ft.Column(controls=[self.display_view, self.edit_view])

    async def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        await self.update_async()

    async def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        await self.update_async()

    async def status_changed(self, e):
        self.completed = self.display_task.value
        await self.task_status_change(self)

    async def delete_clicked(self, e):
        await self.task_delete(self)


class TodoApp(ft.UserControl):
    def build(self):
        self.new_task = ft.TextField(
            hint_text="O que precisa ser feito??", on_submit=self.add_clicked, expand=True
        )
        self.tasks = ft.Column()

        self.filter = ft.Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="Tudo"), ft.Tab(text="ativo"), ft.Tab(text="completo")],
        )

        self.items_left = ft.Text("0 items left")

        # application's root control (i.e. "view") containing all other controls
        return ft.Column(
            width=600,
            controls=[
                ft.Row(
                    [ft.Text(value="Todos", style="headlineMedium")], alignment="center"
                ),
                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD, on_click=self.add_clicked
                        ),
                    ],
                ),
                ft.Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                        ft.Row(
                            alignment="spaceBetween",
                            vertical_alignment="center",
                            controls=[
                                self.items_left,
                                ft.OutlinedButton(
                                    text="Clear completo", on_click=self.clear_clicked
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    async def add_clicked(self, e):
        if self.new_task.value:
            task = Task(self.new_task.value, self.task_status_change, self.task_delete)
            self.tasks.controls.append(task)
            self.new_task.value = ""
            await self.new_task.focus_async()
            await self.update_async()

    async def task_status_change(self, task):
        await self.update_async()

    async def task_delete(self, task):
        self.tasks.controls.remove(task)
        await self.update_async()

    async def tabs_changed(self, e):
        await self.update_async()

    async def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                await self.task_delete(task)

    async def update_async(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                status == "Tudo"
                or (status == "ativo" and task.completed == False)
                or (status == "completo" and task.completed)
            )
            if not task.completed:
                count += 1
        self.items_left.value = f"{count} iten(s) ativos restantes"
        await super().update_async()


async def main(page: ft.Page):
    page.title = "Fazer App"

    # Caminho absoluto
    #icon_path = os.path.join(os.getcwd(), "icon.ico")  # Caminho absoluto
    #page.window_icon = icon_path
    page.window_icon = "icon.ico"
    #page.add(ft.Text("Teste do icon da janela"))
    
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"
    await page.update_async()

    # create application instance
    app = TodoApp()

    # add application's root control to the page
    await page.add_async(app)


ft.app(main)