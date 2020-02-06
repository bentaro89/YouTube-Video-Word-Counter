import discord
from youtube_transcript_api import YouTubeTranscriptApi

# For discord bot
discord_token = 'token'
client = discord.Client()

# Assures connection to discord server
@client.event
async def on_ready():
    print(f'{client.user} has connected to the server!!')

# Gets rid of unnecessary expressions
def strip_word(w):
    w = w.replace(".", "")
    w = w.replace(",", "")
    w = w.replace(";", "")
    w = w.replace(":", "")
    w = w.replace("-", "")
    w = w.replace("?", "")
    w = w.replace("!", "")
    w = w.replace('"', "")
    w = w.lower()
    return w

# Sorts dictionary
def iterate_dict(dictionary):
    list = []
    sorted_dict = sorted(dictionary.items(), key = lambda x:x[1], reverse= True)
    for key in sorted_dict:
        list.append(key)
    return list

def count_words(line):
    # Gets rid of any ( { * symbols
    line = cleaner(line)

    # Integer for how many words in video
    words = 0

    # Dictionary for words in video
    counter_list = {}

    # Strips the line and splits it into a list
    line = line.strip().split()

    # Counter for each word
    # Uses dictionary. Word is the key. Amount of words for value
    for word in line:
        words +=1

        # Cleans word
        word = strip_word(word)

        # Totals the amount of word in the string
        if word.isalpha() or "'" in word:
            if word in counter_list:
                counter_list[word] += 1
            else:
                counter_list[word] = 1

    # Sorts dictionary
    count_dict = iterate_dict(counter_list)

    # print total
    total = ['There are ' + str(words) + ' total words in the video', count_dict]
    return total

def get_text(YT_id):
    one_line = ""
    # Uses YouTube API and parses the text
    for key in YouTubeTranscriptApi.get_transcript(YT_id, languages= ['en']):
        one_line += key['text'] + ' '
    return one_line

# Takes out everything enclosed in string
def cleaner(test_str):
    ret = ''
    skip1c = 0
    skip2c = 0
    skip3c = 0
    for i in test_str:
        if i == '[':
            skip1c += 1
        elif i == '(':
            skip2c += 1
        elif i == '*':
            skip3c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif i == '*'and skip3c > 0:
            skip3c -= 1
        elif skip1c == 0 and skip2c == 0 and skip3c == 0:
            ret += i
    return ret

#For discord
@client.event
async def on_message(message):

    # Checks if client is connected
    if message.author == client.user:
        return

    # Checks if it's a Youtube link
    if message.content[:32] == 'https://www.youtube.com/watch?v=':
        try:
            id = message.content[32:]# Takes the link ID
            final = count_words(get_text(id))# gets string
            await message.channel.send(final[0])# Returns the total amount of words

            # Groups the pairs by how many words they have
            string = ''
            prev_pair = 0
            for i in range(len(final[1])):
                if len(string) >= 1000:
                    await message.channel.send(string)
                    string = ''
                if final[1][i][1] == prev_pair:
                    string += ' | ' + str(final[1][i][0]) +' = ' + str(final[1][i][1])
                elif i == 0:
                    string = str(final[1][i][0]) + ' = ' + str(final[1][i][1])
                else:
                    await message.channel.send(string)
                    string = str(final[1][i][0]) +' = ' + str(final[1][i][1])
                prev_pair = final[1][i][1]
            await message.channel.send(string)
            await message.channel.send("DONE")
        except:
            await message.channel.send("This video does not have subtitles")
    else:
        await message.channel.send("Not a valid YouTube link")

# Same function as above but for terminal
def word_count():
    link = input("Paste a valid Youtube link")
    if link[:32] == 'https://www.youtube.com/watch?v=':
        try:
            id = link[32:]
            final = count_words(get_text(id))
            print(final[0])

            string = ''
            prev_pair = 0
            for i in range(len(final[1])):
                if len(string) >= 1000:
                    print(string)
                    string = ''
                if final[1][i][1] == prev_pair:
                    string += ' | ' + str(final[1][i][0]) +' = ' + str(final[1][i][1])
                elif i == 0:
                    string = str(final[1][i][0]) + ' = ' + str(final[1][i][1])
                else:
                    print(string)
                    string = str(final[1][i][0]) +' = ' + str(final[1][i][1])
                prev_pair = final[1][i][1]
            print(string)
            print("THAT'S ALL")

        except:
            print("This video does not have subtitles")
    else:
        print("Not a valid YouTube link")

while True:
    mode = int(input("Enter 1 for terminal. 2 for discord"))

    if mode == 1: # For terminal
        while True:
            word_count()

    elif mode == 2: # For discord
        client.run(discord_token)
    else:
        print("invalid input. Try again")



