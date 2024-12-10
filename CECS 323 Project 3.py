from pymongo import MongoClient
import certifi

# Mongo connection setup

# localhost:27017
try:
    #connection_string = str(input("Input your connection string: "))
    connection_string = "mongodb://localhost:27017/" # connect locally
    # Create MongoDB client
    client = MongoClient(connection_string)
    db = client['project3']

    # Collections within database
    artists = db['artists']
    concerts = db['concerts']
    seats = db['seats']
    tickets = db['tickets']
    venues = db['venues']

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
        query_num = int(input("Please enter: "))  # Ensure the input is an integer
        #query_num = 2
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 4.")
        continue

    if query_num == 1:
        # Print out each state that has at least one venue, and also 
        # include the number of venues in that state in your printout.
        print("--- QUERY 1 ---\n")
        for info in (venues.aggregate([{'$group': {'_id': '$state','venueCount': {'$sum': 1}}}])):
            print(f"State: {info['_id']} | Venues Amount: {info['venueCount']}")

        print("\n")

    elif query_num == 2:
        # Input the name of an Artist.
        # Print the title, date, venue name, venue city, and venue state 
        #   of all concerts in which an artist with the given name played.
        # Print out the concerts one per line.
        print("--- QUERY 2 ---\n")
        artist_input =  str(input("Please enter artist name(LA Phil, Taylor Swift, Kendrick Lamar, Drake): "))

        myPipeline = [
            {'$match': {'performers.artist.name': artist_input}},

            #base on match, project the info [some from concert / some from venue objects]
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
        # Print out all the sum cost of all tickets sold for any venue section 
        # that is titled "General Admission" at a venue in the state of 'CA'. 
        # Show the sum per section.
        print("--- QUERY 3 ---\n")

        myPipeline = [
        {'$unwind': {'path': '$sections'}},
        {'$match': {'state': 'CA', 'sections.title': 'General Admission'}},
        {'$unwind': {'path': '$sections.seats'}},
        {'$lookup': {'from': 'tickets', 'localField': 'sections.title', 'foreignField': 'seat.sectionTitle', 'as': 'result'}},
        {'$unwind': {'path': '$result'}},
        {'$group': {'_id': {'venueName': "$name", 'sectionTitle': "$result.seat.sectionTitle"},
        'total': {'$sum': "$result.price"}}},
        {'$project': {'name': '$_id.venueName', 'sectionTitle':'$_id.sectionTitle', 'total':1}}
        ]

        result = venues.aggregate(myPipeline)

        for info in result:
            print(f"{info['name']} - {info['sectionTitle']} - ${info['total']}")
        print("\n")
    elif query_num == 4:
        print("Exiting program...")
        break
    else:
        print("Invalid choice, please select a valid number (1-4).")
