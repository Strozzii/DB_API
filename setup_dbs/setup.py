"""This module starts all scripts to set up the local databases"""

from init_scripts import postgres, neo, mongo

TEST_DATA_NUM = 1000

if __name__ == "__main__":

    postgres.setup(TEST_DATA_NUM)
    mongo.setup(TEST_DATA_NUM)
    neo.setup(TEST_DATA_NUM)
