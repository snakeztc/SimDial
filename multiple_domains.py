# -*- coding: utf-8 -*-
# author: Tiancheng Zhao
from simdial.domain import Domain, DomainSpec
from simdial.generator import Generator
from simdial import complexity
import string


class RestSpec(DomainSpec):
    name = "restaurant"
    greet = "Welcome to restaurant recommendation system."
    nlg_spec = {"loc": {"inform": ["I am at %s.", "%s.", "I'm interested in food at %s.", "At %s.", "In %s."],
                        "request": ["Which city are you interested in?", "Which place?"]},

                "food_pref": {"inform": ["I like %s food.", "%s food.", "%s restaurant.", "%s."],
                              "request": ["What kind of food do you like?", "What type of restaurant?"]},

                "open": {"inform": ["The restaurant is %s.", "It is %s right now."],
                         "request": ["Tell me if the restaurant is open.", "What's the hours?"],
                         "yn_question": {'open': ["Is the restaurant open?"],
                                         'closed': ["Is it closed?"]
                                         }},

                "parking": {"inform": ["The restaurant has %s.", "This place has %s."],
                            "request": ["What kind of parking does it have?.", "How easy is it to park?"],
                            "yn_question": {'street parking': ["Does it have street parking?"],
                                            "valet parking": ["Does it have valet parking?"]
                                            }},

                "price": {"inform": ["The restaurant serves %s food.", "The price is %s."],
                          "request": ["What's the average price?", "How expensive it is?"],
                          "yn_question": {'expensive': ["Is it expensive?"],
                                          'moderate': ["Does it have moderate price?"],
                                          'cheap': ["Is it cheap?"]
                                          }},

                "default": {"inform": ["Restaurant %s is a good choice."],
                            "request": ["I need a restaurant.",
                                        "I am looking for a restaurant.",
                                        "Recommend me a place to eat."]}
                }

    usr_slots = [("loc", "location city", ["Pittsburgh", "New York", "Boston", "Seattle",
                                           "Los Angeles", "San Francisco", "San Jose",
                                           "Philadelphia", "Washington DC", "Austin"]),
                 ("food_pref", "food preference", ["Thai", "Chinese", "Korean", "Japanese",
                                                   "American", "Italian", "Indian", "French",
                                                   "Greek", "Mexican", "Russian", "Hawaiian"])]

    sys_slots = [("open", "if it's open now", ["open", "closed"]),
                 ("price", "average price per person", ["cheap", "moderate", "expensive"]),
                 ("parking", "if it has parking", ["street parking", "valet parking", "no parking"])]

    db_size = 100


class RestStyleSpec(DomainSpec):
    name = "restaurant_style"
    greet = "Hello there. I know a lot about places to eat."
    nlg_spec = {"loc": {"inform": ["I am at %s.", "%s.", "I'm interested in food at %s.", "At %s.", "In %s."],
                        "request": ["Which area are you currently locating at?", "well, what is the place?"]},

                "food_pref": {"inform": ["I like %s food.", "%s food.", "%s restaurant.", "%s."],
                              "request": ["What cusine type are you interested", "What do you like to eat?"]},

                "open": {"inform": ["This wonderful place is %s.", "Currently, this place is %s."],
                         "request": ["Tell me if the restaurant is open.", "What's the hours?"],
                         "yn_question": {'open': ["Is the restaurant open?"],
                                         'closed': ["Is it closed?"]
                                         }},

                "parking": {"inform": ["The parking status is %s.", "For parking, it does have %s."],
                            "request": ["What kind of parking does it have?.", "How easy is it to park?"],
                            "yn_question": {'street parking': ["Does it have street parking?"],
                                            "valet parking": ["Does it have valet parking?"]
                                            }},

                "price": {"inform": ["This eating place provides %s food.", "Let me check that for you. The price is %s."],
                          "request": ["What's the average price?", "How expensive it is?"],
                          "yn_question": {'expensive': ["Is it expensive?"],
                                          'moderate': ["Does it have moderate price?"],
                                          'cheap': ["Is it cheap?"]
                                          }},

                "default": {"inform": ["Let me look up in my database. A good choice is %s."],
                            "request": ["I need a restaurant.",
                                        "I am looking for a restaurant.",
                                        "Recommend me a place to eat."]}
                }

    usr_slots = [("loc", "location city", ["Pittsburgh", "New York", "Boston", "Seattle",
                                           "Los Angeles", "San Francisco", "San Jose",
                                           "Philadelphia", "Washington DC", "Austin"]),
                 ("food_pref", "food preference", ["Thai", "Chinese", "Korean", "Japanese",
                                                   "American", "Italian", "Indian", "French",
                                                   "Greek", "Mexican", "Russian", "Hawaiian"])]

    sys_slots = [("open", "if it's open now", ["open", "closed"]),
                 ("price", "average price per person", ["cheap", "moderate", "expensive"]),
                 ("parking", "if it has parking", ["street parking", "valet parking", "no parking"])]

    db_size = 100


class RestPittSpec(DomainSpec):
    name = "rest_pitt"
    greet = "I am an expert about Pittsburgh restaurant."

    nlg_spec = {"loc": {"inform": ["I am at %s.", "%s.", "I'm interested in food at %s.", "At %s.", "In %s."],
                        "request": ["Which city are you interested in?", "Which place?"]},

                "food_pref": {"inform": ["I like %s food.", "%s food.", "%s restaurant.", "%s."],
                              "request": ["What kind of food do you like?", "What type of restaurant?"]},

                "open": {"inform": ["The restaurant is %s.", "It is %s right now."],
                         "request": ["Tell me if the restaurant is open.", "What's the hours?"],
                         "yn_question": {'open': ["Is the restaurant open?"],
                                         'closed': ["Is it closed?"]
                                         }},

                "parking": {"inform": ["The restaurant has %s.", "This place has %s."],
                            "request": ["What kind of parking does it have?.", "How easy is it to park?"],
                            "yn_question": {'street parking': ["Does it have street parking?"],
                                            "valet parking": ["Does it have valet parking?"]
                                            }},

                "price": {"inform": ["The restaurant serves %s food.", "The price is %s."],
                          "request": ["What's the average price?", "How expensive it is?"],
                          "yn_question": {'expensive': ["Is it expensive?"],
                                          'moderate': ["Does it have moderate price?"],
                                          'cheap': ["Is it cheap?"]
                                          }},

                "default": {"inform": ["Restaurant %s is a good choice."],
                            "request": ["I need a restaurant.",
                                        "I am looking for a restaurant.",
                                        "Recommend me a place to eat."]}
                }

    usr_slots = [("loc", "location city", ["Downtown", "CMU", "Forbes and Murray", "Craig",
                                           "Waterfront", "Airport", "U Pitt", "Mellon Park",
                                           "Lawrance", "Monroveil", "Shadyside", "Squrill Hill"]),
                 ("food_pref", "food preference", ["healthy", "fried", "panned", "steamed", "hot pot",
                                                   "grilled", "salad", "boiled", "raw", "stewed"])]

    sys_slots = [("open", "if it's open now", ["open", "going to start", "going to close", "closed"]),
                 ("price", "average price per person", ["cheap", "average", "fancy"]),
                 ("parking", "if it has parking", ["garage parking", "street parking", "no parking"])]

    db_size = 150


class BusSpec(DomainSpec):
    name = "bus"
    greet = "Ask me about bus information."

    nlg_spec = {"from_loc": {"inform": ["I am at %s.", "%s.", "Leaving from %s.", "At %s.", "Departure place is %s."],
                             "request": ["Where are you leaving from?", "What's the departure place?"]},

                "to_loc": {"inform": ["Going to %s.", "%s.", "Destination is %s.", "Go to %s.", "To %s"],
                           "request": ["Where are you going?", "Where do you want to take off?"]},

                "datetime": {"inform": ["At %s.", "%s.", "I am leaving on %s.", "Departure time is %s."],
                             "request": ["When are you going?", "What time do you need the bus?"]},

                "arrive_in": {"inform": ["The bus will arrive in %s minutes.", "Arrive in %s minutes.",
                                         "Will be here in %s minutes"],
                              "request": ["When will the bus arrive?", "How long do I need to wait?",
                                          "What's the estimated arrival time"],
                              "yn_question": {k: ["Is it a long wait?"] if k>15 else ["Will it be here shortly?"]
                                              for k in range(0, 30, 5)}},

                "duration": {"inform": ["It will take %s minutes.", "The ride is %s minutes long."],
                             "request": ["How long will it take?.", "How much tim will it take?"],
                              "yn_question": {k: ["Will it take long to get there?"] if k>30 else ["Is it a short trip?"]
                                              for k in range(0, 60, 5)}},

                "default": {"inform": ["Bus %s can take you there."],
                            "request": ["Look for bus information.",
                                        "I need a bus.",
                                        "Recommend me a bus to take."]}
                }

    usr_slots = [("from_loc", "departure place", ["Downtown", "CMU", "Forbes and Murray", "Craig",
                                                  "Waterfront", "Airport", "U Pitt", "Mellon Park",
                                                  "Lawrance", "Monroveil", "Shadyside", "Squrill Hill"]),
                 ("to_loc", "arrival place", ["Downtown", "CMU", "Forbes and Murray", "Craig",
                                              "Waterfront", "Airport", "U Pitt", "Mellon Park",
                                              "Lawrance", "Monroveil", "Shadyside", "Squrill Hill"]),
                 ("datetime", "leaving time", ["today", "tomorrow", "tonight", "this morning",
                                               "this afternoon"] + [str(t+1) for t in range(24)])
                 ]

    sys_slots = [("arrive_in", "how soon it arrives", [str(t) for t in range(0, 30, 5)]),
                 ("duration", "how long it takes", [str(t) for t in range(0, 60, 5)])
                 ]

    db_size = 150


class WeatherSpec(DomainSpec):
    name = "weather"
    greet = "Weather bot is here."

    nlg_spec = {"loc": {"inform": ["I am at %s.", "%s.", "Weather at %s.", "At %s.", "In %s."],
                        "request": ["Which city are you interested in?", "Which place?"]},

                "datetime": {"inform": ["Weather %s", "%s.", "I am interested in %s."],
                             "request": ["What time's weather?", "What date are you interested?"]},

                "temperature": {"inform": ["The temperature will be %s.", "The temperature that time will be %s."],
                                "request": ["What's the temperature?", "What will be the temperature?"]},

                "weather_type": {"inform": ["The weather will be %s.", "The weather type will be %s."],
                                 "request": ["What's the weather type?.", "What will be the weather like"],
                                 "yn_question": {k: ["Is it going to be %s?" % k] for k in
                                                 ["raining", "snowing", "windy", "sunny", "foggy", "cloudy"]}
                                 },

                "default": {"inform": ["Your weather report %s is here."],
                            "request": ["What's the weather?.",
                                        "What will the weather be?"]}
                }

    usr_slots = [("loc", "location city", ["Pittsburgh", "New York", "Boston", "Seattle",
                                           "Los Angeles", "San Francisco", "San Jose",
                                           "Philadelphia", "Washington DC", "Austin"]),
                 ("datetime", "which time's weather?", ["today", "tomorrow", "tonight", "this morning",
                                                        "the day after tomorrow", "this weekend"])]

    sys_slots = [("temperature", "the temperature", [str(t) for t in range(20, 40, 2)]),
                 ("weather_type", "the type", ["raining", "snowing", "windy", "sunny", "foggy", "cloudy"])]

    db_size = 40


class MovieSpec(DomainSpec):
    name = "movie"
    greet = "Want to know about movies?"

    nlg_spec = {"genre": {"inform": ["I like %s movies.", "%s.", "I love %s ones.", "%s movies."],
                          "request": ["What genre do you like?", "Which type of movie?"]},

                "years": {"inform": ["Movies in %s", "In %s."],
                          "request": ["What's the time period?", "Movie in what years?"]},

                "country": {"inform": ["Movie from %s", "%s.", "From %s."],
                            "request": ["Which country's movie?", "Movie from what country?"]},

                "rating": {"inform": ["This movie has a rating of %s.", "The rating is %s."],
                           "request": ["What's the rating?", "How people rate this movie?"],
                           "yn_question": {"5": ["Does it have a perfect rating?"],
                                           "4": ["Does it have a rating of 4/5?"],
                                           "1": ["Does it have a very bad rating?"]}
                           },

                "company": {"inform": ["It's made by %s.", "The movie is from %s."],
                            "request": ["Which company produced this movie?.", "Which company?"],
                            "yn_question": {k: ["Is this movie from %s?" % k] for k in
                                            ["20th Century Fox", "Sony", "MGM", "Walt Disney", "Universal"]}
                            },

                "director": {"inform": ["The director is %s.", "It's director by %s."],
                             "request": ["Who is the director?.", "Who directed it?"],
                             "yn_question": {k: ["Is it directed by %s?" % k] for k in
                                             list(string.ascii_uppercase)}
                             },

                "default": {"inform": ["Movie %s is a good choice."],
                            "request": ["Recommend a movie.",
                                        "Give me some good suggestions about movies.",
                                        "What should I watch now"]}
                }

    usr_slots = [("genre", "type of movie", ["Action", "Sci-Fi", "Comedy", "Crime",
                                             "Sport", "Documentary", "Drama",
                                             "Family", "Horror", "War", "Music", "Fantasy", "Romance", "Western"]),

                 ("years", "when", ["60s", "70s", "80s", "90s", "2000-2010", "2010-present"]),

                 ("country", "where ", ["USA", "France", "China", "Korea",
                                        "Japan", "Germany", "Mexico", "Russia", "Thailand"])
                 ]

    sys_slots = [("rating", "user rating", [str(t) for t in range(5)]),
                 ("company", "the production company", ["20th Century Fox", "Sony", "MGM", "Walt Disney", "Universal"]),
                 ("director", "the director's name", list(string.ascii_uppercase))
                 ]

    db_size = 200


if __name__ == "__main__":
    # pipeline here
    # generate a fix 500 test set and 5000 training set.
    # generate them separately so the model can choose a subset for train and
    # test on all the test set to see generalization.

    test_size = 500
    train_size = 2000
    gen_bot = Generator()

    rest_spec = RestSpec()
    rest_style_spec = RestStyleSpec()
    rest_pitt_spec = RestPittSpec()
    bus_spec = BusSpec()
    movie_spec = MovieSpec()
    weather_spec = WeatherSpec()

    # restaurant
    gen_bot.gen_corpus("test", rest_spec, complexity.CleanSpec, test_size)
    gen_bot.gen_corpus("test", rest_spec, complexity.MixSpec, test_size)
    gen_bot.gen_corpus("train", rest_spec, complexity.CleanSpec, train_size)
    gen_bot.gen_corpus("train", rest_spec, complexity.MixSpec, train_size)

    # restaurant style
    gen_bot.gen_corpus("test", rest_style_spec, complexity.CleanSpec, test_size)
    gen_bot.gen_corpus("test", rest_style_spec, complexity.MixSpec, test_size)
    gen_bot.gen_corpus("train", rest_style_spec, complexity.CleanSpec, train_size)
    gen_bot.gen_corpus("train", rest_style_spec, complexity.MixSpec, train_size)

    # bus
    gen_bot.gen_corpus("test", bus_spec, complexity.CleanSpec, test_size)
    gen_bot.gen_corpus("test", bus_spec, complexity.MixSpec, test_size)
    gen_bot.gen_corpus("train", bus_spec, complexity.CleanSpec, train_size)
    gen_bot.gen_corpus("train", bus_spec, complexity.MixSpec, train_size)

    # weather
    gen_bot.gen_corpus("test", weather_spec, complexity.CleanSpec, test_size)
    gen_bot.gen_corpus("test", weather_spec, complexity.MixSpec, test_size)
    gen_bot.gen_corpus("train", weather_spec, complexity.CleanSpec, train_size)
    gen_bot.gen_corpus("train", weather_spec, complexity.MixSpec, train_size)

    # movie
    gen_bot.gen_corpus("test", movie_spec, complexity.CleanSpec, test_size)
    gen_bot.gen_corpus("test", movie_spec, complexity.MixSpec, test_size)
    gen_bot.gen_corpus("train", movie_spec, complexity.CleanSpec, train_size)
    gen_bot.gen_corpus("train", movie_spec, complexity.MixSpec, train_size)

    # restaurant Pitt
    gen_bot.gen_corpus("test", rest_pitt_spec, complexity.MixSpec, test_size)
    gen_bot.gen_corpus("train", rest_pitt_spec, complexity.MixSpec, train_size)
