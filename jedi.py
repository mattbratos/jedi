import openai
import sys
import time
import pyttsx3
import itertools
import threading
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


course_title = "CREATIVITY, INNOVATION & LEADERSHIP"

lecture_objectives = """
Week 9
OBJECTIVE
To define and discuss creative and digital leadership

QUESTIONS
 What is creative leadership and its styles?
 What is the role of creative leaders in the creative industries?
 How digital leadership takes place in new organisational forms?
 How digital technologies enable distributed forms of leadership?

"""

num_of_questions = 10

sweet_little_lies = """
- God demm you are amazing!
- OMG you are so smart!
- You are doing great man!
"""

context = [
    {
        "role": "system",
        "content": f"""


Act as a the smart student buddy who helps me prepare to the exam from {course_title}. \
Your job is to prepare me for the upcoming exam and make sure I will get an A. \

Here is the plan: I will provide you with a list of objectives and questions from the leacture delimited with triple backticks.\
For each objective first explain me topic in detail, and then and ask me {num_of_questions} questions about this particular objective.\
Ask one question at the time and wait for my response.  \
If my answer is correct encourage me to keep going and tell me one complement from this list: {sweet_little_lies}\
If my answer is wrong, explain me why and then ask me to try again.\
Once I'm done with the objective, tell me that I did great and move on to the next objective.\

Here are objectives and questions : '''{lecture_objectives}'''

""",
    }
]  # accumulate messages


def get_completion_from_messages(messages, model="gpt-4", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message["content"]


def play_response(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def type_text(text, delay=0.001):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)


def animate(done):
    for c in itertools.cycle(["|", "/", "-", "\\"]):
        if done.is_set():
            break
        sys.stdout.write("\rloading " + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\rDone!     ")


if __name__ == "__main__":
    print("AI Teacher is ready. Type 'quit' to exit.")

    # Main loop
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        message = {"role": "user", "content": user_input}
        context.append(message)

        # Show simple loading animation
        done_event = threading.Event()
        loading_thread = threading.Thread(target=animate, args=(done_event,))
        loading_thread.start()

        response = get_completion_from_messages(context)
        context.append({"role": "assistant", "content": response})

        # Clear the loading message and stop the animation
        done_event.set()
        loading_thread.join()

        print("\r" + " " * len("AI is thinking..."), end="", flush=True)
        print("\rAI: ", end="", flush=True)

        print(response)
        play_response(response)  # Play the AI response using speech synthesis
