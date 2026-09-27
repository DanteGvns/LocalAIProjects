from datetime import datetime
from parseEvent import parseEvent


# set model to try
llmModel = "qwen2.5-coder:3b"

# Get the current date and time
currentDatetime = datetime.now().strftime("%m/%d/%Y %H:%M")
eventString = "I have a meeting with the college of computing on the 4th at 11:30am"

#Build our full formatted message for the LLM
eventMessage = "(Todays date/time is: " + currentDatetime +" )" + "Event to parse: " + eventString

def main():
    #see what date/time we are working with for debugging
    print(currentDatetime)
    #call the llm to parse our event string
    response = parseEvent(llmModel, eventMessage)
    print(response)

if __name__ == "__main__":
    main()