from brain import Brain 
import random

class World():
    def __init__(self,base_brain) -> None:
        self.brain = Brain(base_brain)
        self.location_sights = dict()
        self.location_sounds = dict()

    def seen_at_location(self,location):
        saw = None
        #we see what has been seen here 90% of the time
        if location in self.location_sights and random.random()>0.1:
            saw = random.choice(self.location_sights[location])
        else:
            system_part = f"<|system|>\nYou imagine what can be seen at a given location. You keep it short and only mention one thing."
            system_part +=f"\nFor example: 'you are in a palace' you may say 'a thrown'."
            system_part +=f"\n'you are in a park' you may say 'a bench'."
            system_part +=f"\n'you are in a lab' you may say 'equipmnent'."
            system_part +=f"\n'you are in forest' you may say 'a lot of trees and plants'."
            system_part +="\n<|end|>"
            thought_part = f"<|user|>\nYou are {location}. What do you see?<|end|>"
            full_prompt=  f"{system_part}\n{thought_part}\n<|assistant|>"
            saw = self.brain.prompt(full_prompt)
            if saw not in self.location_sights:
                self.location_sights[location] = saw
        return saw
    
    def hear_at_location(self,location):
        hear = None
        #we see what has been seen here 90% of the time
        if location in self.location_sounds and random.random()>0.1:
            hear = random.choice(self.location_sounds[location])
        else:
            system_part = f"<|system|>\nYou imagine what can be heard at a given location. You keep it short and only mention one thing."
            system_part +=f"\nFor example: 'you are in a palace' you may say 'gentle music'."
            system_part +=f"\n'you are in a park' you may say 'children playing'."
            system_part +=f"\n'you are in a lab' you may say 'the hum of machines'."
            system_part +=f"\n'you are in forest' you may say 'wind rustling or birds singing'."
            system_part +="\n<|end|>"
            thought_part = f"<|user|>\nYou are {location}. What do you hear?<|end|>"
            full_prompt=  f"{system_part}\n{thought_part}\n<|assistant|>"
            hear = self.brain.prompt(full_prompt)
            if hear not in self.location_sounds:
                self.location_sounds[location] = hear
        return hear

