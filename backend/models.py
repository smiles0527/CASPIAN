from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 20 sensor values (numeric, nullable)
    sensor_1 = Column(Float, nullable=True)
    sensor_2 = Column(Float, nullable=True)
    sensor_3 = Column(Float, nullable=True)
    sensor_4 = Column(Float, nullable=True)
    sensor_5 = Column(Float, nullable=True)
    sensor_6 = Column(Float, nullable=True)
    sensor_7 = Column(Float, nullable=True)
    sensor_8 = Column(Float, nullable=True)
    sensor_9 = Column(Float, nullable=True)
    sensor_10 = Column(Float, nullable=True)
    sensor_11 = Column(Float, nullable=True)
    sensor_12 = Column(Float, nullable=True)
    sensor_13 = Column(Float, nullable=True)
    sensor_14 = Column(Float, nullable=True)
    sensor_15 = Column(Float, nullable=True)
    sensor_16 = Column(Float, nullable=True)
    sensor_17 = Column(Float, nullable=True)
    sensor_18 = Column(Float, nullable=True)
    sensor_19 = Column(Float, nullable=True)
    sensor_20 = Column(Float, nullable=True)

    feelings = Column(Text, nullable=True)
    insights = Column(Text, nullable=True)
    care_plan = Column(Text, nullable=True)

    def to_dict(self):
        sensors = {f"sensor_{i}": getattr(self, f"sensor_{i}") for i in range(1, 21)}
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            **sensors,
            "feelings": self.feelings,
            "insights": self.insights,
            "care_plan": self.care_plan,
        }

    def sensors_as_list(self):
        return [getattr(self, f"sensor_{i}") for i in range(1, 21)]
