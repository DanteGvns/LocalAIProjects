import ollama



instructions  ="""
You are an event parser. From the user's natural language input, extract exactly these fields as a JSON object:

- event_category: The primary subject of the event. Key=(["event_category": common names/references}), pick one (["CIS 351": CIS 351, Computer Organization], ["CIS 343": CIS 343, Structure of Programming Languages], ["STA 215": STA 215, Intro Applied Statistics, Stats], ["CIS 656": CIS 656, Distributed Systems], ["CIS 554": CIS 554, Computer Networking], ["UFP": UFP, Internship, job, the office], ["GVSU": GVSU, GV, Grand Valley State University, campus, College of Computing])

- event_details: What is happening at the event, pick one ("Meeting", "Homework", "Assignment", "Work", "Fun", "Other")

- date: Convert natural language dates into MM/DD/YYYY format.
  Use the provided "Todays date/time is: MM/DD/YYYY HH:MM" as the reference.
  Examples:
    - "tomorrow" → reference_date + 1 day
    - "next Tuesday" → next occurrence of Tuesday after reference_date
    - "this Friday" → upcoming Friday on or after reference_date
    - "in two days" → reference_date + 2 days

- time: Convert natural language time into HH:mm 24-hour format.

If any field cannot be determined, set it to "unknown". Output ONLY the JSON object with no extra text.
"""


def parseEvent(model: str, prompt: str) -> str:
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": prompt},
    ]

    response = ollama.chat(model=model, messages=messages)
    return response["message"]["content"]
