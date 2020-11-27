from Miner import Miner

def main():
    states = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RR", "RO", "RJ", "RN", "RS", "SC", "SP", "SE", "TO"]
    for state in states:
        miner = Miner(state, "result")
        miner.mine()

if __name__ == "__main__":
    main()