import time
import ctypes
import psutil


def get_explorer_pid() -> int | None:
    """Возвращает PID процесса explorer.exe, если он существует."""
    for process in psutil.process_iter(['pid', 'name']):
        try:
            if process.info['name'].lower() == 'explorer.exe':
                return process.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None


def get_active_window_pid():
    """Возвращает PID активного окна."""
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()  # Получение дескриптора активного окна
    pid = ctypes.c_ulong()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))  # Получение PID из дескриптора
    return pid.value


def is_pid_active(pid):
    """Проверяет, связано ли активное окно с заданным PID."""
    active_pid = get_active_window_pid()
    return active_pid == pid


if __name__ == "__main__":
    while True:
        explorer_pid = get_explorer_pid()
        if not explorer_pid:
            print("закрыт")
        print(is_pid_active(explorer_pid))
        
        time.sleep(0.7)
