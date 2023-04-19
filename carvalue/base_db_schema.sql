CREATE TABLE public.cars
(
    vin                       TEXT NOT NULL
        UNIQUE,
    year                      SMALLINT,
    make                      TEXT,
    model                     TEXT,
    trim                      TEXT,
    dealer_name               TEXT,
    dealer_street             TEXT,
    dealer_city               TEXT,
    dealer_state              CHAR(2),
    dealer_zip                TEXT,
    listing_price             INTEGER,
    listing_mileage           INTEGER,
    used                      TEXT,
    certified                 TEXT,
    style                     TEXT,
    driven_wheels             TEXT,
    engine                    TEXT,
    fuel_type                 TEXT,
    exterior_color            TEXT,
    interior_color            TEXT,
    seller_website            TEXT,
    first_seen_date           TEXT,
    last_seen_date            DATE,
    dealer_vdp_last_seen_date DATE,
    listing_status            TEXT
);

CREATE INDEX cars_year_index on cars USING btree (year);
CREATE INDEX cars_make_index ON cars USING btree (make);
CREATE INDEX cars_model_index ON cars USING btree (model);
CREATE UNIQUE INDEX cars_vin_key ON cars USING btree (vin);

CREATE MATERIALIZED VIEW public.makes AS
SELECT DISTINCT cars.make
FROM cars
WHERE cars.make IS NOT NULL;

ALTER MATERIALIZED VIEW public.makes OWNER TO carvalue;

CREATE MATERIALIZED VIEW public.models AS
SELECT DISTINCT cars.model
FROM cars
WHERE cars.model IS NOT NULL;

ALTER MATERIALIZED VIEW public.models OWNER TO carvalue;
