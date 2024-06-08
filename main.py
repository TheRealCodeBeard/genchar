import random
import chromadb
import statistics

import character
from character import Character
from brain import Brain
import attributes
from attributes import Names,Media,Moods,Philosophies,Virtues,Values,Locations,Hobbies

def get_or_create_character(base_brain,memory_client,location=None,name=None):
    char = Character.get_or_create(character.character_folder,name if name else random.choice(Names),base_brain)
    char.location = location if location else random.choice(Locations)
    if not char.values:char.values = attributes.get_some(Values)
    if not char.virtues:char.virtues = attributes.get_some(Virtues)
    if not char.mood:char.mood = attributes.get_one(Moods)
    if not char.known_people:char.known_people = attributes.get_some(Names)
    if not char.media:char.media = attributes.get_some(Media)
    if not char.hated_media:char.hated_media = attributes.get_some([m for m in Media if m not in char.media])
    if not char.philosophy:char.philosophy = attributes.get_one(Philosophies)
    if not char.hobbies:char.hobbies = attributes.get_one(Hobbies)
    if len(char.people_rating)==0:
        for p in char.known_people:
            char.people_rating[p]=random.uniform(-1.0, 1.0)
    char.initialise_memory(memory_client)
    char.save(character.character_folder)
    return char

print("_________________")

base_brain = Brain.get_base_brain()
memory_client = chromadb.PersistentClient(f"./chroma")
shared_locaiton = random.choice(Locations)
char_a = get_or_create_character(base_brain,memory_client,shared_locaiton)
char_b = get_or_create_character(base_brain,memory_client,shared_locaiton)
char_a.known_people.append(char_b.name)
char_b.known_people.append(char_a.name)
char_a.save(character.character_folder)
char_b.save(character.character_folder)

print("----------")
char_a_intro = char_a.introduce()
print(char_a_intro)
char_b.remember(char_a_intro)
print("----------")
for i in range(1,5):
    char_a_expression = char_a.express_yourself()
    print(char_a_expression)
    char_b.remember(char_a_expression)
    print("----------")

print(char_b.introduce())
print("++++++++")
question = char_b.generate_question_for(char_a.name)
print(f"[{char_b.name} asks {char_a.name} '{question}']")
print(f"[{char_a.name} responds...]")
char_a_response = char_a.respond(question) 
print(char_a_response)
char_b.remember(char_a_response)

question = char_b.generate_question_for(char_a.name)
print(f"[{char_b.name} asks {char_a.name} '{question}']")
print(f"[{char_a.name} responds...]")
char_a_response = char_a.respond(question) 
print(char_a_response)
char_b.remember(char_a_response)

question = char_b.generate_question_for(char_a.name)
print(f"[{char_b.name} asks {char_a.name} '{question}']")
print(f"[{char_a.name} responds...]")
char_a_response = char_a.respond(question) 
print(char_a_response)
char_b.remember(char_a_response)

print("++++++++")
print(f"Char A mean prompt tokens: {statistics.mean(char_a.brain.prompt_token_counts):.1f} Char B mean prompt tokens: {statistics.mean(char_b.brain.prompt_token_counts):.1f}")
print("_________________")