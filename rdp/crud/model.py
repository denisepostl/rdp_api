from typing import List
from sqlalchemy import ForeignKey, UniqueConstraint

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class ValueType(Base):
    __tablename__ = "value_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[str]
    type_unit: Mapped[str]

    values: Mapped[List["Value"]] = relationship(
        back_populates="value_type", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"ValueType(id={self.id!r}, value_type={self.type_name})"

class Value(Base):
    __tablename__ = "value"
    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[int] = mapped_column()
    value: Mapped[float] = mapped_column()
    value_type_id: Mapped[int] = mapped_column(ForeignKey("value_type.id"))
    device_id: Mapped[int] = mapped_column(ForeignKey("device.id"))

    value_type: Mapped["ValueType"] = relationship(back_populates="values")
    device: Mapped["Device"] = relationship(back_populates="values")

    __table_args__ = (
        UniqueConstraint("time", "value_type_id", "device_id", name="value integrity"),
    )

    def __repr__(self) -> str:
        return f"Value(id={self.id!r}, value_time={self.time!r} value_type={self.value_type.type_name!r}, device={self.device.device},value={self.value})"

class Device(Base):
    __tablename__ = "device"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    device: Mapped[str]
    postalCode: Mapped[int]
    city: Mapped[str]
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"), nullable=True)

    room: Mapped["Room"] = relationship(back_populates="devices")
    values: Mapped[List["Value"]] = relationship(
        back_populates="device", cascade="all, delete-orphan"
    )

    __table_args__ = (UniqueConstraint("device", name="device integrity"),)


class Room(Base):
    __tablename__ = "room"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    room_nr: Mapped[int]
    location_id: Mapped[int] = mapped_column(
        ForeignKey("location.id"), nullable=True
    )

    devices: Mapped[List["Device"]] = relationship(
        back_populates="room", cascade="all, delete-orphan"
    )

    location: Mapped["Location"] = relationship(back_populates="rooms")

class Location(Base):
    __tablename__ = "location"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    city: Mapped[str]
    
    rooms: Mapped[List["Room"]] = relationship(
        back_populates="location", cascade="all, delete-orphan"
    )