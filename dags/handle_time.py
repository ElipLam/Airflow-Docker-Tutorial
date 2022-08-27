from datetime import datetime
import pandas as pd


def get_datetime_now():
    today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    # return str(today)
    return today


# print("Today's date:", today)
if __name__ == "__main__":
    print(get_datetime_now())
    print(type(get_datetime_now()))
    datetime_object = datetime.strptime(get_datetime_now(), "%Y-%m-%d %H:%M:%f")
    year = datetime_object.year
    month = datetime_object.month
    day = datetime_object.day
    df = pd.DataFrame([[year, month, day]])
    df.to_csv(f"{year}_{month}_{day}.csv")
    print(year, month, day)
    pass
