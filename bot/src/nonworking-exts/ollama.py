# Silly LLM stuff
try:
    if type(message.channel) == disnake.DMChannel:
        history = None
        convdir = config["volpath"] + "/ollama/"

        if not os.path.exists(convdir):
            os.makedirs(convdir)

        if str(message.author.id) in os.listdir(convdir):
            history = json.load(open(convdir + str(message.author.id)))
            history.append({"role": "user", "content": message.content})
        else:
            history = [
                {"role": "user", "content": message.content},
            ]

        url = config["ollama_url"] + "/api/chat"
        data = {"model": config["ollama_model"], "messages": history, "stream": False}

        response = await self.fetch_data(url, data)
        rt = await response.text()
        rj = await response.json()

        if response.status == 200:
            stuff = rj
            if "message" in stuff.keys():
                for pt in split_string(stuff["message"]["content"]):
                    if pt != "":
                        await message.channel.send(pt)
                history.append(
                    {"role": "assistant", "content": stuff["message"]["content"]}
                )
                json.dump(history, open(convdir + str(message.author.id), "w"))
            else:
                await message.channel.send("Error: " + str(stuff))
                await message.channel.send("We sent: ```" + str(data) + "```")
        else:
            await message.channel.send("Error: " + str(response.status))
            await message.channel.send("```" + str(rt) + "```")
            await message.channel.send("We sent: ```" + str(data) + "```")

except Exception as e:
    await message.channel.send("Error: " + str(e))
    owner = await self.bot.fetch_user(self.bot.owner_id)
    await owner.send("Error: `" + str(e) + "`")
