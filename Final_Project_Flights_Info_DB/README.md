# Domestic Flight Information Database System (Australia) - Neo4j

## Overview
This project is a database system for domestic flight information in Australia. The database is built on Neo4j and the data is from [Australian Government, data.gov.au](https://data.gov.au/data/dataset/c5029f2a-39b3-4aef-8ae1-73e7962f6170/resource/677d307f-6a1f-4de4-9b85-5e1aa7074423/download/dom_citypairs_web.csv). The database contains monthly flight information between two cities. Below is an example piece of data.

| City1    | City2        | Month | Passenger_Trips | Aircraft_Trips | Passenger_Load_Factor | Distance_GC_km | RPKs     | ASKs     | Seats | Year | Month_num |
|----------|--------------|-------|-----------------|----------------|-----------------------|----------------|----------|----------|-------|------|-----------|
| ADELAIDE | ALICE SPRINGS| Jan-84| 15743           | 143            | 81.8                  | 1316           | 20717788 | 25327369 | 19246 | 1984 | 1         |
| ADELAIDE | BRISBANE     | Jan-84| 3781            | 32             | 89.8                  | 1622           | 6132782  | 6829379  | 4210  | 1984 | 1         |
| ADELAIDE | CANBERRA     | Jan-84| 1339            | 12             | 94.7                  | 972            | 1301508  | 1374348  | 1414  | 1984 | 1         |
| ADELAIDE | DARWIN       | Jan-84| 3050            | 33             | 66.8                  | 2619           | 7987950  | 11958009 | 4566  | 1984 | 1         |

I choose Neo4j database for storing this dataset. Reason: graph is perfect for representing the relation between two entities (cities). And the attributes could be the number of passanger_trips and aircraft_trips between two cities.

## Supported Queries
- Retrieve the distance between two cities

`python3 run-app.py retrieve_distance SYDNEY BRISBANE`

`python3 run-app.py retrieve_distance BRISBANE SYDNEY`

- retrieve the flight information between two cities in a specific month

`python3 run-app.py retrieve_flight_info ADELAIDE BRISBANE 2011 1`

`python3 run-app.py retrieve_flight_info BRISBANE ADELAIDE 2011 1`

- retrieve the top 10 cities by passenger number in a specific month

`python3 run-app.py retrieve_top10_cities_by_passenger_num MELBOURNE 2011 1`

- retrieve the top 10 cities by passenger load factor in a specific month

`python3 run-app.py retrieve_top10_cities_by_passenger_load_factor MELBOURNE 2011 1`

- retrieve annual passenger number statistics between two cities in a specific year

`python3 run-app.py retrieve_annual_passenger_num_statistics MELBOURNE BRISBANE 2011`

- retrieve annual passenger load factor statistics between two cities in a specific year

`python3 run-app.py retrieve_annual_passenger_load_factor_statistics MELBOURNE BRISBANE 2011`

- update the distance between two cities

`python3 run-app.py retrieve_distance MELBOURNE BRISBANE`

`python3 run-app.py update_distance MELBOURNE BRISBANE 1000`

`python3 run-app.py retrieve_distance MELBOURNE BRISBANE`

- create new flight information between two cities in a specific month

`python3 run-app.py retrieve_flight_info MELBOURNE BRISBANE 2030 5`

`python3 run-app.py create_new_flight_info MELBOURNE BRISBANE 2030 5 2000 10 20000`

`python3 run-app.py retrieve_flight_info MELBOURNE BRISBANE 2030 5`

- delete flight information between two cities in a specific month

`python3 run-app.py retrieve_flight_info MELBOURNE BRISBANE 2011 5`

`python3 run-app.py delete_flight_info MELBOURNE BRISBANE 2011 5`

`python3 run-app.py retrieve_flight_info MELBOURNE BRISBANE 2011 5`

- retrieve the shortest distance between two cities

`python3 run-app.py retrieve_shortest_distance NEWMAN SYDNEY`

`python3 run-app.py retrieve_shortest_distance SYDNEY NEWMAN`
