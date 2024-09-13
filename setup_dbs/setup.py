"""This module starts all scripts to set up the local databases"""

from init_scripts import postgres, mongo, neo

if __name__ == "__main__":

    # mongo.setup()
    # postgres.setup()
    neo.setup()
