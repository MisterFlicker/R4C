import json

def example():
    new_file = open('help_file.txt', 'w')
    input = {
        "model":"YTA",
        "version":"D2",
        "created":"2022-12-31 23:59:59"
             }
    json.dump(input, new_file)
    new_file.close()


example()