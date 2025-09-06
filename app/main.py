from nicegui import ui
from app.services.llm_service import LLMService
from app.services.task_service import Task
from app.services.export_service import ExportService


class TaskUiModel:

    def __init__(self):
        self.variables = ''
        self.question = ''
        self.model = ''
        self.api_key = ''


async def start_once(task_data: TaskUiModel):
    llm_service = LLMService(task_data.api_key)
    first_var = task_data.variables.split('\n')[0]
    task = Task(first_var, task_data.question, task_data.model, llm_service)
    response = await task.start_once()
    ui.notify(response, title=f'Task[{task.id}] result', duration=10000)


async def start_all(task_data: TaskUiModel, result_container):
    llm_service = LLMService(task_data.api_key)
    tasks = []
    for var in task_data.variables.split('\n'):
        if not var.strip():
            continue
        task = Task(var.strip(), task_data.question, task_data.model,
                    llm_service)
        tasks.append(task)

    result_container.clear()
    markdown_by_task_id = {}
    total = len(tasks)
    completed = 0
    export_rows = []

    def run_export():
        path = ExportService.export_rows_to_excel(export_rows)
        ui.download(path, filename='results.xlsx')

    # 顶部进度显示
    with result_container:
        with ui.row().classes('items-center gap-3 w-full'):
            progress_label = ui.label(f'进度：{completed} / {total}').classes(
                'text-sm')
            progress_bar = ui.linear_progress(value=0).classes('w-full')
            export_btn = ui.button(
                '导出 Excel',
                on_click=lambda e: run_export()).props('color=accent')
            export_btn.disable()

    # 结果列表
    with result_container:
        for t in tasks:
            with ui.card().classes('w-full'):
                with ui.row().classes('items-center justify-between w-full'):
                    ui.label().bind_text_from(t, 'status').classes('text-sm')
                    ui.label().bind_text_from(t, 'var').classes('text-sm')
                ui.separator()
                md = ui.markdown('').classes('w-full')
                markdown_by_task_id[t.id] = md

    for t in tasks:
        await t.start_once()
        markdown_by_task_id[t.id].set_content(t.result or '')
        completed += 1
        if total:
            progress_bar.set_value(completed / total)
        else:
            progress_bar.set_value(1)
        progress_label.set_text(f'进度：{completed} / {total}')
        export_rows.append({'var': t.var, 'result': t.result})

    export_btn.enable()


@ui.page('/batch_llm')
def create_task():
    task = TaskUiModel()

    ui.page_title('批量提问小助手')
    with ui.header().classes('items-center justify-between px-4 py-2'):
        ui.label('批量提问小助手').classes('text-lg font-medium')
        ui.button('🌙/☀️', on_click=ui.dark_mode().toggle).props('flat')

    with ui.row().classes('w-full gap-6 px-4 pb-4'):
        # 左侧：表单
        with ui.card().classes('w-1/2 min-w-[420px]'):
            ui.label('创建任务').classes('text-base font-medium')

            vars_input = ui.textarea('替换的文本变量，一行一个☝️',
                                     placeholder='例如：\nadidas\nnike').props(
                                         'autogrow').classes('w-full') \
                .bind_value_to(task, 'variables')

            question_input = ui.textarea('Question with {var}',
                                         placeholder='例如：how to buy {var}') \
                .props('autogrow').classes('w-full').bind_value_to(
                    task, 'question')

            ui.select(['gpt-4o-mini', 'gpt-4o'], value='gpt-4o-mini') \
                .classes('w-full').bind_value_to(task, 'model')

            ui.input('openai api key', password=True,
                     placeholder='请输入 openai api key').classes('w-full') \
                .bind_value_to(task, 'api_key')

            with ui.row().classes('gap-2 pt-1'):
                ui.button('试一次', on_click=lambda: start_once(task)).props(
                    'color=primary')
                ui.button('全部运行', on_click=lambda: start_all(task, result_container)) .props(
                    'color=positive')

        # 右侧：预览与结果
        with ui.card().classes('w-1/2 flex-1'):
            ui.label('问题预览').classes('text-base font-medium')
            preview = ui.markdown('').classes('max-h-64 overflow-auto w-full')

            def update_preview():
                first_var = task.variables.split('\n')[0] if task.variables else ''
                try:
                    content = task.question.format(var=first_var)
                except Exception:
                    content = task.question
                preview.set_content(content)

            # 更新预览
            vars_input.on('change', lambda e: update_preview())
            question_input.on('change', lambda e: update_preview())
            update_preview()

    # 页面底部：结果区域
    with ui.row().classes('w-full px-4 mt-2'):
        with ui.card().classes('w-full'):
            ui.label('运行结果').classes('text-base font-medium pb-1')
            result_container = ui.column().classes('w-full')


ui.label('批量提问小助手!')
ui.link('gogogo！', '/batch_llm')

ui.run()
