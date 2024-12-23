from prophet import Prophet
import pandas as pd

from config.config import Config

class Predictor:
    def __init__(self, conf, id, name):
        self.id = id
        self.name = name
        self.conf = conf
        self.model = Prophet(**conf)
        self.fpath = Config.RAWDATA_DIR.joinpath(str(self.id), "data.xlsx")

    def init(self):
        data = pd.read_excel(self.fpath)
        data = data.rename(columns={
            "date": "ds",
            "quantity": "y"
        })
        print(data.head())
        data["ds"] = pd.to_datetime(data["ds"])
        self.model.fit(data)

    def reload(self, id=None, name=None, conf=None):
        
        if id is not None:
            self.id = id
            self.fpath = Config.RAWDATA_DIR.joinpath(str(self.id), "data.xlsx")
        if name is not None:
            self.name = name
        if conf is not None:
            self.conf = conf
        self.model = Prophet(**self.conf)
        self.init()

    def predict(self, k=7):
        future = self.model.make_future_dataframe(periods=k)
        forecast = self.model.predict(future)
        fig1 = self.model.plot(forecast)
        fig1.savefig('temp1.png')
        fig2 = self.model.plot_components(forecast)
        fig2.savefig('temp2.png')
        return forecast

    def __eq__(self, value):
        if isinstance(value, Predictor):
            return self.id == value.id
        else:
            return self.id == value