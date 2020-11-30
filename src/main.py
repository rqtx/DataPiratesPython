from Miner import Miner

def main():
    print("Mining data")
    states = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RR", "RO", "RJ", "RN", "RS", "SC", "SP", "SE", "TO"]
    for state in states:
        try:
            miner = Miner(state, datafolder="result")
            miner.mine()
        except Exception as e:
            print("Error mining state " + state + "\n")
            print(e)

    print("End miner")

if __name__ == "__main__":
    main()