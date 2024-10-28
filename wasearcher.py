import sys
import re
import time

try: 
    msg = open(sys.argv[1])
except IndexError:
    print("Usage: wasearcher.py [chatexport.txt]")
    quit()
except FileNotFoundError:
    print(f"No such file or directory: {sys.argv[1]}")
    quit()

messages = [] #list where messages is stored as dictionary
dateMatch = re.compile('\d{1,2}/\d{1,2}/\d{2}, \d{2}:\d{2}') #regex for knowing if it's a new message
index = -1
print("elaborating...")
start_time = time.time()

for line in msg: 
    if dateMatch.match(line) is not None: #check if line starts with date (new message)
        index += 1
        nameStart = 0
        nameEnd = 0
        date = re.search("\d{1,2}/\d{1,2}/\d{2}", line)
        hour = re.search("\d{2}:\d{2}", line)
        try: #getting the username
            nameStart = line.index('- ') + 2
            nameEnd = line.index(':',nameStart)
            author = line[nameStart:nameEnd]
            content = line[nameEnd+2:-1]
        except ValueError:
            author = "no author"
            content = line[line.index("-") + 2:-1]
        message = { #parse every information in to a dictionary
            "date": date.group(),
            "hour": hour.group(),
            "author": author,
            "content": content,
            "index" : index
        }
        messages.append(message)
    else:
        #if message doesn't start with a date, it means that it's a new line of the previous message
        messages[-1]["content"] = messages[-1]["content"] + " " + line[:-1]

print(f"elaborated {index} messages in {str(time.time() - start_time)}")

while True:
    select = input("\n1) Filter by name\n2) Filter by date\n3) Search by term\n4) Search by id\n5) Messages counter\n6) User counter\n> ")
    match select:
        case "1":
            name = input("Enter name to filter: ")
            for i in messages:
                if name in str(i["author"]):
                    print(i["content"])
        case "2":
            match = re.compile('\d{1,2}/\d{1,2}/\d{2}')
            date = input("Enter date to filter: ")
            if match.match(date) is None:
                print("invalid date")
                break
            else:
                for i in messages:
                    if date in str(i["date"]):
                        print(f"{i['author']}: {i['content']}")
        case "3":
            term = input("Enter term to filter: ")
            for i in messages:
                if term in str(i["content"]):
                    print(f"{i['author']}: {i['content']}")

        case "4":
            ind= input("input message index: ")
            if ind is not int:
                print("NaN")
            else:
                selMess = messages[int(ind)]
                print(f"{selMess['author']}: {selMess['content']}")
        
        case "5":
            counter = {}
            for i in messages:
                author = str(i["author"])
                if author not in counter: counter[author] = 1
                else: counter[author] += 1
            for i in sorted(counter.items(), key=lambda x:x[1]):
                print(f"{i[0]}: {i[1]} messaggi.")

        case "6":
            names = []
            for i in messages:
                author = str(i["author"])
                if author not in names: names.append(author)
            names = sorted(names)
            print("\n".join(names))
            print(f"Total users: {len(names)}")
