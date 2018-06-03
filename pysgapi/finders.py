
"""Finders include functions to find giveaways and parse them
"""

#Native libraries
import random
from argparse import Namespace
from time import sleep
#Own modules
from .assets import Giveaway
from .helpers import steam_url_to_id, string_numbers_only, calculate_probability


def _parse_giveaways(kwargs):
    """Parse a HTML source to fetch all Giveaways from it
    (all params as dict)
    :param source:
    :param games_include:
    :param games_exclude:
    :param pages:
    :param max_level:
    :param max_points:
    """
    p = Namespace(**kwargs)
    giveaways = list()
    giveaways_urls = list()
    has_include = bool(p.games_include)
    has_exclude = bool(p.games_exclude)
    has_filter = has_include or has_exclude

    def _game_eligible(steamid):
        #Check if the game is included or not ignored of filters
        if not has_filter:
            return True
        if has_include:
            return str(steamid) in p.games_include
        if has_exclude:
            return str(steamid) not in p.games_exclude

    #Divs where all giveaways are
    ggaa_divs = p.source.html.find(".giveaway__summary")

    for ga_div in ggaa_divs:
        #find steam url
        ga_steamurl = ga_div.find(".giveaway__icon", first=True).absolute_links.pop()
        ga_steamid = steam_url_to_id(ga_steamurl)
        #Steam ID is also parsed from URL on Giveaway object constructor

        #check if we're interested on this game
        if not _game_eligible(ga_steamid):
            #skip to next giveaway if we're not interested on this game
            continue

        #find giveaway link and ID
        title_div = ga_div.find(".giveaway__heading__name", first=True)
        ga_url = next(e for e in title_div.absolute_links if "steamgifts.com/giveaway/" in e)
        #giveaway ID is parsed from URL on Giveaway object constructor
        #ga_id = _giveaway_url_to_id(ga_url)
        #ignore giveaway if it's repeated
        if ga_url in giveaways_urls:
            continue

        #find points (cost)
        #heading_div = ga_div.find(".giveaway__heading", first=True)
        ga_points = next(e.text for e in ga_div.find(".giveaway__heading__thin") if "P)" in e.text)
        ga_points = string_numbers_only(ga_points, parse_int=True)
        if isinstance(p.max_points, int) and ga_points > p.max_points:
            continue

        #find level required
        level_div = ga_div.find(".giveaway__column--contributor-level", first=True)
        if not level_div: #If no div found, no level required
            ga_level = 0
        else:
            ga_level = string_numbers_only(level_div.text, parse_int=True)
            if isinstance(p.max_level, int) and ga_level > p.max_level:
                continue

        #find game title
        ga_title = title_div.text

        #find number of entries
        ga_entries = ga_div.find(".giveaway__links", first=True).find("span", first=True).text
        ga_entries = string_numbers_only(ga_entries, parse_int=True)
        if isinstance(p.max_entries, int) and ga_entries > p.max_entries:
            continue
        if isinstance(p.min_probability, float) and calculate_probability(ga_entries) > p.min_probability:
            continue

        #find created datetime and user who created the giveaway
        right_div = ga_div.find(".text-right", first=True)
        ga_created_unixtime = int(right_div.find("span", first=True).attrs["data-timestamp"])
        ga_creator = right_div.find(".giveaway__username", first=True).text

        #find end datetime
        ga_end_div = next(
            d for d in ga_div.find("div")
            if "remaining" in d.text
            and "ago by" not in d.text
        )
        ga_end_unixtime = int(ga_end_div.find("span", first=True).attrs["data-timestamp"])

        #create Giveaway object
        giveaways.append(Giveaway(
            game=ga_title,
            steam_url=ga_steamurl,
            sg_url=ga_url,
            level=ga_level,
            points=ga_points,
            entries=ga_entries,
            creator=ga_creator,
            created=ga_created_unixtime,
            end=ga_end_unixtime,
            session=p.session
        ))
        giveaways_urls.append(ga_url)

    print("Found {} giveaways".format(len(giveaways)))
    return giveaways


def generic_find_giveaways(**kwargs):
    """Generic function to search giveaways
    :param session:
    :param games_include:
    :param games_exclude:
    :param pages:
    :param max_level:
    :param max_points:
    :param max_entries:
    :param min_probability:
    """
    giveaways = dict() #{giveawayID : giveawayObject}
    p = Namespace(**kwargs)
    for page in range(1, p.pages+1):
        print("Searching giveaways in page {}/{}".format(page, p.pages))
        r = p.session.get("https://www.steamgifts.com/giveaways/search?page={}".format(page))
        if "No results were found." in r.html.text:
            break
        parse_args = dict(kwargs)
        #parse_args["session"] = None
        parse_args["source"] = r
        ggaa = _parse_giveaways(parse_args)
        for ga in ggaa:
            giveaways[ga.giveaway_id] = ga
        if page < p.pages:
            #Random sleep before requesting the next page
            sleep(random.randint(1, 3))
    return list(giveaways.values())
