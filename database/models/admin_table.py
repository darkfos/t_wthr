from database.create_all_table import Base
from sqlalchemy.orm import Mapped, mapped_column

class AdminTable(Base):
    __tablename__ = "AdminTable"

    admin_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_name: Mapped[str]
    password: Mapped[str]

    def __init__(self, tg_name: Mapped[str], password: Mapped[str]):
        self.tg_name = tg_name
        self.password = password

    def __repr__(self):
        return f"Telegram name: {self.tg_name}, id: {self.admin_id}"