from LinearRegressionModel import run_regression
from chatbot import get_gemini_response

def main():
    soh_value = run_regression()   # run your full regression file

    print("\n💬 Gemini Battery Health Assistant Ready!")
    while True:
        user_msg = input("\nAsk about battery health (or type 'exit'): ")

        if user_msg.lower() == "exit":
            break

        reply = get_gemini_response(user_msg, soh_value)
        print("\n Gemini:", reply)

if __name__ == "__main__":
    main()
