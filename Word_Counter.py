import discord
from youtube_transcript_api import YouTubeTranscriptApi

# For discord bot
discord_token = [token]

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

#Sorts list
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

        #Cleans word
        word = strip_word(word)

        if word.isalpha() or "'" in word:
            if word in counter_list:
                counter_list[word] += 1
            else:
                counter_list[word] = 1

    # Sorts dictionary
    count_dict = iterate_dict(counter_list)
    total = ['There are ' + str(words) + ' total words in the video', count_dict]
    return total

def get_text(YT_id):
    one_line = ""
    for key in YouTubeTranscriptApi.get_transcript(YT_id, languages= ['en']):
        one_line += key['text'] + ' '
    return one_line

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

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content[:32] == 'https://www.youtube.com/watch?v=':
        try:
            id = message.content[32:]
            final = count_words(get_text(id))
            await message.channel.send(final[0])

            string = ''
            prev_pair = 0
            paired = False
            for i in range(len(final[1])):
                if len(string) >= 1000:
                    await message.channel.send(string)
                    string = ''
                if final[1][i][1] == prev_pair:
                    string += ' | ' + str(final[1][i][0]) +' = ' + str(final[1][i][1])
                    paired = True
                elif i == 0:
                    string = str(final[1][i][0]) + ' = ' + str(final[1][i][1])
                else:
                    await message.channel.send(string)
                    string = str(final[1][i][0]) +' = ' + str(final[1][i][1])
                    paired = False
                prev_pair = final[1][i][1]
            await message.channel.send(string)
            await message.channel.send("THAT'S ALL")
        except:
            await message.channel.send("This video does not have subtitles")
    else:
        await message.channel.send("Not a valid YouTube link")

#print(count_words(get_text('7Cykzsi38hA')))
client.run(discord_token)


