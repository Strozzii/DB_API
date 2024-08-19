"""This module starts all scripts to set up the local databases"""

from init_scripts import postgres, neo, mongo

if __name__ == "__main__":
    postgres.setup()
    mongo.setup()
    neo.setup()
