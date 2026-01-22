#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2025, type=int, help='Year of the data')
@click.option('--month', default=11, type=int, help='Month of the data')
@click.option('--trips-table', default='green_taxi_trips', help='Green taxi trips table')
@click.option('--zones-table', default='taxi_zones', help='Taxi zones table')
def run(
    pg_user,
    pg_pass,
    pg_host,
    pg_port,
    pg_db,
    year,
    month,
    trips_table,
    zones_table,
):

    # PostgreSQL connection
    engine = create_engine(
        f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
    )

    # Green taxi trips (Parquet)
    trips_url = (
        f'https://d37ci6vzurychx.cloudfront.net/trip-data/'
        f'green_tripdata_{year}-{month:02d}.parquet'
    )

    print(f'Downloading green taxi trips from {trips_url}')
    df_trips = pd.read_parquet(trips_url)

    print('Writing green taxi trips to PostgreSQL...')
    df_trips.to_sql(
        name=trips_table,
        con=engine,
        if_exists='replace',
        index=False
    )

    # Taxi zones lookup (CSV)
    zones_url = (
        'https://github.com/DataTalksClub/nyc-tlc-data/'
        'releases/download/misc/taxi_zone_lookup.csv'
    )

    print(f'Downloading taxi zones from {zones_url}')
    df_zones = pd.read_csv(zones_url)

    print('Writing taxi zones to PostgreSQL...')
    df_zones.to_sql(
        name=zones_table,
        con=engine,
        if_exists='replace',
        index=False
    )

    print('Ingestion completed successfully')


if __name__ == '__main__':
    run()