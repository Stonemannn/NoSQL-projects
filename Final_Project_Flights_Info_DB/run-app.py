from argparse import ArgumentParser
from app.flights import * # retrieve_distance, retrieve_flight_info, retrieve_top10_cities_by_flight_num, retrieve_top10_cities_by_passenger_num, retrieve_top10_cities_by_passenger_load_factor, retrieve_annual_passenger_num_statistics, retrieve_annual_passenger_load_factor_statistics, update_distance, create_new_flight_info, delete_flight_info

def main():
    parser = ArgumentParser(description="CLI tool for multiple functions")
    
    subparsers = parser.add_subparsers(dest="command")

    # Parser for retrieve_flight_info
    parser_retrieve_flight_info = subparsers.add_parser("retrieve_flight_info")
    parser_retrieve_flight_info.add_argument("cityA", type=str, help="First city")
    parser_retrieve_flight_info.add_argument("cityB", type=str, help="Second city")
    parser_retrieve_flight_info.add_argument("year", type=int, help="Year")
    parser_retrieve_flight_info.add_argument("month", type=int, help="Month")

    # Parser for retrieve_distance
    parser_retrieve_distance = subparsers.add_parser("retrieve_distance")
    parser_retrieve_distance.add_argument("cityA", type=str, help="First city")
    parser_retrieve_distance.add_argument("cityB", type=str, help="Second city")

    # Parse for retrieve_top10_cities_by_flight_num
    parser_retrieve_top10_cities_by_flight_num = subparsers.add_parser("retrieve_top10_cities_by_flight_num")
    parser_retrieve_top10_cities_by_flight_num.add_argument("cityA", type=str, help="City")
    parser_retrieve_top10_cities_by_flight_num.add_argument("year", type=int, help="Year")
    parser_retrieve_top10_cities_by_flight_num.add_argument("month", type=int, help="Month")

    # Parse for retrieve_top10_cities_by_passenger_num
    parser_retrieve_top10_cities_by_passenger_num = subparsers.add_parser("retrieve_top10_cities_by_passenger_num")
    parser_retrieve_top10_cities_by_passenger_num.add_argument("cityA", type=str, help="City")
    parser_retrieve_top10_cities_by_passenger_num.add_argument("year", type=int, help="Year")
    parser_retrieve_top10_cities_by_passenger_num.add_argument("month", type=int, help="Month")

    # Parse for retrieve_top10_cities_by_passenger_load_factor
    parser_retrieve_top10_cities_by_passenger_load_factor = subparsers.add_parser("retrieve_top10_cities_by_passenger_load_factor")
    parser_retrieve_top10_cities_by_passenger_load_factor.add_argument("cityA", type=str, help="City")
    parser_retrieve_top10_cities_by_passenger_load_factor.add_argument("year", type=int, help="Year")
    parser_retrieve_top10_cities_by_passenger_load_factor.add_argument("month", type=int, help="Month")

    # Parser for retrieve_annual_passenger_num_statistics
    parser_retrieve_annual_passenger_num_statistics = subparsers.add_parser("retrieve_annual_passenger_num_statistics")
    parser_retrieve_annual_passenger_num_statistics.add_argument('cityA', type=str, help='CityA')
    parser_retrieve_annual_passenger_num_statistics.add_argument('cityB', type=str, help='CityB')
    parser_retrieve_annual_passenger_num_statistics.add_argument("year", type=int, help="Year")

    # Parser for retrieve_annual_passenger_load_factor_statistics
    parser_retrieve_annual_passenger_load_factor_statistics = subparsers.add_parser("retrieve_annual_passenger_load_factor_statistics")

    parser_retrieve_annual_passenger_load_factor_statistics.add_argument('cityA', type=str, help='CityA')
    parser_retrieve_annual_passenger_load_factor_statistics.add_argument('cityB', type=str, help='CityB')
    parser_retrieve_annual_passenger_load_factor_statistics.add_argument("year", type=int, help="Year")

    # Parser for update_distance
    parser_update_distance = subparsers.add_parser("update_distance")
    parser_update_distance.add_argument("cityA", type=str, help="First city")
    parser_update_distance.add_argument("cityB", type=str, help="Second city")
    parser_update_distance.add_argument("distance", type=int, help="Distance")

    # Parser for create_new_flight_info
    parser_create_new_flight_info = subparsers.add_parser("create_new_flight_info")
    parser_create_new_flight_info.add_argument("cityA", type=str, help="First city")
    parser_create_new_flight_info.add_argument("cityB", type=str, help="Second city")
    parser_create_new_flight_info.add_argument("year", type=int, help="Year")
    parser_create_new_flight_info.add_argument("month", type=int, help="Month")
    parser_create_new_flight_info.add_argument("passenger_trips", type=int, help="Passenger trips")
    parser_create_new_flight_info.add_argument("aircraft_trips", type=int, help="Aircraft trips")
    parser_create_new_flight_info.add_argument("seats", type=int, help="Seats")

    # Parser for delete_flight_info
    parser_delete_flight_info = subparsers.add_parser("delete_flight_info")
    parser_delete_flight_info.add_argument("cityA", type=str, help="First city")
    parser_delete_flight_info.add_argument("cityB", type=str, help="Second city")
    parser_delete_flight_info.add_argument("year", type=int, help="Year")
    parser_delete_flight_info.add_argument("month", type=int, help="Month")

    # Parser for retrieve_shortest_distance
    parser_retrieve_shortest_distance = subparsers.add_parser("retrieve_shortest_distance")
    parser_retrieve_shortest_distance.add_argument("cityA", type=str, help="First city")
    parser_retrieve_shortest_distance.add_argument("cityB", type=str, help="Second city")


    args = parser.parse_args()

    if args.command == "retrieve_flight_info":
        retrieve_flight_info(args.cityA, args.cityB, args.year, args.month)

    elif args.command == "retrieve_distance":
        retrieve_distance(args.cityA, args.cityB)

    elif args.command == "retrieve_top10_cities_by_flight_num":
        retrieve_top10_cities_by_flight_num(args.cityA, args.year, args.month)
    
    elif args.command == "retrieve_top10_cities_by_passenger_num":
        retrieve_top10_cities_by_passenger_num(args.cityA, args.year, args.month)
    
    elif args.command == "retrieve_top10_cities_by_passenger_load_factor":
        retrieve_top10_cities_by_passenger_load_factor(args.cityA, args.year, args.month)
    
    elif args.command == "retrieve_annual_passenger_num_statistics":
        retrieve_annual_passenger_num_statistics(args.cityA, args.cityB, args.year)
    
    elif args.command == "retrieve_annual_passenger_load_factor_statistics":
        retrieve_annual_passenger_load_factor_statistics(args.cityA, args.cityB, args.year)
    
    elif args.command == "update_distance":
        update_distance(args.cityA, args.cityB, args.distance)
    
    elif args.command == "create_new_flight_info":
        create_new_flight_info(args.cityA, args.cityB, args.year, args.month, args.passenger_trips, args.aircraft_trips, args.seats)
    
    elif args.command == "delete_flight_info":
        delete_flight_info(args.cityA, args.cityB, args.year, args.month)
    
    elif args.command == "retrieve_shortest_distance":
        retrieve_shortest_distance(args.cityA, args.cityB)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()

    ''' 
        Running app in debug mode
        It will trace errors if produced and display them
        Each time a change is made in code, the changes will reflect instantaneously. 
    '''
    # app.run(debug=True)