import json

class _tv_database:

    # CONSTRUCTOR

    def __init__(self):
        self.tv_details   = dict()  # Holds general information about TV shows
        self.tv_ratings   = dict()  # Holds ratings of TV shows
        self.tv_summaries = dict()  # Holds summaries, images, and websites for TV shows
        self.tv_episodes  = dict()  # Holds lists of episodes for TV shows
        self.users        = dict()  # Holds a dictionary of all users

    # METHODS FOR TV SHOWS

    def load_tv_shows(self, tv_file):

        # Open and read JSON file containing TV shows
        with open(tv_file, encoding="utf-8") as f:
            data = json.load(f)

        # Loop through each show and populate dictionaries
        for show in data:
            tvid = show["id"]

            # Populate tv_details
            self.tv_details[tvid] = dict()
            self.tv_details[tvid]["id"]             = show["id"]
            self.tv_details[tvid]["name"]           = show["name"]
            self.tv_details[tvid]["genres"]         = show["genres"]
            self.tv_details[tvid]["status"]         = show["status"]
            self.tv_details[tvid]["episode-length"] = show["runtime"]
            self.tv_details[tvid]["schedule"]       = show["schedule"]

            if show["network"]:
                self.tv_details[tvid]["network"]    = show["network"]["name"]
            else:
                self.tv_details[tvid]["network"]    = show["webChannel"]["name"]

            # Populate tv_ratings
            self.tv_ratings[tvid] = show["rating"]["average"]

            # Populate tv_summaries
            self.tv_summaries[tvid] = dict()
            self.tv_summaries[tvid]["images"]            = dict()
            self.tv_summaries[tvid]["website"]           = show["officialSite"]
            self.tv_summaries[tvid]["images"]["medium"]  = show["image"]["medium"]
            self.tv_summaries[tvid]["images"]["regular"] = show["image"]["original"]
            self.tv_summaries[tvid]["summary"]           = show["summary"]

            # Populate tv_episodes
            self.tv_episodes[tvid] = show["_embedded"]["episodes"]

    def get_tv_shows(self):
        return self.tv_details.keys()

    def get_tv_details(self, tvid=None):
        if tvid is not None:
            try:
                details = self.tv_details[tvid]
            except Exception as e:
                details = None
        else:
            return self.tv_details

        return details

    def get_tv_rating(self, tvid=None):
        if tvid is not None:
            try:
                rating = self.tv_ratings[tvid]
            except Exception as e:
                rating = None
        else:
            return self.tv_ratings

        return rating

    def get_tv_summary(self, tvid=None):
        if tvid is not None:
            try:
                summary = self.tv_summaries[tvid]
            except Exception as e:
                summary = None
        else:
            return self.tv_summaries

        return summary

    def get_tv_episodes(self, tvid=None):
        if tvid is not None:
            try:
                episodes = self.tv_episodes[tvid]
            except Exception as e:
                episodes = None
        else:
            return self.tv_episodes

        return episodes

    def set_tv_show(self, tvid, details={}, rating={}, summary={}, episodes={}):
        self.tv_details[tvid]   = details
        self.tv_ratings[tvid]   = rating
        self.tv_episodes[tvid]  = episodes
        self.tv_summaries[tvid] = summary

    # METHODS FOR USERS

    def load_users(self, users_file):

        # Open and read JSON file containing users
        with open(users_file) as f:
            data = json.load(f)

        # Populate users
        for user in data.keys():
            self.users[user] = data[user]

    def get_users(self):
        return self.users.keys()

    def get_user(self, uid=None):
        if uid is not None:
            try:
                user = self.users[uid]
            except Exception as e:
                user = None
        else:
            return self.users

        return user

    def set_attribute(self, uid, attribute, value):
        self.users[uid][attribute] = value

    def set_user(self, uid, details={}):
        self.users[uid] = details

if __name__ == '__main__':
    tvdb = _tv_database()

    tvdb.load_tv_shows('tv-shows.json')
    tvdb.load_users('users.json')

    print(json.dumps(tvdb.users, indent=2))

