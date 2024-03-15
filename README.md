# DS-SearchApp
Important Instructions

For optimal performance, ensure that you use Python 3.9 to execute this code, preferably version 3.9.13.

Initial (One-Time) Setup:

Open a terminal and enter the following command: "pip install -r requirements.txt".
Download PostgreSQL, launch the application, and confirm that the server is running.
Navigate to the 'utils' folder and execute 'twitter-users.ipynb'. Provide your system's username when prompted. Ensure that the dataset' is added to the 'utils' folder before running the file.
Run 'tweets_to_mongoDB.ipynb' in the 'utils' folder to verify the connection to the MongoDB cluster.
Running the API:

In the terminal, enter: "cd src" to change the working directory to the 'src' folder.
Start the API server by typing either "python -m uvicorn main:app --reload" or "python main.py" in the terminal.
Visit http://127.0.0.1:8000/docs to perform a search.
