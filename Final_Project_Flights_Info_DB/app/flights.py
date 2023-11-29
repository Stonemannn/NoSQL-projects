import neo4j
import pandas as pd

driver = neo4j.GraphDatabase.driver(uri="neo4j://0.0.0.0:7687", auth=("neo4j", "password"))
session = driver.session(database="neo4j")


# Importing a csv file using the LOAD CSV command
# MERGE does a MATCH and does NOT modify the matched subgraph (data) if matched
# If no subgraph exists, MERGE creates it

# NOTE: IMPORT DATA FIRST
query = '''
    MATCH (origin:City)
    RETURN count(origin) AS cityCount
'''
result = session.run(query).single()
if result['cityCount'] > 0:
    print('Data already imported')
else:
    query = '''
        LOAD CSV WITH HEADERS FROM 'file:///australia_domestic_flights.csv' AS row
        WITH row
        WHERE row.City1 IS NOT NULL AND row.City2 IS NOT NULL AND row.Distance_GC_km <> '0' 
            AND row.Year < '2020' AND row.Year > '2000'
        MERGE (origin:City {name: row.City1})
        MERGE (destination:City {name: row.City2})
        MERGE (flight_info:Flight {
            month: toInteger(row.Month_num),
            year: toInteger(row.Year),
            passenger_trips: toInteger(row.Passenger_Trips),
            aircraft_trips: toInteger(row.Aircraft_Trips),
            passenger_load_factor: toFloat(row.Passenger_Load_Factor),
            available_seat_km: toFloat(row.ASKs),
            revenue_passenger_km: toFloat(row.RPKs),
            seats: toInteger(row.Seats),
            between: [row.City1, row.City2]
        })
        MERGE (origin)-[distance:DISTANCE_TO {number: toInteger(row.Distance_GC_km)}]->(destination)
        MERGE (origin)-[:HAS_FLIGHT]->(flight_info)
        MERGE (flight_info)-[:FLEW_TO]->(destination)
        MERGE (destination)-[:HAS_FLIGHT]->(flight_info)
        MERGE (flight_info)-[:FLEW_TO]->(origin)
    '''
    session.run(query)


def run_query_to_pandas(session, query, **kwargs): 
    # run a query and return the results in a pandas dataframe
    
    result = session.run(query, **kwargs) # dictionary of arguments
    # session.run(query, name='Tom Hanks', source='New York', target='Nashville', type='Person')
    
    df = pd.DataFrame([r.values() for r in result], columns=result.keys())
    
    return df


def run_query_print_raw(session, query):
    result = session.run(query)
    
    for r in result:
        print(r.values())



# ------------------------------------------------------------------------------------------------------------------------
# Given cityA and cityB, print out the distance between cityA and cityB.
def retrieve_distance(cityA, cityB):
    query = f'''
    MATCH (origin: City {{name: '{cityA}'}})-[distance:DISTANCE_TO]-(destination: City {{name: '{cityB}'}})
    RETURN distance.number AS distance
    '''

    df = run_query_to_pandas(session, query)
    print(df)
    print()

# Testing
# retrieve_distance('BRISBANE', 'SYDNEY')
# retrieve_distance('SYDNEY', 'BRISBANE')

#  Given cityA, cityB, year, month, print out the specific flight information between cityA and cityB in that month and year.
def retrieve_flight_info(cityA, cityB, year, month):
    query = f'''
    MATCH (origin: City {{name: '{cityA}'}})-[:HAS_FLIGHT]->(flight_info:Flight)-[:FLEW_TO]->(destination: City {{name: '{cityB}'}})
    WHERE flight_info.year = {year} AND flight_info.month = {month}
    RETURN flight_info.passenger_trips AS passenger_trips, 
        flight_info.aircraft_trips AS aircraft_trips, 
        flight_info.passenger_load_factor AS passenger_load_factor, 
        flight_info.available_seat_km AS available_seat_km, 
        flight_info.revenue_passenger_km AS revenue_passenger_km, 
        flight_info.seats AS seats
    '''
    df = run_query_to_pandas(session, query)
    print(df)
    print()

# Testing
# retrieve_flight_info( 'ADELAIDE','BRISBANE', 2011, 1)
# retrieve_flight_info( 'BRISBANE','ADELAIDE',2011, 1)

# Given CityA, Year, Month, print out the top 10 cities that have the most flights between CityA in that month and year.
def retrieve_top10_cities_by_flight_num(cityA, year, month):
    query = f'''
    MATCH (origin: City {{name: '{cityA}'}})-[:HAS_FLIGHT]->(flight_info)-[:FLEW_TO]->(destination: City)
    WHERE flight_info.year = {year} AND flight_info.month = {month}
           AND origin <> destination
    RETURN destination.name AS destination, flight_info.aircraft_trips AS aircraft_trips
    ORDER BY flight_info.aircraft_trips DESC
    LIMIT 10
    '''
    df = run_query_to_pandas(session, query)
    print(f'Top 10 cities that have the most flights between CityA {year}/{month}:')
    print(df)
    print()

# Testing
# retrieve_top10_cities_by_flight_num('MELBOURNE', 2011, 1)

# Given CityA, Year, Month, print out the top 10 cities that have the most passenger trips between CityA in that month and year.
def retrieve_top10_cities_by_passenger_num(cityA, year, month):
    query = f'''
    MATCH (origin: City {{name: '{cityA}'}})-[:HAS_FLIGHT]->(flight_info)-[:FLEW_TO]->(destination: City)
    WHERE flight_info.year = {year} AND flight_info.month = {month}
            AND origin <> destination
    RETURN destination.name AS destination, flight_info.passenger_trips AS passenger_trips
    ORDER BY flight_info.passenger_trips DESC
    LIMIT 10
    '''
    df = run_query_to_pandas(session, query)
    print(f'Top 10 cities that have the most passengers between CityA {year}/{month}:')
    print(df)
    print()

# Testing
# retrieve_top10_cities_by_passenger_num('MELBOURNE', 2011, 1)

# Given CityA, Year, Month, print out the top 10 cities that have the most passenger load factor between CityA in that month and year.
def retrieve_top10_cities_by_passenger_load_factor(cityA, year, month):
    query = f'''
    MATCH (origin: City {{name: '{cityA}'}})-[:HAS_FLIGHT]->(flight_info)-[:FLEW_TO]->(destination: City)
    WHERE flight_info.year = {year} AND flight_info.month = {month}
            AND origin <> destination
    RETURN destination.name AS destination, flight_info.passenger_load_factor AS passenger_load_factor
    ORDER BY flight_info.passenger_load_factor DESC
    LIMIT 10
    '''
    df = run_query_to_pandas(session, query)
    print(f'Top 10 cities that have the most passenger load factor between CityA {year}/{month}:')
    print(df)
    print()

# # Testing
# retrieve_top10_cities_by_passenger_load_factor('MELBOURNE', 2011, 1)

# Given CityA, CityB, Year, print out the statistics of passenger trips between CityA and CityB in that year.
def retrieve_annual_passenger_num_statistics(cityA, cityB, year):
    query = f'''
    MATCH (origin: City {{name: '{cityA}'}})-[:HAS_FLIGHT]->(flight_info)-[:FLEW_TO]->(destination: City {{name: '{cityB}'}})
    WHERE flight_info.year = {year}
    RETURN sum(flight_info.passenger_trips) AS total_passenger_trips,
            avg(flight_info.passenger_trips) AS average_passenger_trips,
            max(flight_info.passenger_trips) AS max_passenger_trips,
            min(flight_info.passenger_trips) AS min_passenger_trips
    '''
    df = run_query_to_pandas(session, query)
    print(f'The statistics of passenger trips between CityA and CityB in {year}:')
    print(df)
    print()

# Testing
# retrieve_annual_passenger_num_statistics('MELBOURNE', 'BRISBANE', 2011)

# Given CityA, CityB, Year, print out the statistics of passenger load factor between CityA and CityB in that year.
def retrieve_annual_passenger_load_factor_statistics(cityA, cityB, year):
    query = f'''
    MATCH (origin: City {{name: '{cityA}'}})-[:HAS_FLIGHT]-(flight_info)-[:FLEW_TO]-(destination: City {{name: '{cityB}'}})
    WHERE flight_info.year = {year}
    RETURN sum(flight_info.passenger_load_factor) AS total_passenger_load_factor,
            avg(flight_info.passenger_load_factor) AS average_passenger_load_factor,
            max(flight_info.passenger_load_factor) AS max_passenger_load_factor,
            min(flight_info.passenger_load_factor) AS min_passenger_load_factor,
            count(flight_info.passenger_load_factor) AS count_passenger_load_factor
    '''
    df = run_query_to_pandas(session, query)
    print(f'The statistics of passenger load factor between {cityA} and {cityB} in {year}:')
    print(df)
    print()

# Testing
# retrieve_annual_passenger_load_factor_statistics('MELBOURNE', 'BRISBANE', 2012)
# retrieve_annual_passenger_load_factor_statistics('MELBOURNE', 'BRISBANE', 2013)
# retrieve_annual_passenger_load_factor_statistics('MELBOURNE', 'BRISBANE', 2014)
# retrieve_annual_passenger_load_factor_statistics('MELBOURNE', 'BRISBANE', 2015)


# Given CityA, CityB, Distance, Update the distance between CityA and CityB in that month and year.
def update_distance(cityA, cityB, distance):
    query = f'''
    MATCH (origin: City {{name: '{cityA}'}})-[distance:DISTANCE_TO]-(destination: City{{name: '{cityB}'}})
    SET distance.number = {distance}
    RETURN origin.name AS origin, destination.name AS destination, distance.number AS distance
    '''
    session.run(query)
    print(f'Updated distance between {cityA} and {cityB}: {distance}')
    print()

# Testing
# retrieve_distance('MELBOURNE', 'BRISBANE')
# update_distance('MELBOURNE', 'BRISBANE', 1000)
# retrieve_distance('MELBOURNE', 'BRISBANE')

# Given CityA, CityB, Year, Month, Create new flight information between CityA and CityB in that month and year.
def create_new_flight_info(cityA, cityB, year, month, passenger_trips, aircraft_trips, seats):
    query = f'''
    MATCH (origin:City {{name: '{cityA}'}})-[distance:DISTANCE_TO]-(destination:City {{name: '{cityB}'}})
    MERGE (flight_info:Flight {{
        year: {year},
        month: {month},
        between: ['{cityA}', '{cityB}'],
        passenger_trips: {passenger_trips},
        passenger_load_factor: toFloat({passenger_trips})/toFloat({seats})*100,
        aircraft_trips: {aircraft_trips},
        available_seat_km: {seats}*distance.number,
        revenue_passenger_km: {passenger_trips}*distance.number,
        seats: {seats} }})
    MERGE (origin)-[:HAS_FLIGHT]->(flight_info)
    MERGE (flight_info)-[:FLEW_TO]->(destination)
    MERGE (destination)-[:HAS_FLIGHT]->(flight_info)
    MERGE (flight_info)-[:FLEW_TO]->(origin)
    RETURN flight_info.year AS year, 
        flight_info.month AS month, 
        flight_info.passenger_trips AS passenger_trips,
        flight_info.passenger_load_factor AS passenger_load_factor,
        flight_info.aircraft_trips AS aircraft_trips,
        flight_info.available_seat_km AS available_seat_km,
        flight_info.revenue_passenger_km AS revenue_passenger_km,
        flight_info.seats AS seats
    '''
    print(f'Created new flight information between {cityA} and {cityB} in {year}/{month}')
    df = run_query_to_pandas(session, query)
    print(df)
    print()

# # Testing
# retrieve_flight_info('MELBOURNE', 'BRISBANE', 2030, 5)
# create_new_flight_info('MELBOURNE', 'BRISBANE', 2030, 5, 2000, 10, 20000)

# Given CityA, CityB, Year, Month, Delete the flight information between CityA and CityB in that month and year.
def delete_flight_info(cityA, cityB, year, month):
    query = f'''
    MATCH (origin:City {{name: '{cityA}'}})-[:HAS_FLIGHT]->(flight_info:Flight)-[:FLEW_TO]->(destination:City {{name: '{cityB}'}})
    WHERE flight_info.year = {year} AND flight_info.month = {month}
    DETACH DELETE flight_info
    '''
    session.run(query)
    print(f'Deleted flight information between {cityA} and {cityB} in {year}/{month}')
    print()

# Testing
# retrieve_flight_info('MELBOURNE', 'BRISBANE', 2011, 5)
# delete_flight_info('MELBOURNE', 'BRISBANE', 2011, 5)
# retrieve_flight_info('MELBOURNE', 'BRISBANE', 2011, 5)

def retrieve_shortest_distance(cityA, cityB):
    # Set the boolean flag as the second parameter to false 
    # so that the procedure fails silently on non-existing graphs
    query = "CALL gds.graph.drop('flights_graph', false)"
    session.run(query)

    # Create a projection in Neo4j memory first before we can do anything interesting with it...
    query = '''CALL gds.graph.project('flights_graph',
        'City',
        {
        DISTANCE_TO: {
            type: 'DISTANCE_TO',
            orientation: 'UNDIRECTED',
            properties: 'number'}
        }
    )
    '''
    session.run(query)

    query = f"""

    MATCH (source:City {{name: '{cityA}'}}), (target:City {{name: '{cityB}'}})
    CALL gds.shortestPath.dijkstra.stream(
        'flights_graph', 
        {{ sourceNode: source, 
        targetNode: target, 
        relationshipWeightProperty: 'number'
        }}
    )
    YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
    RETURN
        gds.util.asNode(sourceNode).name AS from,
        gds.util.asNode(targetNode).name AS to,
        totalCost,
        [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS nodes,
        costs
    ORDER BY index

    """
    df = run_query_to_pandas(session, query, source=cityA, target=cityB)
    print(df)
    print()

# Testing
# retrieve_shortest_distance('NEWMAN', 'SYDNEY')