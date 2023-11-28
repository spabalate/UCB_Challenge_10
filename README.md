# UCB_Challenge_10
# sqlalchemy-challenge

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area. 

Part 1: Analyze and Explore the Climate Data
Used Python and SQLAlchemy to do a basic climate analysis and data exploration of the climate database. Used SQLAlchemy ORM queries, Pandas, and Matplotlib.

Precipitation Analysis
- Found the most recent date in the dataset.
- Using that date, gathered the previous 12 months of precipitation data by querying the previous 12 months of data.
- Loaded the query results into a Pandas DataFrame. Explicitly set the column names.
- Sorted the DataFrame values by "date".
- Plotted the results by using the DataFrame plot method, as the following image shows:
- Used Pandas to print the summary statistics for the precipitation data.

Station Analysis:
- Designed a query to calculate the total number of stations in the dataset.
- Designed a query to find the most-active stations
- Designed a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
- Designed a query to get the previous 12 months of temperature observation (TOBS) data. 
A screenshot depicts the histogram.

Part 2: Design Your Climate App
- Designed a Flask API based on the queries that you just developed. 
- List all the available routes.
- Converted the query results from the precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
- Returned the JSON representation of your dictionary.
- Returned a JSON list of stations from the dataset.
- Queried the dates and temperature observations of the most-active station for the previous year of data.
- Returned a JSON list of temperature observations for the previous year.
- Returned a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
