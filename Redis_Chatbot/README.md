# Redis_Chatbot

This Chatbot uses Redis's Pub/Sub mechanism to realize  real-time messaging. I created this Chatbot by integrating Redis with Python.

### Instruction
To use this Chatbot for fun, you should first run the docker-compose file in this directory to create 2 containers: one is for python and the other one is or redis, including the network between these two containers.

After running the docker-compose file successfully, you can simply run command 'python3 Redis_Chatbot.py' in your terminal.

You will see following instruction:

        Hi! I'm your friendly Redis Chatbot.
        Here are the commands this bot supports:
        !help: List of commands
        !weather <city>: Weather update
        !fact: Random fun fact
        !whoami: Your user information
        

        Options:
        1: Identify yourself
        2: Join a channel
        3: Leave a channel
        4: Send a message to a channel
        5: Get info about a user
        6: Exit



