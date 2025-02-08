import time
import win32api
import win32con


def is_dragging():
    """Проверяет, выполняется ли в данный момент drag-and-drop."""
    try:
        return win32api.GetKeyState(win32con.VK_LBUTTON) < 0
    except Exception as e:
        print(f"Ошибка при проверке drag-and-drop: {e}")
    
    return False


def detect_shake():
    """Отслеживает координаты мыши для определения потрясывания."""
    threshold = 30  # Порог движения для потрясывания
    prev_pos = win32api.GetCursorPos()
    shake_count = 0
    
    while is_dragging():
        curr_pos = win32api.GetCursorPos()
        # movement = abs(curr_pos[0] - prev_pos[0]) + abs(curr_pos[1] - prev_pos[1])
        movement = sum(abs(curr - prev) for curr, prev in zip(curr_pos, prev_pos))

        # print(movement)

        if movement > threshold:
            shake_count += 1
        else:
            shake_count = max(0, shake_count - 1)

        prev_pos = curr_pos
        time.sleep(0.15)

        if shake_count >= 3:
            return True


def get_cursor_pos() -> tuple[int, int]:
    curr_pos = win32api.GetCursorPos()
    return curr_pos[0], curr_pos[1]
