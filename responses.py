import random
import requests
import json

user_name = ''
nice_words = ["love", "adore", "like"]
curse_responses = ["Do you talk to your mother with that mouth?", "The world needs more kindness.", "You can do better than that.", "Gross.", "Yikes.", "And same to you."]
dog_words = ["dog", "puppy", "pupper", "pup", "doggo", "woofer", "good boi"]
goodbye_words = ["bye", "goodbye", "adios", "later"]
trivia_answer = ''

def boto_response(user_message):
    global user_name
    global trivia_answer
    split_msg = user_message.split()
    if is_name(user_message):
        return "ok", f"Hi {user_name}, nice to meet you!"
    elif "joke" in user_message:
        joke = get_joke()
        return "laughing", joke
    elif any(word in split_msg for word in dog_words):
        dog_fact = get_dog_fact()
        return "dog", dog_fact
    elif any(word in split_msg for word in nice_words):
        return "inlove", "Awwwww."
    elif "weather" in user_message:
        weather = get_weather()
        if "Rain" in weather:
            return "crying", f"In Tel Aviv, the temperature is {weather[0]}C. There is {weather[2]}."
        else:
            return "money", f"In Tel Aviv, the current weather is {weather[1]}. The temperature is {weather[0]}C."
    elif "date" in user_message:
        date = get_weather()[3]
        return "confused", f"The date is {date}."
    elif "time" in user_message:
        time = get_weather()[4]
        return "afraid", f"{time}."
    elif "trivia" in user_message:
        trivia_question = get_trivia_question()[0]
        return "excited", f"When you're ready to see the answer, type 'tell me'. Here's the question: {trivia_question}"
    elif "tell me" in user_message:
        return "dancing", f"{trivia_answer}"
    elif ("what" or "?") in user_message:
        user_message = user_message.replace('?', '').lower()
        split_message = user_message.split(" ")
        return answer_question(split_message)
    elif is_cursing(user_message):
        return "heartbroke", random.choice(curse_responses)
    elif any(word in split_msg for word in goodbye_words):
        return "no", f"Ok, fine. Talk to you next time {user_name}!"
    else:
        return "waiting", "Try asking me about something I know, like the weather or dogs. We can even play trivia or I can tell you a joke!"

def is_cursing(user_message):
    split_message = user_message.split(" ")
    with open('lib/cursewords.txt') as f:
        cursewords = f.read().splitlines()
        for word in split_message:
            if word in cursewords:
                return any(cursewords)

def get_joke():
    url = "https://joke3.p.rapidapi.com/v1/joke"
    headers = {
        'x-rapidapi-host': "joke3.p.rapidapi.com",
        'x-rapidapi-key': "39c70e6116msh7430b0e6ad6ac0dp1fa31djsn73849ea423ce"
    }
    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)
    joke = data.get("content", "I'm not in a joking mood.")
    return joke

def get_dog_fact():
    url = "http://dog-api.kinduff.com/api/facts"
    response = requests.request("GET", url)
    data = json.loads(response.text)
    fact = data.get("facts", "I'm more of a cat person.")
    return fact[0]

def get_trivia_question():
    global trivia_answer
    url = "http://jservice.io/api/random"
    response = requests.request("GET", url)
    data = json.loads(response.text)
    trivia = data[0]
    trivia_question = trivia.get("question", "I don't want to play now. Maybe later.")
    trivia_answer = trivia.get("answer", "I don't know the answer. Google it.")
    return trivia_question, trivia_answer

def get_weather():
    url = "http://dataservice.accuweather.com/currentconditions/v1/215854?apikey=VdbvG6p7Nh2ac6Gp04AmNO44SkcoMfEq"
    response = requests.request("GET", url)
    data = json.loads(response.text)
    weather_dict = data[0]
    date_time = weather_dict.get('LocalObservationDateTime', "")
    date = date_time[0:10]
    time = date_time[11:16]
    temp = weather_dict.get('Temperature', "There was an error.")
    metric = temp.get("Metric", "")
    temperature = metric.get("Value", "unknown")
    weather_summary = weather_dict.get("WeatherText", "There was an error.")
    precipitation = weather_dict.get("PrecipitationType", "no precipitation.")
    return([temperature, weather_summary, precipitation, date, time])

def is_name(user_message):
    global user_name
    split_message = user_message.split(" ")
    with open('lib/names.txt') as f:
        names = f.read().splitlines()
        for word in split_message:
            word = word.capitalize()
            if word in names:
                user_name = word
                return True

def answer_question(split_message):
    if ("your" and "name") in split_message:
        return "giggling", "My name is Boto. Nice to meet you!"
    elif "meaning" and "life" in split_message:
        return "takeoff", "42."
    else:
        return "bored", "Try asking me about something I know, like the weather or dogs. We can even play trivia or I can tell you a joke!"
