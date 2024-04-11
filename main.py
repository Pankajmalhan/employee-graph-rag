from dotenv import load_dotenv
from src.utils.llm import process_gpt
import os
def main():
   response = process_gpt('Your are math professor, answer my questions', 'what is square?')
   print(response)
   
if __name__ == "__main__":
   # Load environment variables
    load_dotenv()
    main()