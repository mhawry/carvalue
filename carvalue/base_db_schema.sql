create table public.cars
(
    vin                       text not null
        unique,
    year                      smallint,
    make                      text,
    model                     text,
    trim                      text,
    dealer_name               text,
    dealer_street             text,
    dealer_city               text,
    dealer_state              char(2),
    dealer_zip                text,
    listing_price             integer,
    listing_mileage           integer,
    used                      text,
    certified                 text,
    style                     text,
    driven_wheels             text,
    engine                    text,
    fuel_type                 text,
    exterior_color            text,
    interior_color            text,
    seller_website            text,
    first_seen_date           text,
    last_seen_date            date,
    dealer_vdp_last_seen_date date,
    listing_status            text
);
