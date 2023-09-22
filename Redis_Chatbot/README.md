# Redis_Chatbot

This chatbot leverages Redis's Pub/Sub mechanisms to enable real-time messaging. It is built by integrating Redis with Python.

### Unique Features
This chatbot offers an experience akin to iMessage or Instagram's messaging service. As long as you're in a channel, you can receive live messages. Once you leave the channel, you won't receive any further messages. This adds a layer of real-time interactivity that goes beyond the basic Pub/Sub structure, where you would otherwise need to subscribe and unsubscribe from channels manually.

### Instructions
To engage with this chatbot, you must first run the `docker-compose` file located in this directory to set up two containers: one for Python and another for Redis. This also establishes the network connection between the two containers.

After successfully running the `docker-compose` file, simply execute `python3 Redis_Chatbot.py` in your terminal.

You will be presented with the following instructions:

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
        
![Screenshot 2023-09-22 at 17 58 14](https://github.com/Stonemannn/NoSQL-projects/assets/97291369/6f8605da-79a1-4a02-8f4f-c68ca34de405)
![Screenshot 2023-09-22 at 17 58 47](https://github.com/Stonemannn/NoSQL-projects/assets/97291369/0f606660-1265-4bc9-a074-a8e2796f681a)
![Screenshot 2023-09-22 at 17 59 03](https://github.com/Stonemannn/NoSQL-projects/assets/97291369/ec17fbce-e4e6-4fed-901e-644268698c67)
![Screenshot 2023-09-22 at 17 59 16](https://github.com/Stonemannn/NoSQL-projects/assets/97291369/f7faf421-2cf8-49b5-a325-90c922e94dd6)
![Screenshot 2023-09-22 at 17 59 41](https://github.com/Stonemannn/NoSQL-projects/assets/97291369/3928a57d-232b-41d2-8a29-5a45f4c81b7f)
![Screenshot 2023-09-22 at 18 00 43](https://github.com/Stonemannn/NoSQL-projects/assets/97291369/2851c637-2747-4236-85e9-5762f3e22e6f)
![Screenshot 2023-09-22 at 18 01 05](https://github.com/Stonemannn/NoSQL-projects/assets/97291369/425a4ec2-2f4b-48ca-841d-c4fda5722694)



