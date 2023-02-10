# AIR
Audio Open AI Robot - Scripts with Open AI on Raspberry PI and Python

This describes the procedures and installations needed to run scripts with ChatGPT/Open AI on Raspberry PI and Python.

Source link ---  https://peppe8o.com/chatgpt-raspberry-pi-python/



Step-by-Step Procedure



Sign up to OpenAI and get your API Key
Please sign up to OpenAI at their official page: https://openai.com/join. Once registered, from your personal dashboard, please open your user menù and click the “View API keys” link.

Differently from my following screen, your Secret Keys list should be empty. Please click the “Create new secret key” button to generate your first API key.

This will generate a new API key code that you must copy into a notepad, as it will be required in our python scripts.

Now we are ready to move to Raspberry PI settings and script preparation.

Prepare the Raspberry PI Operating System
Start with OS installation using my Raspberry PI OS Lite guide. This procedure also works with Raspberry PI OS Desktop, using its internal terminal.

If not already done, please make your OS up-to-date. From the terminal, use the following commands:

sudo apt update -y && sudo apt upgrade -y

We need pip to install the required python packages. From terminal:

sudo apt install python3-pip -y
Finally, the only package you need is OpenAI:

pip3 install openai
During this installation, you may get the following warnings:

WARNING: The script normalizer is installed in '/home/pi/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
  WARNING: The script tqdm is installed in '/home/pi/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
  WARNING: The script openai is installed in '/home/pi/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
You can fix it by editing your bashrc file:

nano ~/.bashrc

And append the following line at the end of this file:

export PATH="$HOME/.local/bin:$PATH"
You can reload the bashrc with the following terminal command without the need to logout or reboot:

source ~/.bashrc

It’s enough to use ChatGPT on Raspberry PI.



My ChatGPT script for Raspberry PI


NOTE: before starting, please note that in rare cases I’ve got the scripts returning errors because of the ChatGPT servers busy. This error raises in some cases and it is the same problem affecting the ChatGPT web try pages when they get a lot of requests. In those cases, please just try running the script again, better if after a few minutes.

It’s time to create our very fist script to use ChatGPT with Raspberry PI. You can get the full code for this first script with the following terminal command in your Raspberry PI:

wget https://peppe8o.com/download/python/chatgpt/chatgpt-text-query.py


At the start, we import the required modules. I also import “sys” as I will make it possible to use this script by giving the input query from your bash while calling the whole python script. So, the modules are:

import sys
import openai
Then, I define the model to use. Here I referenced all the available models in order to leave uncommented the one you are wishing to use and comment (with a starting “#” at the beginning of the line) all the remaining ones. As said, the model chosen will affect both the answer reliability and the token usage in a reverse proportion. For my tests I will use the Davinci model, leaving only this uncommented as in the following:

model_to_use="text-davinci-003" # most capable
#model_to_use="text-curie-001"
#model_to_use="text-babbage-001"
#model_to_use="text-ada-001" # lowest token cost
The next line should be configured with the OpenAI API key, previously created, inside brakets. Please use your one instead of the highlighted chars:

openai.api_key="your-OpenAI-api-key"
As should be a good programming practice, I love using custom functions in order to make my code the most clean as possible. My “chatGPT()” function requires as input only the text query to submit to ChatGPT service. Here you can define better some ChatGPT parameters like the max number of tokens to use, the completion temperature and so on (the full list is availiable at https://beta.openai.com/docs/api-reference/completions/create. For my test, I just use the max token. Please note that reducing too much the max token value could result into responses text cut.

Finally, the custom function returns the text answer (stripped from the “\n” chars) and the tokens usage:

def chatGPT(query):
	response = openai.Completion.create(
		model=model_to_use,
		prompt=query,
		temperature=0,
		max_tokens=1000
		)
	return str.strip(response['choices'][0]['text']), response['usage']['total_tokens']
With this, the main program reduces to a few very simple lines. The “query” variable takes our input from the bash shell by using the “sys.argv[1]” (as we’ll see in a few seconds). Our query is submitted to the ChatGPT service that returns the response and our token usage. The last 2 rows are just printing these values:


query=sys.argv[1]

(res, usage) = chatGPT(query)
print(res)
print("\n----------------\nTokens used: "+str(usage))
Testing my ChatGPT script
Let’s try if the script works. From your Raspberry PI terminal, add your query to the “python3 chatgpt-text-query.py” command, as below:

python3 chatgpt-text-query.py "my text query"
The following example will ask ChatGPT “Where is Rome?”. This will return a proper answer and the used tokens:

pi@raspberrypi:~ $ python3 chatgpt-text-query.py "where is Rome?"
Rome is the capital of Italy and is located in the central-western portion of the Italian Peninsula, on the Tiber River.

----------------
Tokens used: 33
Comparing the Cost of Different ChatGPT Models
An interesting test is asking ChatGPT with the same query and check both the answers reliability and their costs. I’ve made this test with the query “Explain what is a Raspberry PI with 100 words”. The following are the results.

Using the Davinci model:

Raspberry Pi is a small, affordable, single-board computer that can be used for a variety of applications. It is a credit-card sized computer that plugs into a monitor or TV, and uses a standard keyboard and mouse. It is capable of doing everything a desktop computer can do, such as playing high-definition video, browsing the internet, and playing games. It also has the ability to interact with the physical world through its GPIO pins, allowing it to control lights, motors, and other electronic components. It is a great tool for learning programming and electronics.

----------------
Tokens used: 127
Using the Curie model:

A Raspberry Pi is a small, low-cost computer that can be used to create projects, such as a home media center, a robot, or a camera. It is powered by an ARM processor and has a variety of ports, such as a USB port, an HDMI port, and a microSD card slot.

----------------
Tokens used: 76
Using the Babbage model:

A Raspberry PI is a computer that is designed to be used as a low-cost, single-board computer. It is a small, single-board computer that is based on the ARM Cortex-A53 processor. It has a number of features that make it a popular choice for small-scale projects and for learning computer programming.

----------------
Tokens used: 81
Finally, the Ada model:

A Raspberry PI is a computer device that is designed to be attached to a computer and used to access online resources. It has a variety of uses such as understanding human behavior, understanding the behavior of other animals, and understanding the behavior of other computers.

----------------
Tokens used: 62
As you can see, the Davinci model has a really reliable and complete answer, but the cost is quite double compared to the other models.

The Curie and Babbage models can give reasonable answers, even if less detailed. On the other side, they can give you a sensible token saving.

Finally, the Ada model is the less expensive, but its response is quite far from the right answer to our submitted question.

Summarizing the results for this test:

Query: “Explain what is a Raspberry PI with 100 words“

Model	Tokens used:

Davinci	  127
Curie	    76
Babbage	  81
Ada	      62


Writing Code with ChatGPT
One of the most revolutionary feature of ChatGPT, compared with the other AI software, is its capability to write down code with different programming languages from a text query. The most descriptive the query, the most complete and previce will be the code. For this task, I suggest to use the Davinci model.

Let’s test also this. In orde to make the example as much clear as possible, I will highlight in red my query and I will use the blu for the text answer:

pi@raspberrypi:~ $ python3 chatgpt-text-query.py "python code to get two numbers as input and print the sum"

# Program to add two numbers

# Store input numbers
num1 = input('Enter first number: ')
num2 = input('Enter second number: ')

# Add two numbers
sum = float(num1) + float(num2)

# Display the sum
print('The sum of {0} and {1} is {2}'.format(num1, num2, sum))

----------------
Tokens used: 104
Paste the code the code into a “sum.py” file and run it, you will find that it works (12 and 5 are my inputs on script prompt):

pi@raspberrypi:~ $ python3 sum.py
Enter first number: 12
Enter second number: 5
The sum of 12 and 5 is 17.0
Even more complex code requests get an answer:

pi@raspberrypi:~ $ python3 chatgpt-text-query.py "python code to control my email every 5 minutes and notify me when new message arrive"

import smtplib
import time

# Connect to the server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("your_email_address", "your_password")

while True:
    # Check for new messages
    messages = server.search(None, 'UNSEEN')
    if messages[1][0] != b'':
        print("You have new messages!")
    # Wait 5 minutes
    time.sleep(300)

server.quit()

----------------
Tokens used: 147
In this case, ChatGPT supposed that I’m using gmail (i didn’t specified this) and missed to warn that gmail requires to create a specific password for authorized apps. Moreover, it uses the smtplib library that can only send emails (not to receive. Even if of those imprecisions, the answer try is quite impressive.

Last test, with HTML code request:

pi@raspberrypi:~ $ python3 chatgpt-text-query.py "html code to show a page with hello world message. The background must be red. The page must also welcome the reader and exaplain what is chatgpt"

<html>
<head>
<title>Hello World</title>
<style>
body {
    background-color: red;
}
</style>
</head>
<body>
<h1>Welcome to ChatGPT!</h1>
<p>ChatGPT is a natural language processing platform that enables you to create chatbots and virtual assistants.</p>
<p>Hello World!</p>
</body>
</html>

----------------
Tokens used: 141
Save the code to a file named, for example, “test.html” and open it with a browser:

Generating Images
Before closing this tutorial, I just want to show you how to create images from text strings.

The OpenAI product that accomplish this task is Dall-e and uses a similar script construction and the sam API Key already generated. You can find my test script with the following:

wget https://peppe8o.com/download/python/dall-e/picture-query.py
This script is really similar to the previous one, but it changes on the custom function using the “Image.create” with the related options (the full API reference for image generation is available at https://beta.openai.com/docs/api-reference/images/create):

def img_gen(query):
	response = openai.Image.create(
  		prompt=query,
  		n=1,
  		size="1024x1024"
	)
	return response['data'][0]['url']
Moreover, this function will return the URL for the generated image. You can use this returned URL in your browser in order to get the generated image:

pi@raspberrypi:~ $ python3 picture-query.py "a dog watching at an hotdog"
https://oaidalleapiprodscus.blob.core.windows.net/private/org-4yHD0Vt1wG9MmaKE2vMypmSB/user-h5F3cAdmI1a7ce6633FCkhnj/img-TaMDqWcDlMT6zybQxqJSHzr2.png?st=2023-01-13T10%3A26%3A02Z&se=2023-01-13T12%3A26%3A02Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-01-13T07%3A37%3A07Z&ske=2023-01-14T07%3A37%3A07Z&sks=b&skv=2021-08-06&sig=VsK4Rl0TX5XW6JYWyN0AOrnaF0VmfJ7UkROvyHIiCws%3D
With the URL resulting in the following:

Please also note that the image generation has a different pricing, also this exposed at OpenAI pricing page.
