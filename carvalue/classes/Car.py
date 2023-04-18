import pandas as pd
from flask import current_app


class Car:
    def __init__(self, year: int, make: str, model: str) -> None:
        self.year = year
        self.make = make
        self.model = model

    def get_name(self) -> str:
        """Returns the car name (year, make, and model) as a single string"""
        return f"{self.year} {self.make.capitalize()} {self.model.capitalize()}"

    def find_similar(self) -> pd.DataFrame:
        """Generates a DataFrame of cars with the same year, make, and model

        Returns
        -------
        pandas.DataFrame
            A DataFrame of cars with the same year, make, and model
        """
        engine = current_app.config['DB_ENGINE']

        query = 'select vin, year, make, model, trim, listing_price, listing_mileage, dealer_city, dealer_state from cars where year = %(year)s AND LOWER(make) = %(make)s AND LOWER(model) = %(model)s'
        params = {
            'year': self.year,
            'make': self.make,
            'model': self.model,
        }
        df = pd.read_sql_query(query, con=engine, params=params).dropna()

        # those need to be ints (they are floats by default)
        df['listing_price'] = df['listing_price'].astype(int)
        df['listing_mileage'] = df['listing_mileage'].astype(int)

        return df
