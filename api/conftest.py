"""This file is meant as a workaround for
adding this directory to the PYTHONPATH when running tests
with pytest. It is also used for making enviroment variables
available before tests
"""


from dotenv import load_dotenv


load_dotenv()