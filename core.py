import json, random

class Client:

    def __init__(self, path=None):
        if not path:
            self.path = "data.json"
        else:
            self.path = path
        try:
            with open(self.path) as f:
                json.load(f)
        except Exception as e:
            print("Making file path a valid JSON file")
            with open(self.path, "w") as f:
                f.write("{}")


    def add_to_data(self, messages):
        with open(self.path) as f:
            data = json.load(f)

        if "escape start" not in data.keys():
            data["escape start"] = {}

        if isinstance(messages, str):
            messages = [messages]

        for message in messages:
            message_l = message.split(' ')

            for i in range(len(message_l)):
                if message_l[i] not in data.keys():
                    data[message_l[i]] = {
                        "escape end": 0,
                        "escape middle": 0
                    }

                if i == (len(message_l) - 1):
                    data[message_l[i]]["escape end"] += 1

                if i == 0:
                    if message_l[i] not in data["escape start"].keys():
                        data["escape start"][message_l[i]] = 0

                    data["escape start"][message_l[i]] += 1

                    if i != (len(message_l) - 1):

                        if message_l[i+1] not in data[message_l[i]].keys():
                            data[message_l[i]][message_l[i+1]] = 0
                        
                        data[message_l[i]][message_l[i+1]] += 1
                        
                if i != 0 and i != (len(message_l) - 1):
                    data[message_l[i]]["escape middle"] += 1

                    if message_l[i+1] not in data[message_l[i]].keys():
                        data[message_l[i]][message_l[i+1]] = 0
                    
                    data[message_l[i]][message_l[i+1]] += 1

        with open(self.path, 'w') as f:
            f.write(json.dumps(data, indent=4))

    def create_message(self):
        with open(self.path) as f:
            data = json.load(f)

        total = 0
        guess = 0

        try:
            for num in data["escape start"].values():
                total += num
        except Exception as e:
            raise KeyError("no data found")

        randint = random.randint(1, total)

        for word, num in data["escape start"].items():
            guess += num
            if randint <= guess:
                message = word
                currWord = word
                break

        while True:
            if data[currWord]["escape end"] == 0 and data[currWord]["escape middle"] == 0:
                total = 0
                guess = 0

                for word, num in data[currWord].items():
                    if word != "escape end" and word != "escape middle":
                        total += num

                randint = random.randint(1, total)

                for word, num in data[currWord].items():
                    if word != "escape end" and word != "escape middle":
                        guess += num
                        if randint <= guess:
                            currWord = word
                            message += " " + currWord
                            break
            else:
                rand_test = 0
                for word, num in data[currWord].items():
                    if word != "escape middle" and word != "escape start":
                        rand_test += num

                if data[currWord]["escape middle"] == 0 and rand_test > 0:
                    continue_chance = rand_test
                else:
                    continue_chance = data[currWord]["escape middle"]

                randint = random.randint(1, data[currWord]["escape end"] + continue_chance)

                if randint <= data[currWord]["escape middle"]:
                    total = 0
                    guess = 0

                    for word, num in data[currWord].items():
                        if word != "escape end" and word != "escape middle":
                            total += num

                    randint = random.randint(1, total)

                    for word, num in data[currWord].items():
                        if word != "escape end" and word != "escape middle":
                            guess += num
                            if randint <= guess:
                                currWord = word
                                message += " " + currWord
                                break

                else:
                    break
        return message