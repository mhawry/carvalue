import os
import pandas
import math
from . import db
from .classes.Car import Car
from flask import Flask, render_template, request, g
from sklearn.linear_model import LinearRegression

MIN_YEAR_VALUE = 1980  # the lowest value for year in our dataset
MAX_YEAR_VALUE = 2025  # the highest value for year in our dataset
MAX_RESULTS = 100  # the maximum number of cars to display on the results page


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY={os.environ.get('APP_SECRET_KEY')},
        DB_ENGINE=f"postgresql+psycopg2://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_HOST')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}",
    )
    db.init_app(app)

    @app.route('/', methods=['GET', 'POST'])
    def index() -> str:
        g.form_errors = []

        if request.method == 'POST':
            validated_form = validate_form(request.form['car_name'], request.form['mileage'])

            # if there are errors in the form
            if validated_form is None:
                return render_template('search/index.html', car_name=request.form['car_name'], mileage=request.form['mileage'])

            year, make, model, mileage = validated_form

            # at this point we are ready to instantiate the Car object and pull similar car values from the database
            car = Car(year, make, model)
            cars_df = car.find_similar()

            # in case we don't have any data on the car
            if cars_df.empty:
                g.form_errors.append(f"Sorry, we don't have any data for {car.get_name()}")
                return render_template('search/index.html', car_name=car.get_name(), mileage=request.form['mileage'])

            estimate = estimate_value(cars_df, mileage)
            results = cars_df[:MAX_RESULTS]

            return render_template('search/results.html', car_name=car.get_name(), mileage=mileage, estimate=estimate, results=results)

        return render_template('search/index.html')

    def estimate_value(cars_df: pandas.DataFrame, mileage: int = None) -> int:
        """Estimates the value of a car based on similar cars and mileage (if provided)

        Parameters
        ----------
        cars_df : pandas.DataFrame
            A DataFrame containing sample data on similar cars
        mileage : int, Optional
            The position side (SIDE_BUY or SIDE_SELL)

        Returns
        -------
        int
            The estimated value rounded up to the nearest hundredth
        """
        # if the mileage is provided, use linear regression to predict the value
        if mileage:
            x = cars_df[['listing_mileage']]
            y = cars_df['listing_price']

            linear_regression_model = LinearRegression()
            linear_regression_model.fit(x, y)

            estimate = linear_regression_model.predict([[mileage]])
        else:
            estimate = cars_df['listing_price'].mean()  # no mileage was provided, use the mean instead

        # the estimate needs to be rounded up to the nearest hundredth
        return int(math.ceil(estimate / 100.0)) * 100

    def validate_form(car: str, mileage: str) -> list or None:
        car = car.strip().lower()

        # in case someone decides to use a "," or "." in the mileage
        mileage = mileage.strip().replace(',', '').replace('.', '')

        if not car:
            g.form_errors.append("You need to specify a car")
            return

        # this is to make sure the value for car contains at least three parts
        try:
            year, make, model = car.split(maxsplit=2)  # TODO what if the make has a space in it?
        except ValueError:
            g.form_errors.append("The provided value for car is invalid. Please make sure to include the year, make, and model")
            return

        if year.isdigit():
            year = int(year)
        else:
            g.form_errors.append("Please enter a valid year")
            return

        if year < MIN_YEAR_VALUE or year > MAX_YEAR_VALUE:
            g.form_errors.append(f"The year needs to be between {MIN_YEAR_VALUE} and {MAX_YEAR_VALUE} (inclusively)")
            return

        # mileage needs to either be an int or empty
        if mileage.isdigit():
            mileage = int(mileage)
        elif mileage:
            g.form_errors.append("Invalid value for mileage")
        else:
            mileage = None

        return year, make, model, mileage

    return app


app = create_app()
