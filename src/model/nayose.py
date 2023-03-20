import os

import pandas as pd
from sqlalchemy import Column, Integer, String

if not __name__ == "__main__":
    from model.setting import Base, nayose_engine
else:
    from setting import Base, nayose_engine


class Nayose(Base):
    __tablename__ = "nayose"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reid = Column(Integer)
    name = Column(String)
    address = Column(String)
    prefecture = Column(String)
    city = Column(String)
    town = Column(String)
    timewalk = Column(Integer)
    housenum = Column(Integer)

    @classmethod
    def _init_data(cls):
        nayose_df = pd.read_csv(f"{os.getcwd()}/src/csv/nayose_raw - raw (1).csv")
        nayose_df["id"] = nayose_df.index
        nayose_trans_df = nayose_df[[k for k in vars(cls) if not k.startswith("_")]]

        nayose_trans_df.to_sql(
            cls.__tablename__, nayose_engine, index=False, if_exists="replace"
        )

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


if __name__ == "__main__":
    Nayose._init_data()