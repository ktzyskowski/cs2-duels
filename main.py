from processing.features.marshall import extract_features_from_rounds
from processing.parser import parse_json

if __name__ == "__main__":
    parsed_rounds = list(parse_json(path="res/json/0a5040e7-f972-4e0d-b9bf-ee6dfbdf0342.json"))
    features = extract_features_from_rounds(parsed_rounds)
    print(len(parsed_rounds))
