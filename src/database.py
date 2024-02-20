import sqlite3, sys, utils
from tabulate import tabulate

LOGGER = utils.LOGGER

# ==============================================================================================================
def create_tables():
    '''
    Initializes the empty tables.

    Parameter(s): None

    Output(s): 
        Bool: returns true if the tables are created, else returns false
    '''
    
    try:
        with sqlite3.connect('Skylar.db') as conn:      

            c = conn.cursor()
            # Force forgein key support
            c.execute("PRAGMA foreign_keys = ON;")

            # Customer Elements
            LOGGER.info("Creating Customer Table...")
            c.execute("""CREATE TABLE Customer(
                    cid INTEGER PRIMARY KEY AUTOINCREMENT,
                    cname TEXT,
                    address TEXT,
                    city TEXT,
                    state TEXT
            )""")
        
            # Customer contact information
            LOGGER.info("Creating ContactInfo Table...")
            c.execute("""CREATE TABLE ContactInfo(
                    cid INTEGER,
                    type TEXT, 
                    value TEXT,
                    PRIMARY KEY (cid, type, value),
                    FOREIGN KEY (cid) REFERENCES Customer(cid)
            )""")

            # Owner information
            LOGGER.info("Creating Owner Table...")
            c.execute("""CREATE TABLE Owner(
                    Oid INTEGER PRIMARY KEY AUTOINCREMENT,
                    oname TEXT
            )""")

            # Restaurant information
            LOGGER.info("Creating Restaurant Table...")
            c.execute("""CREATE TABLE Restaurant(
                    rid INTEGER PRIMARY KEY AUTOINCREMENT,
                    rname TEXT,
                    city TEXT,
                    state TEXT,
                    rating TEXT,
                    ownerID INTEGER,
                    FOREIGN KEY (ownerID) REFERENCES Owner(Oid)
            )""")

            # Reservation information
            LOGGER.info("Creating Reservation Table...")
            c.execute("""CREATE TABLE Reservation(
                    cid INTEGER,
                    rid INTEGER,
                    date TEXT,
                    num_adults INTEGER,
                    num_child INTEGER,
                    PRIMARY KEY (cid, rid),
                    FOREIGN KEY (cid) REFERENCES Customer(cid),
                    FOREIGN KEY (rid) REFERENCES Restaurant(rid)
            )""")

            conn.commit()
        
        return True
        
    except Exception as e:
        LOGGER.error(f"An error occured when creating tables: {e}")

# ==============================================================================================================
def clear_tables():
    '''
    Clears all the data from the tables.

    Parameter(s): None

    Output(s): 
        Bool: returns true if the tables are wiped, else returns false
    '''

    try:
        with sqlite3.connect('Skylar.db') as conn:
            c = conn.cursor()

            # Customer Elements
            LOGGER.info("Deleting Data From Customer Table...")
            c.execute("DELETE FROM Customer")
        
            # Customer contact information
            LOGGER.info("Deleting Data From ContactInfo Table...")
            c.execute("DELETE FROM ContactInfo")

            # Owner information
            LOGGER.info("Deleting Data From Owner Table...")
            c.execute("DELETE FROM Owner")

            # Restaurant information
            LOGGER.info("Deleting Data From Restaurant Table...")
            c.execute("DELETE FROM Restaurant")

            # Reservation information
            LOGGER.info("Deleting Data From Reservation Table...")
            c.execute("DELETE FROM Reservation")

            conn.commit()

        return True
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occurred when deleting all records from the tables: {e}")
        return False

# ==============================================================================================================
def print_tables():
    '''
    Prints the contents of Skylar

    Parameter(s): None

    Output(s):
        Prints tables to command terminal
    '''

    with sqlite3.connect('Skylar.db') as conn:
            c = conn.cursor()

            # Print Customer table data
            print("Customer Table Data:")
            c.execute("SELECT * FROM Customer")
            customers = c.fetchall()
            print(tabulate(customers, headers=["cid", "cname", "address", "city", "state"], tablefmt="grid"))

            # Print ContactInfo table data
            print("ContactInfo Table Data:")
            c.execute("SELECT * FROM ContactInfo")
            contacts = c.fetchall()
            print(tabulate(contacts, headers=["cid", "type", "value"], tablefmt="grid"))

            # Print Owner table data
            print("Owner Table Data:")
            c.execute("SELECT * FROM Owner")
            owners = c.fetchall()
            print(tabulate(owners, headers=["Oid", "oname"], tablefmt="grid"))

            # Print Restaurant table data
            print("Restaurant Table Data:")
            c.execute("SELECT * FROM Restaurant")
            restaurants = c.fetchall()
            print(tabulate(restaurants, headers=["rid", "rname", "city", "state", "rating", "ownerID"], tablefmt="grid"))

            # Print Reservation table data
            print("Reservation Table Data:")
            c.execute("SELECT * FROM Reservation")
            reservations = c.fetchall()
            print(tabulate(reservations, headers=["cid", "rid", "date", "num_adults", "num_child"], tablefmt="grid"))

            conn.commit()

# ==============================================================================================================
def db_query(query:str):
    '''
    Executes a user defined CRUD operation in the database

    Parameter(s):
        query (str): user defined 

    Output(s):
        repsonse (list, default=[]): a list of tuples containing the relanvent data to the query, else an 
        empty list if the query fails or the query isn't a SELECT type (create, update, or delete)
    '''
    response = []

    try:
        with sqlite3.connect('Skylar.db') as conn:
            c = conn.cursor()

            LOGGER.info(f"Executing Query:\n{query}")
            c.execute(query)

            # Get selected data if there is any
            if query.strip().upper().startswith('SELECT'):
                response = c.fetchall()

            conn.commit()

        return response
    
    except sqlite3.Error as e:
        LOGGER.error(f"An error occurred when executing the query {query}: {e}")
        return response

# ==============================================================================================================
def insert_customer(cname:str, address:str, city:str, state:str):
    '''
    Inserts the customer data in the database
    
    Parameter(s):
        cname (str): customer name
        address (str): the street address of the customer's home
        city (str): the city in which the customer resides
        state (str): the state in which the customer lives
    
    Output(s)
        A primary key (int) that represents the customer in the Customer table if added, else None
    '''

    try:
        with sqlite3.connect('Skylar.db') as conn:      

            c = conn.cursor()
            c.execute("INSERT INTO Customer (cname, address, city, state) VALUES (?,?,?,?)", (cname, address, city, state))
            conn.commit()

            key = c.lastrowid
        
            return key
        
    except Exception as e:
        LOGGER.error(f"An error occured when inserting into Customer table: {e}")
        return None

# ==============================================================================================================
def insert_contact(key:int, type:str, value:str):
    '''
    Inserts the contact information of a customer
    
    Parameter(s):
        key (int): the primary key referencing the customer
        type (str): the contact type such as an email or phone number
        value (str): an email address or phone number
    
    Output(s):
        True if the contact is successfully added, else false
    '''

    try:
        with sqlite3.connect('Skylar.db') as conn:      

            c = conn.cursor()
            c.execute("INSERT INTO ContactInfo (cid, type, value) VALUES (?,?,?)", (key, type, value))
            conn.commit()
        
        return True
        
    except Exception as e:
        LOGGER.error(f"An error occured when inserting into ContactInfo table: {e}")
        return False
    
# ==============================================================================================================
def insert_owner(oname:str):
    '''
    Inserts the owner data into the database
    
    Parameter(s):
        oname (str): name of the owner
    
    Output(s):
        A primary key (int) that represents the owner in the Owner table if added, else None
    '''

    try:
        with sqlite3.connect('Skylar.db') as conn:      

            c = conn.cursor()
            c.execute("INSERT INTO Owner (oname) VALUES (?)", (oname))
            conn.commit()

            key = c.lastrowid
        
            return key
        
    except Exception as e:
        LOGGER.error(f"An error occured when inserting into Owner table: {e}")
        return None

# ==============================================================================================================
def insert_restaurant(rname:str, city:str, state:str, rating:int, ownerID:int):
    '''
    Inserts the reservation data into the database
    
    Parameter(s):
        rname (str): name of the restaurant
        city (str): city in which the restaurant is located
        state (str): state in which the restaurant is located
        rating (int): the customer rating of the restaurant
        ownerID (int): the primary key of the owner of the restaurant
        
    Output(s):
        True if the restaurant is successfully added, else false
    '''

    try:
        with sqlite3.connect('Skylar.db') as conn:

            c = conn.cursor()
            c.execute("INSERT INTO Restaurant (rname, city, state, rating, ownerID) VALUES (?,?,?,?,?)", (rname, city, state, rating, ownerID))
            conn.commit()
        
        return True
        
    except Exception as e:
        LOGGER.error(f"An error occured when inserting into Reservation table: {e}")
        return False

# ==============================================================================================================
def insert_reservation(cid:int, rid:int, date:str, num_adults:int, num_child:int):
    '''
    Inserts the reservation data into the database
    
    Parameter(s):
        cid (int): customer primary key
        rid (int): restaurant primary key
        data (str): day and time the reservantion is placed
        num_adults (int): the number of adults attending
        num_child (int): the number of children attending
        
    Output(s):
        True if the reservation is successfully added, else false
    '''

    try:
        with sqlite3.connect('Skylar.db') as conn:      

            c = conn.cursor()
            c.execute("INSERT INTO Reservation (cid, rid, date, num_adults, num_child) VALUES (?,?,?,?,?)", (cid, rid, date, num_adults, num_child))
            conn.commit()
        
        return True
        
    except Exception as e:
        LOGGER.error(f"An error occured when inserting into Reservation table: {e}")
        return False

# ==============================================================================================================
if __name__ == "__main__":
    '''
    Handles command line entries to manually set the database tables

    Parameter(s): 
        Two system arguments that include a input flag: 
        python ./init_db.py [flag]

    flag(s):
        Create tables, "-c", initializes the Flashcard and Figure tables
        Clear tables, "-d", deletes all the rows in both tables
        Print tables, "-p", prints all the rows in both tables

    Output(s): None
    '''

    # python .\phylogeny.py input_file
    if(len(sys.argv) != 2):
        print(f"Only two inputs allowed, {len(sys.argv)} were entered!")

    # Create Tables
    if(sys.argv[1] == "-c"): create_tables()
    # Delete Tables
    elif(sys.argv[1] == "-d"): clear_tables()
    # Print Tables
    elif(sys.argv[1] == "-p"): print_tables()

    else:
        print("Invalid Arguments!\nCreate Tables: -c\nDelete Tables: -d\n")