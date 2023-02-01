

# Jobsity Data Engineering Challenge

This is a simple API that ingests trips data in csv format, stores it and gives an endpoint to consume a weekly average metric.

API is written with Flask, data is stored in a PostgreSQL database with PostGIS extension. This API has the option to scale for up to 100 million records.

## Running locally

This API is meant to be used with docker-compose. To run it, execute:

```bash
docker-compose up
# Or alternatively run as daemon: docker-compose up -d
```

This command will download and build the images, perform an initial database setup, and expose the API on port 5000.

## Configuration

You can adjust database name, user and password in `.env` file.

You can also set the option `ENABLE_EMAIL_NOTIFICATION` to something not empty, and the API will notify you via email when the ingestion is done. In order for this to happen you have to specify all the EMAIL/STMP options.

## Available endpoints

 - `/trips` (POST)

This endpoint expects a file to be sent via `file` form parameter. File must be in csv format, here is an example of valid contents:

```csv
region,origin_coord,destination_coord,datetime,datasource
Prague,POINT (14.4973794438195 50.00136875782316),POINT (14.43109483523328 50.04052930943246),2018-05-28 09:03:40,funny_car
Turin,POINT (7.672837913286881 44.9957109242058),POINT (7.720368637535126 45.06782385393849),2018-05-21 02:54:04,baba_car
Prague,POINT (14.32427345662177 50.00002074358429),POINT (14.47767895969969 50.09339790740321),2018-05-13 08:52:25,cheap_mobile
Turin,POINT (7.541509189114433 45.09160503827746),POINT (7.74528653441973 45.02628598341506),2018-05-06 09:49:16,bad_diesel_vehicles
```

Example request, assuming we have a correctly formatted csv file called `trips.csv`:

```bash
$ curl http://127.0.0.1:5000/trips -F file=@trips.csv
{"message":"file uploaded successfully, inserted 100 rows"}
```

 - `/trips/weekly_average` (GET)

This endpoint calculates a weekly average number of trips. It expects either a region or a bounding box defined by two points.

Example of a request that calculates a weekly average number of trips for of a region:

```bash
$ curl -XGET http://127.0.0.1:5000/trips/weekly_average?region=Prague
{"weekly_average":"6.80"}
```

To get a weekly average of trips in a bounding box you must specify two points via `xmin`, `ymin`, `xmax` and `ymax` parameters. A trip will be within a bounding box if both origin and destination are within that box. Example:

```bash
$ curl -XGET http://127.0.0.1:5000/trips/weekly_average?xmin=7.5415091&ymin=45.091605&xmax=10.0588964&ymax=53.4948642
{"weekly_average":"1.50"}
```


## Other resources in this repository

 - `helper_scipts/augment_data.py` is a script that can help you generate more data from a given csv file. It works by repeating the contents of a given csv file N times.

For example, running this command will repeat the contents of trips.csv 100 times and store the results in output.csv:

```bash
python helper_scipts/augment_data.py trips.csv output.csv 100
```

 - `example_queries`: in this directory you can find some example queries you can run directly against the database.

