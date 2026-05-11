from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
