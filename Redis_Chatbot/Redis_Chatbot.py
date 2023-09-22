import redis
import json
import random
import threading

# Static data
weather_data = {}
for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    temperature = random.randint(0, 100)  # Generates a random integer between 0 and 100
    weather_data[letter] = f"{temperature}°F"


fun_facts = ['Honey never spoils.', 'Octopuses have three hearts.']

# Function to return weather data
def get_weather(city):
    return weather_data.get(city, 'Weather data not available for this city. \n City should be one capital letter.')

def get_fun_fact():
    return random.choice(fun_facts)

# The chatbot can recognize the following special commands 
# and provide automated responses to them
def handle_command(command):
    if command.startswith('!help'):
        return "Available commands: !help, !weather <city>, !fact, !whoami"
    
    elif command.startswith('!weather'):
        _, city = command.split(' ', 1)
        return get_weather(city)
        
    elif command.startswith('!fact'):
        return get_fun_fact()
        
    elif command.startswith('!whoami'):
        return f'You are {bot.username}.'
    
    else:
        return 'Unknown command. Type !help for a list of available commands.'

class Chatbot:
    def __init__(self, host='my-redis', port=6379):
        self.client = redis.StrictRedis(host=host, port=port)
        self.pubsub = self.client.pubsub()
        self.introduce()
        self.username = None
        self.current_channel = None  # Add this line

    def introduce(self):
        intro = """
        Hi! I'm your friendly Redis Chatbot.
        Here are the commands this bot supports:
        !help: List of commands
        !weather <city>: Weather update
        !fact: Random fun fact
        !whoami: Your user information
        """
        print(intro)

    # User Identification
    def identify(self, username, age, gender, location):
        self.username = username
        self.client.hset(f"user:{username}", mapping={
            "age": age,
            "gender": gender,
            "location": location
        })
        print(f"Hello, {username}! You've been identified.")


    # Channels
    def join_channel(self, channel):
        self.pubsub.subscribe(channel)
        self.current_channel = channel 
        print(f"Listening to {channel}.")
        thread = threading.Thread(target=self.listen_to_channel, args=(channel,))
        thread.daemon = True  # set the thread as a daemon so it will exit when the main program does
        thread.start()
        self.chat_in_channel()

    def listen_to_channel(self, channel):
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                print(f"[{channel}] {message['data'].decode('utf-8')}")

    def chat_in_channel(self):
        print(f"Type your messages for the channel {self.current_channel}. Press Ctrl + C to exit.")
        try:
            while True:
                message = input()
                self.send_message(self.current_channel, message)
        except KeyboardInterrupt:
            print("\nExiting the channel.")
            self.leave_channel(self.current_channel)
            self.current_channel = None  # Reset current_channel


    def send_message(self, channel, message):
        message_obj = {
            'message from': self.username,
            'message': message
        }
        self.client.publish(channel,json.dumps(message_obj))


    def leave_channel(self, channel):
        # Leave a channel
        # Unsubscribe from the channel
        self.pubsub.unsubscribe(channel)
        print(f"Left from {channel}.")




    def get_user_info(self, user):
        user_key = f"user:{user}"
        age = bot.client.hget(user_key, 'age').decode('utf-8')
        gender = bot.client.hget(user_key, 'gender').decode('utf-8')
        location = bot.client.hget(user_key, 'location').decode('utf-8')
        print(f'Info for {user}: Username: {user}, Age: {age}, Gender: {gender}, Location: {location}')







if __name__ == "__main__":
    # Chatbot Initialization 
    bot = Chatbot()
    
    while True:
        print("""
        Options:
        1: Identify yourself
        2: Join a channel
        3: Send a message to a channel
        4: Get info about a user
        5: Exit
        """)

        choice = input('Enter your choice: ')

        # In case of invalid input
        if choice.startswith('!'):
            print(handle_command(choice))

        elif choice == "1":
            username = input('Enter your username: ')
            age = input('Enter your age: ')
            gender = input('Enter your gender: ')
            location = input('Enter your location: ')
            bot.identify(username, age, gender, location)

        elif choice == '2':
            channel = input('Enter the channel number you want to join: ')
            bot.join_channel(channel)

        elif choice == '3':
            channel = input('Enter the channel number you want to send a message: ')
            message = input('Enter the message you want to send: ')
            bot.send_message(channel, message)     

        # In case the invalid input
        elif choice == '4':
            user = input('Enter the user name: ')

            if not bot.client.exists(f"user:{user}"):
                print(f"User name {user} does not exist.")
            else:
                bot.get_user_info(user)
        
        elif choice == '5':
            print('Adios, my friend!')
            break



















