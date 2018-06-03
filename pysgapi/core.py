
"""Core includes the SG object, which is used to interact with pysgapi
"""

#Installed libraries
from requests_html import HTMLSession
#Own modules
from .finders import generic_find_giveaways


class SG(object):
    """The SG object can search giveaways in the Steamgifts site
    Methods:
        - find_giveaways
    """
    def __init__(self, proxy=None):
        #self.proxy = proxy #TODO
        self.session = HTMLSession()
        #find_giveaways aliases
        self.find = self.find_giveaways
        self.get_giveaways = self.find_giveaways
        self.search_giveaways = self.find_giveaways

    def find_giveaways(self, games_include=[], games_exclude=[], pages=1, max_level=None, max_points=None, max_entries=None, min_probability=None):
        """Find giveaways from the Steamgifts site
        A set of parameters can be defined to filter giveaways by:
        :param games_include: List/tuple of Steam App ID for games to search *
        :param games_exclude: List/tuple of Steam App ID for games to ignore *
        :param pages: Number of pages to search (default=1)
        :param max_level: Level required limit (inclusive) (default=None)
        :param max_points: Giveaway cost in points limit (inclusive) (default=None)
        :param max_entries: Limit of entries (users that entered the giveaway) (inclusive) (default=None)
        :param min_probability: Minimum probability to win the giveaway (float, inclusive)
        * When using games_include, games_exclude will be ignored
        * games filters must be lists; to avoid using one filter, use an empty list
        """
        return generic_find_giveaways(
            session=self.session,
            games_include=games_include,
            games_exclude=games_exclude,
            pages=pages,
            max_level=max_level,
            max_points=max_points,
            max_entries=max_entries,
            min_probability=min_probability
        )
