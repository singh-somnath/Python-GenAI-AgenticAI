from llm_factory import get_llm


def main():
    try:
        llm = get_llm()
        response  = llm.invoke("What is the capital of spain?")
        print(response.content if response.content else response)

    except Exception as e:
        print(f"Error : {e}")


if __name__ == "__main__":
    main()
