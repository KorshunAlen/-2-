import time
import wx
import matplotlib.pyplot as plt

class TimeTracker:
    def __init__(self):
        self.tasks = {}
        self.start_times = {}

    def start_task(self, task_name):
        if task_name in self.start_times:
            wx.MessageBox(f"Задача '{task_name}' уже запущена.", "Ошибка", wx.OK | wx.ICON_ERROR)
            return
        self.start_times[task_name] = time.time()
        wx.MessageBox(f"Задача '{task_name}' начата.", "Информация", wx.OK | wx.ICON_INFORMATION)

    def stop_task(self, task_name):
        if task_name not in self.start_times:
            wx.MessageBox(f"Задача '{task_name}' не была запущена.", "Ошибка", wx.OK | wx.ICON_ERROR)
            return
        start_time = self.start_times.pop(task_name)
        elapsed_time = time.time() - start_time
        if task_name in self.tasks:
            self.tasks[task_name] += elapsed_time
        else:
            self.tasks[task_name] = elapsed_time
        wx.MessageBox(f"Задача '{task_name}' остановлена. Прошло времени: {elapsed_time:.2f} секунд.", "Информация",
                      wx.OK | wx.ICON_INFORMATION)

    def report(self):
        if not self.tasks:
            wx.MessageBox("Нет завершенных задач.", "Информация", wx.OK | wx.ICON_INFORMATION)
            return

        total_seconds = 24 * 60 * 60  # 24 часа в секундах
        labels = []
        times = []
        for task, elapsed_time in self.tasks.items():
            labels.append(task)
            times.append(elapsed_time)

        # Добавляем оставшееся время до 24 часов
        other_time = total_seconds - sum(times)
        if other_time > 0:
            labels.append("Прочее")
            times.append(other_time)

        # Функция для форматирования меток с часами и процентами
        def format_func(pct, allvals):
            absolute = pct / 100. * sum(allvals)
            hours = absolute / 3600
            return "{:.1f}%\n({:.1f} ч)".format(pct, hours)

        # Рисуем круговую диаграмму
        plt.figure(figsize=(10, 7))
        plt.pie(times, labels=labels, autopct=lambda pct: format_func(pct, times), startangle=140)
        plt.axis('equal')
        plt.title('Диаграмма выполненных задач за 24 часа')
        plt.show()


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)

        self.tracker = TimeTracker()

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.task_name_ctrl = wx.TextCtrl(panel)
        vbox.Add(self.task_name_ctrl, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.start_button = wx.Button(panel, label="Начать задачу")
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start_task)
        vbox.Add(self.start_button, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.stop_button = wx.Button(panel, label="Остановить задачу")
        self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop_task)
        vbox.Add(self.stop_button, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.report_button = wx.Button(panel, label="Показать отчет")
        self.report_button.Bind(wx.EVT_BUTTON, self.on_report)
        vbox.Add(self.report_button, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.exit_button = wx.Button(panel, label="Выход")
        self.exit_button.Bind(wx.EVT_BUTTON, self.on_exit)
        vbox.Add(self.exit_button, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)

        self.SetTitle("Тайм Трекер")
        self.Centre()

    def on_start_task(self, event):
        task_name = self.task_name_ctrl.GetValue().strip()
        if task_name:
            self.tracker.start_task(task_name)
        else:
            wx.MessageBox("Введите название задачи.", "Ошибка", wx.OK | wx.ICON_ERROR)

    def on_stop_task(self, event):
        task_name = self.task_name_ctrl.GetValue().strip()
        if task_name:
            self.tracker.stop_task(task_name)
        else:
            wx.MessageBox("Введите название задачи.", "Ошибка", wx.OK | wx.ICON_ERROR)

    def on_report(self, event):
        self.tracker.report()

    def on_exit(self, event):
        self.Close()


def main():
    app = wx.App(False)
    frame = MainFrame(None)
    frame.Show(True)
    app.MainLoop()


if __name__ == "__main__":
    main()
