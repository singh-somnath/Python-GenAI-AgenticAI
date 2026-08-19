from llm_factory import get_llm
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate,FewShotPromptTemplate


def main():
    try:
        llm = get_llm()

        ####PromptTemplate
        '''        
        prompt_template = PromptTemplate(
            input_variables=["type","format"],
            template="Explain with example {type} in {format} format"
        )
        filled_prompt = prompt_template.format(type="few shot prompting", format="Beginner friendly")
        response = llm.invoke(filled_prompt)
        print(response.content)        
        '''  

        ####ChatMessagePromptTemplate
        '''          
        message = ChatPromptTemplate.from_messages([
            ("system","You are an assistant that help to teach AI related stuff to 10 year old kids."),
            ("user","{topic}")
        ])
        response = llm.invoke(message.format_messages(topic="What is few shot prompt in langchain"))
        print(response.content)
        '''
        
        #####Few Shot Prompting
        '''
        examples = [
            {"text":"I love this product","sentiment":"positive"},
            {"text":"The service is terrible","sentiment":"negative"}
        ]

        promtTemplate = PromptTemplate(
            input_variables=["text","sentiment"],
            template="Text : {text}\n Sentiment:{sentiment}"
        )

        prompt=FewShotPromptTemplate(
            examples=examples,
            example_prompt = promtTemplate,
            prefix="Classify the sentiment using the example",
            suffix="Text :\n {text}\nSentiment:",
            input_variables=["text"]            
        )     
        response = llm.invoke(prompt.format(text="Food taste is african"))
        print(response.content)
        '''

        #####Chain of thought prompting

        
    except Exception as e:
        print(f"Error : {e}")


if __name__ == "__main__":
    main()
