import random
import chromadb
import statistics

import character
from character import Character
from brain import Brain
from attributes import Locations
from worlds import World

def print_l(text, word_limit=10):
    words = text.split()
    for i in range(0, len(words), word_limit):
        print(' '.join(words[i:i + word_limit]))

print("_________________")

base_brain = Brain.get_base_brain()
memory_client = chromadb.PersistentClient(f"./chroma")
shared_locaiton = random.choice(Locations)
world  = World(base_brain)
char_a = character.get_or_create_character(base_brain,memory_client,shared_locaiton)
#char_b = get_or_create_character(base_brain,memory_client,shared_locaiton)
#char_a.known_people.append(char_b.name)
#char_b.known_people.append(char_a.name)

char_a.save(character.character_folder)
#char_b.save(character.character_folder)

char_a.see(world.seen_at_location(char_a.location))
char_a.see("Barney stole some chips from Barbara","Barney")
char_a.hear(world.hear_at_location(char_a.location))
char_a.hear("a loud laugh","Barney")
char_a.hear("Someone made a terrifying scream")
char_a.hear("I likes chips","Barbara")
char_a.hear("I love potatoes","Barbara")
char_a.hear("I hate Barney","Barbara")
char_a.hear("I dislikes cats","Barbara")
print("----------")
print_l(char_a.introduce())
print("\n++")
print_l(char_a.express_yourself())
print("++")
print_l(char_a.generate_question_for("Barbara"))
print("++")
print_l(char_a.generate_question_for("Barney"))
print("----------")
char_a.save(character.character_folder)

# char_a_intro = char_a.introduce()
# print(char_a_intro)
#print(char_b.introduce())
# char_b.remember(char_a_intro)
# for i in range(1,5):
#     char_a_expression = char_a.express_yourself()
#     print(char_a_expression)
#     char_b.remember(char_a_expression)
#     print("----------")

# print(char_b.introduce())
# print("++++++++")
# question = char_b.generate_question_for(char_a.name)
# print(f"[{char_b.name} asks {char_a.name} '{question}']")
# print(f"[{char_a.name} responds...]")
# char_a_response = char_a.respond(question) 
# print(char_a_response)
# char_b.remember(char_a_response)

# question = char_b.generate_question_for(char_a.name)
# print(f"[{char_b.name} asks {char_a.name} '{question}']")
# print(f"[{char_a.name} responds...]")
# char_a_response = char_a.respond(question) 
# print(char_a_response)
# char_b.remember(char_a_response)

# question = char_b.generate_question_for(char_a.name)
# print(f"[{char_b.name} asks {char_a.name} '{question}']")
# print(f"[{char_a.name} responds...]")
# char_a_response = char_a.respond(question) 
# print(char_a_response)
# char_b.remember(char_a_response)

# print("++++++++")
#print(f"Char A mean prompt tokens: {statistics.mean(char_a.brain.prompt_token_counts):.1f} Char B mean prompt tokens: {statistics.mean(char_b.brain.prompt_token_counts):.1f}")
print(f"Char A mean prompt tokens: {statistics.mean(char_a.brain.prompt_token_counts):.1f}")
print("_________________")