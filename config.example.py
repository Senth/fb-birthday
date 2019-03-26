email = 'your@email.com'
password = 'yourpassword'

# $ is replaced with the first name of the person
default_messages = {
    'english': [
        'Happy Birthday, $! :D',
        "Happy Birthday, $! :) Hope you'll have a wonderful day!",
    ],
    'swedish': [
        'Grattis på födelsedagen $! :D',
        'Grattis på födelsedagen $! :D Hoppas du får en fin dag! :)',
    ],
}

messages = {
    'John Doe': "Happy birthday, John! :D Hope you'll have a great day :)",
    'Sara Doe': 'english',
    'Andreas Svensson': 'swedish',
}
