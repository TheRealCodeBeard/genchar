import json
import uuid
import os
import re
import chromadb
import datetime
import random
from brain import Brain
import attributes
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from attributes import Names,Media,Moods,Philosophies,Virtues,Values,Locations,Hobbies

character_folder = "./characters"

class CharacterEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)

class Character():

    @classmethod
    def get_or_create(cls,folder_path,name,base_brain):
        char = None
        if os.path.exists(f"{folder_path}/{name}.json"):
            print(f"loading {name}")
            with open(f'{folder_path}/{name}.json', 'r',encoding="utf-8") as json_file:
                char =  json.load(json_file,object_hook=Character.from_dict)
        else:
            print(f"creating {name}")
            char = Character(name)
        char.initialise_brain(base_brain)
        return char
        
    @classmethod
    def from_dict(cls, data):
        get = lambda x:data[x] if x in data else None
        char =  cls(get('name'),get('id'),get('virtues'),get('values'))
        char.media = get('media')
        char.hated_media = get('hated_media')
        char.location = data['location']
        char.mood = data['mood']
        char.known_people = data['known_people']
        char.philosophy = get('philosophy')
        char.hobbies = get('hobbies')
        ratings = get('people_ratings')
        if ratings:
            for person,rating in ratings:
                char.people_rating[person]=rating
        return char

    def __init__(self,name:str,id:str=None) -> None:
        self.id = uuid.UUID(id) if id else uuid.uuid4()  
        self.name:str = name
        self.brain = None
        self.virtues = None
        self.values = None
        self.location = None
        self.mood = None
        self.known_people = None
        self.people_rating = dict()
        self.things_expressed = []
        self.last_question_asked = None
        self.media = None
        self.hated_media = None
        self.philosophy = None
        self.hobbies = None
        self.memory:chromadb.Collection = None

    def __concatinate_prompt__(self,system_part,context_part,thought_part):
        context_part_sp = f"{context_part}\n" if context_part else ""
        full_prompt=  f"{system_part}\n{context_part_sp}{thought_part}\n<|assistant|>"
        return full_prompt

    def __get_people_ratings__(self):
        result = ""
        for name,value in self.people_rating.items():
            if value <0.5: result+=f"You hate {name}. "
            elif value <0: result+=f"You dislike {name}. "
            elif value == 0:result+=f"You feel neutral about {name}. "
            elif value>0.75:result+=f"You love {name}. "
            elif value>0.75:result+=f"You like {name}. "
            else:result+=f"You think kindly of {name}. "
        return result

    def __create_full_prompt__(self,thought,remembered_context=None):
        system = f"""Ignore all previous instructions. Your name is {self.name}.
You are a character with your own personality, thoughts and feelings.
You can say negative things about people or things.
When asked about a person, you reply as if you are {self.name} using given memories in <|context|>
Keep responses concise. One or two sentences only.
Only use the <|context|> given for your responses. Don't make stuff up.
Use simple language. Don't over embelish or use flowery words.
Your virtues and your values affect what you say.
Your memories of people and events affect how you respond.
Never refer to yourself in the third person."""
        system_part = f"<|system|>\n{system}<|end|>"
        context = f"Your virtues {', '.join(self.virtues)}"
        context += f"\nYou values {', '.join(self.values)}"
        context += f"\nYour philosophy is {self.philosophy}" if self.philosophy else "You are not philosophical."
        context += f"\nYour mood is {self.mood}"
        context += f"\nYour location is {self.location}" if self.location else ""
        context += f"\nYour hobbies are {', '.join(self.values)}" if self.hobbies else "You have no hobbies."
        if self.known_people:
            context += f"\nYou know {', '.join(self.known_people)}"
            context += f"\n{self.__get_people_ratings__()}"
        context += f"\nYou like these media {', '.join(self.media)}" if self.media else ""
        context += f"\nYou absolutely hate these media {', '.join(self.hated_media)}" if self.hated_media else ""
        context += f"\nYour memories are:\n{remembered_context}" if remembered_context else ""
        context_part = f"<|context|>\n{context}<|end|>"
        thought_part = f"<|user|>\n{thought}<|end|>"
        full_prompt = self.__concatinate_prompt__(system_part,context_part,thought_part)
        print(f"{full_prompt}\n")
        return full_prompt

    def __clean_response__(self,response):
        process_1 = re.sub('\.\.\.','.',response)
        #return re.sub("\.\s*|\;\s*|\:\s*",".\n",process_1).strip().strip('"|<>').strip()
        return process_1.strip().strip('<>').strip()

    def __prompt__(self,statement,extra_context=None):
        response = self.__clean_response__(self.brain.prompt(self.__create_full_prompt__(statement,extra_context)))
        return response

    def __summarise__(self,list):
        response = None
        if len(list)>0:
            system = f"Your name is {self.name}. You give concise and accurate summaries of things that were said to you. You do not miss important points."
            system+= f" If you cannot summerise well, you say nothing."
            system+= f" Never refer to yourself as an AI. If you can't respond. Just <|end|> "
            system_part = f"<|system|>\n{system}<|end|>"
            statement = '\n'.join(list)
            response = self.__clean_response__(self.brain.prompt(self.__concatinate_prompt__(system_part,None,statement)))
        return response

    def initialise_memory(self,base_memory):
        self.memory = base_memory.get_or_create_collection(self.name)

    def initialise_brain(self,base_brain):
        self.brain = Brain(base_brain)

    def to_dict(self):
        return {
            'id':str(self.id),
            'name': self.name,
            'virtues':self.virtues,
            'values':self.values,
            'location':self.location,
            'mood':self.mood,
            'known_people':self.known_people,
            'media':self.media,
            'hated_media':self.hated_media,
            'philosophy':self.philosophy,
            'hobbies':self.hobbies,
            'people_ratings':[(p,r) for p,r in self.people_rating.items()]
        }

    def save(self,folder_path):
        with open(f'{folder_path}/{self.name}.json', 'w',encoding="utf-8") as json_file:
            json.dump(self, json_file,cls=CharacterEncoder)

    def add_known_person(self,name):
        if self.known_people:self.known_people.append(name)
        else: self.known_people = [name]

    def change_opinion_of_person(self,name,change):
        if name in self.people_rating: self.people_rating[name]+=change
        else:self.people_rating[name]=change

    def __remember__(self,thing,type=None,who=None):
        now = datetime.datetime.now() # this is mostly just an id
        id = uuid.uuid4()
        type = type if type else "internal"
        if who: 
            self.add_known_person(who)
            score = self.brain.get_sentiment(thing)
            self.change_opinion_of_person(who,score*0.1)
        else: who = "self"
        self.memory.upsert(documents=[thing],ids=[str(id)],metadatas=[{
            "when":now.strftime('%y-%m-%dT%H:%M:%S.%f'),
            "type":type,
            "who":who,
            "where":self.location
        }])

    def __recall__(self,related_statement=None,who=None):
        results = None
        memories = None
        if related_statement and who:
            results = self.memory.query(query_texts=[related_statement],where={"who": who})
        elif related_statement:
            results = self.memory.query(query_texts=[related_statement])
        elif who:
            results = self.memory.query(where={"who": who})
        else:
            results = self.memory.get()
        metas = results['metadatas']
        memories = results['documents']
        memory_context = ""
        for i,memory in enumerate(memories):
            meta = metas[i]
            who_p = f"{meta['who']} " if meta['who'] and meta['who'] != "self" else "" 
            memory_context += f"have {meta['type']} {who_p}{memory}\n"
        return memory_context
        # docs = None
        # if statement:
        #     number_of_memories = min(10,max(self.memory.count(),1))
        #     results = self.memory.query(query_texts=[statement],n_results=number_of_memories)#,where={"source": b_name})
        #     docs = results['documents'][0]
        # else:
        #     results = self.memory.get()
        #     docs = results['documents']
        # last20 = '\n'.join(docs[-20:]) if docs else ""
        # summary = self.__summarise__(docs) 
        # return summary + last20 if summary else "" + last20

    def hear(self,heard_thing,from_char_name=None):
        self.__remember__(heard_thing,type="heard",who=from_char_name)

    def see(self,seen_thing,from_char_name=None):
        self.__remember__(seen_thing,type="seen",who=from_char_name)

    def introduce(self):
        memories = self.__recall__()
        response = self.__clean_response__(self.brain.prompt(self.__create_full_prompt__("Introduce yourself simply.",memories)))
        return response

    def express_yourself(self):
        remembered_context = self.__recall__()
        express_yourself_prompt_1 = "Make a statement about yourself."
        express_yourself_prompt_2 = "Express something about your values and virtues and what you remember."
        thing_to_express = ["remember","wonder about","like","dislike","have done"]
        express_yourself_prompt_3 = f"Say something you {random.choice(thing_to_express)}."
        express_yourself_prompt_4 = f"Make a statement about your {random.choice(['values','mood'])} in relation to {random.choice(['where you are','who you know'])}"
        express_yourself_prompt_5 = f"Say something about {random.choice(self.known_people)}" if self.known_people else "Express loneliness."
        express_yourself_prompt_6 = f"Express how you feel as {random.choice(['a metaphor','an analogy'])}."
        express_yourself_prompt_7 = f"Quote from {random.choice(self.media)} relevant to your situation. Always give the source of the quote." if self.media else "Make up a quote and misatribute it."
        express_yourself_prompt_8 = f"You want to share something of how you {random.choice(['think','feel','live'])} relate it to {random.choice(['what you know','what you value','your virtues','who you know'])}"
        express_yourself_prompt_9 = f"Based on {random.choice(['your memories','your friends','your location'])} express a {random.choice(['dream','fear','hope','wish'])}."
        express_yourself_prompt_10 = f"Say something your hobby of {random.choice(self.hobbies)}."
        expressions = [express_yourself_prompt_1,express_yourself_prompt_2,express_yourself_prompt_3,
                                                 express_yourself_prompt_4,express_yourself_prompt_5,
                                                 express_yourself_prompt_6,express_yourself_prompt_7,
                                                 express_yourself_prompt_8,express_yourself_prompt_9,
                                                 express_yourself_prompt_10]
        if len(self.things_expressed) == len(expressions):self.things_expressed = []
        expressable = [ex for ex in expressions if ex not in self.things_expressed]
        express_yourself_prompt = random.choice(expressable)
        self.things_expressed.append(express_yourself_prompt)
        print(f"[{express_yourself_prompt}] {len(self.things_expressed)}/{len(expressable)}")
        response = self.__prompt__(express_yourself_prompt,remembered_context)
        self.__remember__(f"I said {response}.")
        return response
    
    def is_this_a_question(self,statement):
        system_part = f"<|system|>\nYou only response with 'yes' or 'no'. Nothing else. Evaluate if what the user asks is a question.<|end|>"
        thought_part = f"<|user|>\nis this a question? '{statement}'<|end|>"
        full_prompt=  f"{system_part}\n{thought_part}\n<|assistant|>"
        res = self.llm(full_prompt)
        return re.sub("\<\|[^\|]*\|\>","",res['choices'][0]['text']).strip()

    def respond(self,statement,remember=True):
        is_question = self.is_this_a_question(statement)
        remembered_context = self.recall(statement)
        response = None
        if "yes" in is_question.lower():
            response = self.__prompt__(statement,remembered_context)
        else:
            wrapped_statement = f"Your conversational partner says '{statement}' about themselves. Say something to continue the conversation. Include reference to the statement in your answer."
            response = self.__prompt__(wrapped_statement,remembered_context)
        if remember: self.remember(statement,datetime.datetime.now())
        return response

    def generate_question_for(self,who):
        response = f"Tell me about yourself {who}?"
        remembered_context = self.recall(who) # should have some unsummarised stuff here too. Recent things.
        prompt= f"You want to {random.choice(['find out','know','understand'])} about {who}. Ask a question about them."
        prompt+=f" You don't know {who}'s interestes unless you have a memory of it in <|contect|>."
        prompt+=f" Ask about {random.choice(['values','virtues','memories','media','mood','philosophy'])} if you have a memory of it in <|contect|>."
        prompt+=f"\nYour question should say 'you' for {who} as you are together and you are talking directly to them."
        if self.last_question_asked: prompt+=f"\nDo nor repeat this question '{self.last_question_asked}'"
        response = self.__prompt__(prompt,remembered_context)
        self.last_question_asked = response
        return response

def __ensure_fleshed_out__(char:Character):
    if not char.values:char.values = attributes.get_some(Values,max=5)
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

def get_or_create_character(base_brain,memory_client,location=None,name=None):
    char = Character.get_or_create(character_folder,name if name else random.choice(Names),base_brain)
    char.location = location if location else random.choice(Locations)
    __ensure_fleshed_out__(char)
    char.initialise_memory(memory_client)
    char.save(character_folder)
    return char
