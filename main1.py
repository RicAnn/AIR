import openai

def askGPT(text):
    openai.api_key = "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"
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = text,
        temperature = 0.6,
        max_tokens = 30,
    )
    #print(response)
    #print(response.choices[0])
    return print(response.choices[0].text)

def main():
    while True:
        print('GPT: Cosa mi vuoi chiedere?\n')
        #myQn = input()
        myQn = "conosci il chitarrista riccardo annolfi?"
        askGPT(myQn)
        print('\n')

main()