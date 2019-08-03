"""ASSETS
Secondary objects used by pysgapi
Giveaway is the object that represents a Giveaway found in SG website
"""

# # Native # #
from datetime import datetime

# # Package # #
from .helpers import giveaway_url_to_id, steam_url_to_id, calculate_probability, get_users


class Giveaway(object):
    def __init__(self, session, game, steam_url, sg_url, level, points, entries, created, creator, end):
        self._session = session
        # Game name
        self.game = game
        self.name = self.game
        self.title = self.game
        # Steam URL and ID
        self.steam_url = steam_url
        self.steam_link = self.steam_url
        self.steam_id = steam_url_to_id(steam_url)
        # Giveaway URL and ID
        self.sg_url = sg_url
        self.giveaway_url = self.sg_url
        self.url = self.sg_url
        self.id = giveaway_url_to_id(sg_url)
        self.giveaway_id = self.id
        # Giveaway level and points/cost
        self.level = level
        self.points = points
        self.cost = self.points
        # Number of entries (users who entered the giveaway)
        self.entries = entries
        # Created and End timestamps
        self.created_unix = created
        self.end_unix = end
        # User who created the giveaway
        self.creator = creator
        self.user = self.creator
        self.username = self.creator
        self.creator_url = "https://www.steamgifts.com/user/" + self.creator
        self.user_url = self.creator_url
        # Get created/end in datetime object (UTC)
        self.created_utc = datetime.fromtimestamp(created)
        self.end_utc = datetime.fromtimestamp(end)

    def get_remaining_time(self):
        """Calculate the giveaway remaining time
        :return: remaining time in seconds
        """
        dif = self.end_utc - datetime.utcnow()
        return dif.seconds

    def get_elapsed_time(self):
        """Calculate the time the giveaway has been active
        (since it was created until now)
        :return: elapsed time in seconds
        """
        dif = datetime.utcnow() - self.created_utc
        return dif.seconds
    
    def get_total_time(self):
        """Calculate the total life time of the giveaway
        (since it was created until it will end)
        :return: total life time in seconds
        """
        dif = self.end_utc - self.created_utc
        return dif.seconds

    def calculate_probability(self):
        """Calculate the probability to win the giveaway.
        Is the result of dividing 1/number of entries
        :return: probability as a float
        """
        return calculate_probability(self.entries)

    def get_users(self):
        """Get a full list of all the users who entered the giveaway.
        Read .entries variable if you just want to know the ammount of entries (users)
        :return: List of Strings with SG usernames
        """
        return get_users(
            session=self._session,
            giveaway_url=self.url
        )
