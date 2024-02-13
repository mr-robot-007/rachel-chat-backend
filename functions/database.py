import json
import random
# Get recent messages
def get_recent_messages():

    # Define the file naem and learn instruction
    file_name = 'stored_data.json'
    learn_instruction = {
        "role": "system",
        "content":"You are a voice assisant named Rachel and your job is to answer question and communicate with the user. Only answer question in maximum of 30 words and talk professionally. "
    }

    # Initialize messages
    messages = []

    # Add a random element
    # x = random.uniform(0,1)
    # if x < 0.5:
    #     learn_instruction["content"] = learn_instruction["content"] + "Your response will include some dry humour"
    # else:
    #     learn_instruction["content"] = learn_instruction["content"] + "Your response will include a rather challenging question"

    # Append instruction to message
    messages.append(learn_instruction)

    # Get last messages
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

            # print("data from line 30: ",data)

            #  Append last 5 items of data
            if data:
                # print("if execcuted") # it will not execute if data is empty {}
                if len(data) < 5:
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-5:]:
                        messages.append(item)
        
    except Exception as e:
        pass


    # Return 
    return messages

# Store Messages
def store_messages(request_message,response_message):
    
    # Define the file name
    file_name = "stored_data.json"

    # Get recent messages ( get all message except first one because it automatically get added when user makes request)
    messages = get_recent_messages()[1:]


    # Add messages to data
    user_message = {"role":"user","content":request_message}
    assistant_message = {"role":"assistant","content":response_message}
    messages.append(user_message)
    messages.append(assistant_message)

    # Save the updated file/ write message to json file
    with open(file_name,"w") as f:
        json.dump(messages,f)



# Reset messages
def reset_messages():

    # Overwrite current file with nothing 
    open("stored_data.json","w") 
    