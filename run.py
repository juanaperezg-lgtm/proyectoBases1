from tkinter import Tk

from app.ui.login_window import LoginWindow


def main() -> None:
    root = Tk()
    LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
