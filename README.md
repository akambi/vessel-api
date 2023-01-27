Vessel trips
==========================

This project provides a way to track vessel positions. It contains an API that inserts vessel positions in the database

How to use it?
============

API

[GET] http://localhost/api/v1/vessels/positions?dateFrom=2017-11-01&dateTo=2017-11-18

This endpoint returns a list of vessel positions bethween two dates.

[POST] http://localhost/api/v1/vessels/positions

This endpoint is used to insert new vessel's position in the system. You must provide the following parameters

- vessel_id (`Integer`)
- received_time_utc (`Datetime`)
- latitude (`Float`)
- longitude (`Float`)

To test the API, you can use Postman.
You can also run the test.py in the api service with `docker-compose exec kp-backend python api/test.py`

