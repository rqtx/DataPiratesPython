from Miner import Miner
import json
import os

def load_jsonl(input_path) -> list:
    """
    Read list of objects from a JSON lines file.
    """
    data = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.rstrip('\n|\r')))
    print('Loaded {} records from {}'.format(len(data), input_path))
    return data

def test1():
    miner = Miner("DF", save=False)
    result = miner.mine()
    dirname = os.path.dirname(__file__)
    expected = load_jsonl(os.path.join(dirname, "DF.jsonl"))
    assert result == expected