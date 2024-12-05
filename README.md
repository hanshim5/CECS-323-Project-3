# CECS-323-Project-3
**Project 3: I Don't Actually Know Anything About Taylor Swift**
You may work on and submit this project with one other person.

**Overview**
In this project, you will translate the Project 1 UML solution into MongoDB collections, using JSON schemas that I will provide. You will expand the collections that I provide by designing a schema to store Users and the Inventories they own, as shown in the Project 1 UML solution. You will then write a short Python program using the PyMongo library, allowing a user to search the various objects in the database.

**Setting up the collections**
Use Compass to create a new database, "project3". Create collections for concerts, venues, artists, seats, and tickets.

Download and extract project3files.zip Download project3files.zipOpen this document with ReadSpeaker docReaderfrom Canvas to your local machine. Open the schemas folder. Copy and paste the contents of the Concerts.schema.json file into the Validation tab of the colors collection in Compass. (Click "Add Rule", then overwrite the text box by pasting the schema contents.) Do the same for the other schemas and collections.

You will want to review the schemas for each collection before moving on, and will refer to them when doing the next task.

**Analyzing the schemas**
Answer these questions about the schemas, and submit them along with the other project deliverables. Give your answers in complete English sentences; be thorough in your responses.

Give an example of a one-to-few relationship in the schemas. Do you agree that one-to-few was the appropriate model for this relationship? Explain.
Give an example of a one-to-squillions relationship in the schemas. Do you agree that one-to-squillions was the appropriate model for this relationship? Explain.
Give an example of a one-to-many relationship in the schemas. Do you agree that one-to-many was the appropriate model for this relationship? Explain.
 

**Inserting documents**
Begin by creating JSON documents for the following objects. The documents must match the schemas from the previous step.

You can do this by hand, or I will allow and encourage you to use a Large Language Model tool like ChatGPT to generate the objects. To use an LLM in this way, you should write a prompt explaining that you are providing a MongoDB $jsonSchema, and then paste one of the schemas into the prompt. Then ask the AI to generate a JSON object that matches the schema. Give the details of the object as an English sentence; like, "The Venue is named 'SoFi Stadium', and has sections named '100', '200', and '300'." 

Check the output of the AI, and use more prompts to guide it to correct any mistakes. For example, the above prompt could create a Venue with a City of "Long Beach"; you can use a second prompt to change that, like "Set the city of the venue to Los Angeles". You can also use follow-up prompts to add children to the object, for example, "add another Section to the Venue named '400'."

The AI can't do everything for you; it might leave placeholders for things like object IDs, which you will need to generate and replace by hand. It may use the wrong formatting for some values, for example, it might write ISODate("2023-12-01") for date objects, which is not what Mongo wants; you can fix this by asking it to use "$date" values for dates, "$oid" values for object IDs, etc. It won't be able to magically know the object ID of an object from a different collection. If you create an Artist named Michael and then try to add Michael to the performance list of a Concert, the AI might not know the object ID of Michael's artist object. Also, in this denormalized database design, sometimes there are two classes that each refer to each other: for example, a Section has a list of Seats, and each Seat identifies its Section. You won't be able to finish a Section object until all its Seats are created, and you won't be able to finish a Seat object until its Section exists... so you'll have to be clever about going back to edit objects that you made earlier.

If I ask you to create an object without specifying one of its fields, you can choose any reasonable value yourself.

Once an object is complete, use Compass to insert it into the correct collection. Compass will reject the insertion if the document does not match the schema, and you will need to work with the AI to figure out why and correct the issue. 

Create these objects, and then insert them into your Mongo database. I have bolded changes from the Project 1/2 objects.

Two Venues:
The Hollywood Bowl (an outdoor venue)
SoFi Stadium (an indoor venue)
Four Artists:
LA Phil
Taylor Swift
Kendrick Lamar
Drake
Two Tours:
LA Phil Summer Season
The Eras Tour
Four Concerts:
"The Eras Tour night 1"; with Taylor Swift, at SoFi Stadium, August 3 2023 8:00pm; part of The Eras Tour
"The Eras Tour night 2"; with Taylor Swift, at SoFi Stadium, August 4 2023 8:00pm; part of The Eras Tour
"Dudamel Leads Beethoven 9"; with LA Phil, at Hollywood Bowl, September 10 2024 4:30pm; part of the LA Phil Summer Season.
"What If?"; with Kendrick Lamar (first) and Drake (second), at SoFi Stadium, July 1 2026 10:00pm; not part of a tour.
Sections "Lower Box", "Upper Box", and "A" at the Hollywood Bowl.
Seats "Box A", "Box B" in Lower Box; seats "A1" and "A2" in section A.
Box A and Box B can sell up to 10 tickets per concert.
Seat "A1" and "A2" are obstructed viewing. Box B is accessible seating and in-seat attendant.
Sections "General Admission" at SoFi Stadium.
Seats "GA1" in "General Admission", with a maximum of 100 tickets.
Tickets to see What If?:
Seat GA1 for $500.
Seat GA1 for $202.
Tickets to see Dudamel Leads Beethoven 9:
Seat A1, for $50
Three tickets for Box A, at $200 each.

**Python application**
You must now write a Python application using PyMongo to interact with this concerts database.

Your application should begin with a Main Menu of these options:

State report
Print out each state that has at least one venue, and also include the number of venues in that state in your printout.
You must use only a single query. You cannot do any aggregation using Python application code, i.e., you can't loop through results from the database and count them yourself. The database must do all the work.
Artist search
Input the name of an Artist.
Print the title, date, venue name, venue city, and venue state of all concerts in which an artist with the given name played.
Print out the concerts one per line.
This query does not require a join.
General admission totals
Print out all the sum cost of all tickets sold for any venue section that is titled "General Admission" at a venue in the state of 'CA'. Show the sum per section.
This query requires:
filtering venues that are in CA
filtering sections in those venues that are titled 'General Admission', i.e., murdering sections that are not.
joining the sections to tickets from the section.
summing the prices of the tickets in the section
Print the results in the format Venue Name - Section Title - $TotalOfTicketPrices

**Deliverables**
You must deliver to me a printout containing the following documents:

Title page (name of course and section number, title of assignment, team member names, due date)
The document you created for SoFi stadium.
The document you created for the artist Taylor Swift.
The document you created for the "What If?" concert.
The ticket documents you created for the "What If?" concert.
Your answers to the analysis question.
The entire code of the Python application you were required to write. I should be able to run your program on my local machine.
