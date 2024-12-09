from pymongo import MongoClient
import certifi

# Mongo connection setup

#mongodb://localhost:27017/  <- Hannah's connection string
# localhost:27017 [kinoko connection]
try:
    #connection_string = str(input("Input your connection string: "))
    connection_string = "localhost:27017"
    # Create MongoDB client
    client = MongoClient(connection_string)
    db = client['project3']

    # Collections within database
    artists = db['artists']
    concerts = db['concerts']
    seats = db['seats']
    tickets = db['tickets']
    venues = db['venues']


    # FOR TESTING PURPOSES:
    # Print available collections
    # print("Mongo Collection names:")
    # print(db.list_collection_names())
    #
    # print("Sample data from artists collection:")
    # for doc in artists.find().limit(5):
    #     print(doc)

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()

while True:
    print("\nSelect a query number(1-3) or exit(4): \n   "
          "1. State report\n   "
          "2. Artist search\n   "
          "3. General admission totals\n   "
          "4. Exit\n")
    try:
        query_num = int(input("please enter: "))  # Ensure the input is an integer
        #query_num = 2
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 4.")
        continue

    if query_num == 1:
        #report = concerts.find({})
        print("--- QUERY 1 ---\n")
        #myPipeline = venues.aggregate([{'$group': {'_id': '$state','venueCount': {'$sum': 1}}}])
        #myResult = venues.aggregate(myPipeline)

        for info in (venues.aggregate([{'$group': {'_id': '$state','venueCount': {'$sum': 1}}}])):
            print(f"State: {info['_id']} | Venues Amount: {info['venueCount']}")

        print("\n")

    elif query_num == 2:
        print("QUERY 2\n")
        artist_input =  str(input("please enter artist name: "))

        myPipeline = [
            #CONCERT DATABASE

            #performers.artist.name : to match the input artist
            {'$match': {'performers.artist.name': artist_input}},

            #base on match, project the info [some from concert/ some frome venue objects]
            {'$project': {
                '_id': 0,
                'title': 1,
                'start': 1,
                'venue.name': 1,
                'venue.city': 1,
                'venue.state': 1
            }}
        ]

        for info in (concerts.aggregate(myPipeline)):
            print(f"Title: {info['title']}, Date: {info['start']}, Venue: {info['venue']['name']}, "
                  f"City: {info['venue']['city']}, State: {info['venue']['state']}")
        print("\n")

    elif query_num == 3:
        print("query 3\n")

        myPipeline = [
        {'$unwind': {'path': '$sections'}},
        {'$match': {'state': 'CA', 'sections.title': 'General Admission'}},
        {'$unwind': {'path': '$sections.seats'}},
        {'$lookup': {'from': 'tickets', 'localField': 'sections.title', 'foreignField': 'seat.sectionTitle', 'as': 'result'}},
        {'$unwind': {'path': '$result'}},
        {'$group': {'_id': '$name', 'total': {'$sum': '$result.price'}}}
        ]

        result = venues.aggregate(myPipeline)

        for info in result:
            print(f"Venue name: {info['_id']} ,total: {info['total']}")
        print("\n")
    elif query_num == 4:
        print("Exiting program...")
        break
    else:
        print("Invalid choice, please select a valid number (1-4).")
