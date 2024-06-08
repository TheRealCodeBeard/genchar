import random

Names = [
    "Steve", "Sally", "Mark", "Kana", "Abodo", "Simon", "Penelope", "Christine", "Karen", "Colin",
    "Marcus", "Tony", "Clarance", "Helen", "Ben", "Toby", "Frances", "Tanaka", "Bert", "Earnie",
    "Hans", "Klaus", "Dorothy", "Lisa", "Chuck", "Emily", "John", "Alice", "Robert", "Nancy",
    "David", "Julia", "Michael", "Eleanor", "Paul", "Rachel", "George", "Sarah", "James", "Laura",
    "Peter", "Victoria", "Thomas", "Rebecca", "Henry", "Megan", "Andrew", "Nina", "Joshua", "Isabella",
    "Ryan", "Clara", "Louis", "Fiona", "Kevin", "Anna", "Samuel", "Olivia", "Jack", "Lily",
    "Nathan", "Sophia", "Daniel", "Grace", "Adam", "Matthew", "Chloe", "Gabriel", "Jessica", "Ethan",
    "Hannah", "Liam", "Amber", "Lucas", "Emma", "Mason", "Ava", "Alexander", "Natalie", "Jacob",
    "Ella", "William", "Samantha", "Owen", "Mia", "Charlotte", "Logan", "Harper", "Jason", "Elena",
    "Vincent", "Diana", "Oliver", "Madison", "Zachary", "Jasmine", "Patrick", "Kaitlyn", "Jordan", "Sofia",
    "Max", "Brooke", "Brian", "Catherine", "Philip", "Sophia", "Eric", "Victoria", "Evan", "Nora",
    "Gavin", "Faith", "Hunter", "Paige", "Julian", "Ruby", "Oscar", "Violet", "Xavier", "Zoey",
    "Bradley", "Holly", "Caleb", "Sadie", "Declan", "Piper", "Eli", "Aurora", "Finn", "Scarlett",
    "Grant", "Aubrey", "Hayden", "Sienna", "Ivan", "Sydney", "Jude", "Tessa", "Kieran", "Vanessa",
    "Leon", "Whitney", "Micah", "Yara", "Noah", "Zara", "Omar", "Willow", "Perry", "Ursula",
    "Quentin", "Tiffany", "Riley", "Serena", "Scott", "Renee", "Troy", "Roxanne", "Ulysses", "Vivian",
    "Wyatt", "Wendy", "Xander", "Yvonne", "Yosef", "Zelda", "Asher", "Alicia", "Blake", "Brenda",
    "Cody", "Carla", "Derek", "Daisy", "Ethan", "Elsie", "Frank", "Faye", "Greg", "Gwen",
    "Harry", "Hannah", "Isaac", "Ivy", "Jack", "Jade", "Kyle", "Kayla", "Liam", "Lila",
    "Mason", "Maya", "Nathan", "Nina", "Owen", "Olive", "Paul", "Penny", "Quinn", "Quincy",
    "Ryan", "Rachel", "Sean", "Sophie", "Tom", "Tina", "Umar", "Uma", "Victor", "Vera",
    "William", "Willa", "Xander", "Xenia", "Yusuf", "Yara", "Zach", "Zara"
]

Media = ["Albert Camus' book The Fall", "Shakespeare's Sonnets", "Shakespeare's plays", "George Orwell's books", "Starwars", "Startrek", "The Bible", 
         "Classic Russian Sci-fi", "American Pragmatism", "Hegel", "Delia Smith's cook books", "The Beno between 1970 and 1985", "DC Comic books", 
         "Marvel Comic books", "Batman", "French romantic literature", "English fantasy novels", "Scientific papers", "Internet forums", "Tabloid newspapers", 
         "TV Series", "Anime", "Korean Drama", "Pop music", "Techno", "Pop music", "Lord of the rings", "Game of thrones", "Ayn Rand", "Stalin", "Marx", "Mistic Meg", 
         "Greek Mythology", "Arthurian Legends", "Jazz Music", "Rock Music", "Historical Biographies", "Self-help Books", "Fantasy RPGs", "Documentaries", "Mystery Novels", "Cyberpunk Literature",
          "Philosophical Essays", "Satirical Magazines", "Classical Music", "Horror Movies", "Adventure Novels", "Spy Thrillers", "Epic Poetry", "Contemporary Art"]

Virtues = ["wisdom","courage","temperence","justice","humanity","transcendence"]

Values = ["authenticity", "achievement", "adventure", "authority", "autonomy", "balance", "beauty", "boldness", "compassion", 
            "challenge", "citizenship", "community", "competency", "contribution", "creativity", "curiosity", "determination", 
            "exercise", "fairness", "faith", "fame", "friendship", "forgiveness", "fun", "growth", "happiness", "health", "history", 
            "honesty", "humor", "influence", "inner harmony", "justice", "kindness", "knowledge", "leadership", "learning", "love", 
            "loyalty", "meaningful work", "money", "nature", "openness", "optimism", "peace", "pleasure", "poise", "popularity", "power", 
            "recognition", "religion", "reputation", "respect", "responsibility", "security", 
            "self-respect", "service", "spirituality", "stability", "success", "status", "trustworthiness", "wealth", "wisdom"]

Locations =  [
    "in the village square", "in the dark woods", "on the windswept hillside",
    "in the pub", "on a walk", "outside a church", "standing next to a grave",
    "by a pond", "in line at a shop", "sitting on a bench by a park",
    "by a withered tree", "under a streetlight", "inside a library", "at the beach",
    "on a mountain trail", "in a cozy cafe", "at the city market", "near a waterfall",
    "in an old barn", "on a riverbank", "inside a museum", "on a snowy peak", 
    "in a bustling city square", "at a carnival", "inside a movie theater",
    "in a quiet meadow", "on a bridge", "in a boat on the lake", "by a campfire", 
    "at a bus stop", "in a train station", "inside a cathedral", "on a rooftop garden",
    "at a farm", "on a deserted island", "at the zoo", "in a greenhouse", 
    "on a forest path", "at a concert", "in a subway station", "in a rose garden",
    "in a classroom", "on a ferris wheel", "at an airport", "inside a cave", 
    "in a grand ballroom", "at a vineyard", "in a pottery studio", "on a bicycle path",
    "inside a bakery", "at a lighthouse", "on a sandy dune", "in a castle courtyard", 
    "at a ski resort", "on a fishing dock", "inside a planetarium", "in a recording studio",
    "at a farmer's market", "on a nature reserve", "in a treehouse", "at a bookshop", 
    "in a secret garden", "at a sports stadium", "on a city bus", "inside an art gallery",
    "at a botanical garden", "in a jazz club", "on a playground", "in a science lab",
    "at a wildlife sanctuary", "on a cobblestone street", "in a yoga studio", "at a swimming pool",
    "on a picnic blanket", "in a ski lodge", "at a brewery", "inside a theater", 
    "in a lighthouse", "on a hiking trail", "at a sculpture park", "in a coffee shop", 
    "on a vineyard tour", "at a race track", "in a music hall", "on a golf course",
    "at a haunted house", "inside a greenhouse", "on a cruise ship", "at a theme park", 
    "in a chess club", "at a dance studio", "on a mountaintop", "in a sauna", 
    "at a meditation retreat", "on a city rooftop", "at a flea market", "in a surf shop",
    "on a kayak", "at a cooking class", "in a candy store", "on a carnival ride"
]

Moods =[
    "bad", "grumpy", "angry", "happy", "playful", "jokey", "sad", "excited",
    "nervous", "relaxed", "content", "bored", "anxious", "confused", "optimistic",
    "pessimistic", "curious", "disappointed", "hopeful", "frustrated", "lonely",
    "energetic", "sleepy", "motivated", "depressed", "guilty", "ashamed", "proud",
    "jealous", "calm", "overwhelmed", "fearful", "grateful", "inspired", "resentful",
    "irritated", "elated", "melancholic", "satisfied", "worried", "apathetic",
    "passionate", "envious", "serene", "terrified", "humiliated", "ecstatic", 
    "thoughtful", "nostalgic"
]

Philosophies = ["Existentialist", "Logical positivist", "Dualist", "Kantian", "Absurdist", "Neo-Platonist", 
                "Post-humanist", "Stoic", "Nihilist", "Utilitarian", "Hedonist", "Pragmatist", "Transcendentalist", 
                "Idealist", "Materialist", "Phenomenologist", "Rationalist", "Empiricist", "Marxist", "Structuralist"]

Hobbies = [
    "reading", "writing", "painting", "drawing", "gardening", "cooking",
    "baking", "hiking", "cycling", "swimming", "photography", "knitting",
    "sewing", "fishing", "bird watching", "traveling", "playing musical instruments",
    "dancing", "yoga", "gaming", "scrapbooking", "pottery", "woodworking", "running",
    "collecting stamps", "collecting coins", "origami", "model building", "calligraphy",
    "rock climbing", "surfing", "skateboarding", "snowboarding", "skiing", "kayaking",
    "scuba diving", "playing chess", "playing cards", "jogging", "meditation"
]

def get_some(list,max=3):
    result = []
    for i in range(1,max):
        if random.random()>0.5:
            result.append(random.choice([v for v in list if v not in result]))
    return result

def get_one(list):
    return random.choice(list)
