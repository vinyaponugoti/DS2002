import pandas as pd
import sqlite3

# Benchmark 1.1: Ingesting a pre-defined data source
# Data File from Kaggle: https://www.kaggle.com/datasets/thespacefreak/taylor-swift-spotify-data?resource=download
# This is a csv that contains spotify data about Taylor Swift's songs including the song and album names and scores for certain characteristics such as popularity, loudness, danceability that spotify rates the song on based off their own internal data
tswift_data = pd.read_csv('spotify_taylorswift.csv')


# Benchmark 1.3: Modifying the number of columns from the source to the destination and transforming the columns
# Deleting the unnamed column from the dataset
tswift_data.rename({"Unnamed: 0":"indices"}, axis="columns", inplace=True)
tswift_data.drop(["indices"], axis=1, inplace=True)
# Adding column that states length of song in minutes and deletes the original length in miliseconds column
tswift_data['length_mins'] = (tswift_data['length']/60000).round(2) 
tswift_data.drop(["length"], axis=1, inplace=True)
# Renaming name column to song name
tswift_data.rename({"name":"song name"}, axis="columns", inplace=True)



# Benchmark 1.2: Converting the general format of the source
# Benchmark 1.4: Writing converted file to the disk
# Benchmark 2.1: Produce informative errors
# Has user input the file format they want to receive the data in
choice = input("\nPick which format to convert data to: CSV, JSON, or SQL\nTo convert to CSV: Type CSV and hit enter.\nTo convert to JSON: Type JSON and hit enter\nTo convert to SQL: Type SQL and hit enter\n")

if choice == "JSON": # Converting to JSON the file will be located locally in json_tswift_data.json
    try:
        tswift_data.to_json('json_tswift_data.json', orient='records', indent = 2)
        print("Conversion Successful. The JSON output is in json_tswift_data.json")
    except:
        print("An exception occured. File wasn't able to be transformed to JSON format")
elif choice == "CSV": # Converting to CSV the file will be located locally in csv_tswift_data.csv
    try:  
        tswift_data.to_csv('csv_tswift_data.csv',index=False)
        print("Conversion Successful. The CSV output is in csv_tswift_data.csv")
    except:
        print("An exception occured. File wasn't able to be transformed to CSV format")
elif choice == "SQL": # Converting to SQL the file will be located locally in tswift_database.db
    try:
        conn = sqlite3.connect('tswift_database.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS tswift (song name,album,artist,release_date,popularity,danceability,acousticness,energy,instrumentalness,liveness,loudness,speechiness,valence,tempo,length_mins)')
        conn.commit()
        tswift_data.to_sql('tswift', conn, if_exists='replace', index = False)
        print("Conversion Successful. The SQL output is in tswift_database.db")
        view = input("To view the contents of the database type yes otherwise type no and hit enter\n")
        if view == "yes":
            c.execute('''  SELECT * FROM tswift  ''')
            for row in c.fetchall():
                print (row)
    except:
        print("An exception occured. File wasn't able to be transformed to SQL format")
else: # If user doesn't enter JSON, CSV, or SQL exactly then this exception will be raised 
    raise Exception("Only JSON, CSV, or SQL allowed as input")

# Benchmark 1.5: Brief summary about data including number of records and columns
print("The transformed data file has",len(tswift_data), "records")
print("The transformed data file has",len(tswift_data.columns), "columns")
    
