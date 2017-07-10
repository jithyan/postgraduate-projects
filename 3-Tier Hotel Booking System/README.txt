Attempted: HD Level
Implemented: 3 hotels (two in one city), luhn validation, broker and client.

To setup:
================================================================
* Don't run the compiled files immediately. In order for the system
to work, run all the hotel servers, the broker and finally the client.

----------
CLIENT
----------

1. Go to Client dir. 

2. To compile:
 javac ClientStarter.java

3. To run the client:
 java ClientStarter


-----------
BROKER
-----------
1. Go to HotelBroker\src dir

2. To compile:
 javac BrokerTester.java

3. Create a separate folder and copy all the class files into it.

4. Copy all the files from the BrokerTester\rsc into the above folder.

5. To run the broker:
 java BrokerTester


---------------
HOTEL SERVERS
---------------
1. Create 3 new folders, you can call them holidayinn, grandhyatt and ritzcarlton 
(the folder names are for identifying the hotels, and don't affect the running of the program).

2. Go to HotelServer\src dir

3. Compile the java files:
 javac Tester.java

4. Copy all the resulting class files into each of the three folders created previously.

5. Copy all the files in the HotelServer\rsc folder into the above three folders as well. 

6. To run the server, it needs a port number as an argument.
There are three hotels (which are the folder names in step 1). 
The port numbers for each hotel are listed in HotelBroker\rsc\hotel_server_info.txt 

The server also needs the sqlite jdbc included in the classpath. The sqlite jar is included in
the rsc folder (which you should have copied).

To run:
 java -cp "sqlite-jdbc-3.8.11.2.jar;" Tester [port number]

The port numbers for the respective hotels are:
Grand Hyatt Hotel (Melbourne) : 5889
Ritz Carlton Hotel (Melbourne) : 5999
Holiday Inn (Perth) : 5992


---------
To use
---------
After setting up all the classes and resource files into their own folders,
run the broker and all the hotel servers, each in separate terminals.
There should be 4 terminals displaying a running server at this point.

The hotel server will create a new database.

All 4 servers should display "Server has started listening...", indicating they're ready to accept connections.

Then start a new terminal to run the client.


----------
Issues
----------
* In my own special tests, I've found that having more than 10 concurrent requests to a hotel server
causes "database busy" exceptions. I suspect, based on my research,  it's to do with the way I'm openning 
multiple connections. I haven't had time to resolve this issue.

* Sometimes when making a booking/checking vacancy, the system hangs. I've found restarting all the servers fixes it.

