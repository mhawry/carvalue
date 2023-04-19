import pandas as pd
from flask import current_app


class Car:
    def __init__(self, year: int, make: str, model: str) -> None:
        self.year = year
        self.make = make
        self.model = model

    def get_name(self) -> str:
        """Return the car name (year, make, and model) as a single string"""
        return f"{self.year} {self.make} {self.model}"

    def find_similar(self) -> pd.DataFrame:
        """Generate a DataFrame of cars with the same year, make, and model

        Returns
        -------
        pandas.DataFrame
            A DataFrame of cars with the same year, make, and model
        """
        engine = current_app.config['DB_ENGINE']

        query = 'SELECT vin, year, make, model, trim, listing_price, listing_mileage, dealer_city, dealer_state FROM cars WHERE year = %(year)s AND LOWER(make) = %(make)s AND LOWER(model) = %(model)s'
        params = {
            'year': self.year,
            'make': self.make.lower(),
            'model': self.model.lower(),
        }
        df = pd.read_sql_query(sql=query, con=engine, params=params).dropna()

        # those need to be ints (they are floats by default)
        df['listing_price'] = df['listing_price'].astype(int)
        df['listing_mileage'] = df['listing_mileage'].astype(int)

        return df

    @staticmethod
    def fetch_existing_makes() -> list:
        """Fetch the makes for which we have data in our database

        Returns
        -------
        list
            A list of makes
        """
        df = pd.read_sql_query(sql='SELECT LOWER(make) AS make FROM makes',
                               con=current_app.config['DB_ENGINE'])

        return df['make'].values

    @staticmethod
    def fetch_existing_models() -> list:
        """Fetch the models for which we have data in our database

        Returns
        -------
        list
            A list of models
        """
        df = pd.read_sql_query(sql='SELECT LOWER(model) AS model FROM models',
                               con=current_app.config['DB_ENGINE'])

        return df['model'].values
