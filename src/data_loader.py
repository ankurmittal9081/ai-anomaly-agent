import pandas as pd


def load_data(file_path):
    data = pd.read_excel(file_path)

    data["Date"] = pd.to_datetime(data["Date"])

    return data