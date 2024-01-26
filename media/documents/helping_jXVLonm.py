import json

def example():
    new_file = open('help_file.json', 'w')
    input = {
        "model":"GG",
        "version":"D2",
        "created":"2022-12-31 23:59:59"
             }
    json.dump(input, new_file)
    new_file.close()


example()