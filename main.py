import random
import chromadb
import statistics

import character
from character import Character
from brain import Brain
from attributes import Locations
from worlds import World

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
char_a.hear(world.hear_at_location(char_a.location))
print("----------")
print("||")
print(char_a.introduce())
print("\n||")
print(char_a.express_yourself())
print("----------")
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