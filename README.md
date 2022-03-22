<h1>About the Project</h1>

A simple trivia game using <a href="https://opentdb.com/api_config.php">Open Trivia DB</a>

<h2>Process</h2>

Pulls random trivia covering a wide range of topics that a user will choose upon start of the game. The answers are pulled into one dictionary, shuffled, and presented to the user with the related question. 

<h2>Libraries</h2>

<b>requests</b>: used to access the API and request the relevant data.

<b>json</b>: Used to read the json data from the requested data.

<b>random</b>: Shuffles the correct and incorrect answers.

<b>html</b>: Using .unescape to format the text to exclude html characters (i.e. &quot).

<b>Typing</b>: Typehinting
