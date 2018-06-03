
"""Helpers include misc functions
"""

def string_numbers_only(inputstring, parse_int=False):
    #Remove everything but numbers from inputstring
    r = ''.join(filter(lambda x: x.isdigit(), inputstring))
    if parse_int:
        return int(r)
    return r

def string_has_numbers_only(inputstring):
    #Check if the provided inputstring ONLY has numbers on it
    if len(inputstring) == 0:
        return False
    numberstr = string_numbers_only(inputstring)
    return numberstr == inputstring

def steam_url_to_id(url):
    #url format: https://store.steampowered.com/app/463200/
    #split by "/"
    #ID is the only element in list with numbers only
    url = url.split("/")
    return next(c for c in url if string_has_numbers_only(c))

def giveaway_url_to_id(url):
    #url format: https://www.steamgifts.com/giveaway/ID/GAME
    #split by "/"
    #giveaway ID index is -2
    #return url.split("/")[-2]
    #giveaway ID has 5 characters and is right after "giveaway" chunk
    url = url.split("/")
    url_giveaway_position = url.index(next(c for c in url if c == "giveaway"))
    return next(c for c in url if len(c) == 5 and url.index(c) == url_giveaway_position+1)

def calculate_probability(n):
    return 1/n

def get_users(session, giveaway_url):
    """Get users that entered the given giveaway
    The function will loop through different available pages of the users list
    :param session: SG object HTMLSession
    :param giveaway_url:
    :return: List of Strings (usernames)
    """
    if giveaway_url[-1] != "/":
        giveaway_url += "/"
    giveaway_url += "entries/search?page="
    users = set()

    def _parse(r):
        for e in r.html.find(".table__column__heading"):
            users.add(e.text)

    #Get first page
    r = session.get(giveaway_url + "1")
    _parse(r)

    #Check if users list have more than one page
    pages_urls = tuple(e for e in r.html.absolute_links if giveaway_url in e)
    if not pages_urls:
        #Only one page of users
        last_page = False
    else:
        #Get number of last page of users
        last_page = max(
            string_numbers_only(
                e.split("/")[-1],
                parse_int=True
            ) for e in pages_urls
        )

    #Get users from other pages if giveaway has more than one page of users
    if last_page:
        for i in range(2, last_page+1):
            r = session.get(giveaway_url + str(i))
            _parse(r)

    return list(users)

