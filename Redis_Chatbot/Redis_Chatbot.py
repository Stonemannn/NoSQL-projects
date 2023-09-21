import redis
import json
import random

class Chatbot:
    def __init__(self, host='my-redis', port=6379):
        self.client = redis.StrictRedis(host=host, port=port)
        self.pubsub = self.client.pubsub()
        self.introduce()
        self.username = None

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

    def identify(self, username, age, gender, location):
        self.username = username
        self.client.hset(f"user:{username}", mapping={
            "age": age,
            "gender": gender,
            "location": location
        })
        print(f"Hello, {username}! You've been identified.")

    def join_channel(self, channel):
        # Join a channel
        channels_key = f'channels:{self.username}'
        self.client.sadd(channels_key, channel)

    def leave_channel(self, channel):
        # Leave a channel
        channels_key = f'channels:{self.username}'
        self.client.srem(channels_key, channel)

    def send_message(self, channel, message):
        message_obj = {
            'from': self.username,
            'message': message
        }
        self.client.publish(channel,json.dumps(message_obj))

    def read_message(self, channel):
        # Read messages from a channel
        self.pubsub.subscribe(channel)        

    def process_commands(self, message):
        # Handle special chatbot commands
        pass

    def direct_message(self, message):
        # Send a direct message to the chatbot
        pass

    def get_user_info(self, user):
        user_key = f"user:{user}"
        return self.client.hgetall(user_key)

if __name__ == "__main__":
    bot = Chatbot()
    
    while True:
        print("""
        Options:
        1: Identify yourself
        2: Join a channel
        3: Leave a channel
        4: Send a message to a channel
        5: Get info about a user
        6: Exit
        """)

        choice = input('Enter your choice: ')

        # In case of invalid input
        if choice not in map(str,range(1,7)):
            print('Invalid input! Please enter your choice again: ')

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
            channel = input('Enter the channel number you want to leave: ')
            bot.leave_channel(channel)            

        elif choice == '4':
            channel = input('Enter the channel number you want to send a message: ')
            message = input('Enter the message you want to send: ')
            bot.send_message(channel, message)     

        # In case the invalid input
        elif choice == '5':
            user = input('Enter the user name: ')

            if not bot.client.exists(f"user:{user}"):
                print(f"User name {user} does not exist.")
            
            else:
                age = bot.client.hget(f"user:{user}", 'age').decode('utf-8')
                gender = bot.client.hget(f"user:{user}", 'gender').decode('utf-8')
                location = bot.client.hget(f"user:{user}", 'location').decode('utf-8')

                bot.get_user_info(user)
                print(f'Info for {user}: Username: {user}, Age: {age}, Gender: {gender}, Location: {location}')

        elif choice == '6':
            print('Goodbye, my friend!')




# if __name__ == "__main__":
#     bot = Chatbot()

#     while True:
#         print("""
#         Options:
#         1: Identify yourself
#         2: Join a channel
#         3: Leave a channel
#         4: Send a message to a channel
#         5: Get info about a user
#         6: Exit
#         """)

#         choice = input("Enter your choice: ")

#         if choice == "1":
#             username = input("Enter your username: ")
#             age = input("Enter your age: ")
#             gender = input("Enter your gender: ")
#             location = input("Enter your location: ")
#             bot.identify(username, age, gender, location)

#         elif choice == "2":
#             channel = input("Enter channel name: ")
#             bot.join_channel(channel)

#         elif choice == "3":
#             channel = input("Enter channel name: ")
#             bot.leave_channel(channel)

#         elif choice == "4":
#             channel = input("Enter channel name: ")
#             message = input("Enter your message: ")
#             bot.send_message(channel, message)

#         elif choice == "5":
#             username = input("Enter username to get info about: ")
#             # Add implementation to fetch user info

#         elif choice == "6":
#             print("Goodbye!")
#             break
