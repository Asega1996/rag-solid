from ragas import evaluate, EvaluationDataset
from ragas.llms import llm_factory
from ragas.metrics import Faithfulness, LLMContextRecall, FactualCorrectness
from openai import OpenAI

from query import retriever, rag_chain

test_cases = [
    {
        "question": "What is the Single Responsibility Principle?",
        "reference": "A class should have only one reason to change, meaning it should be responsible for a single piece of functionality."
    },
    {
        "question": "What is the Open/Closed Principle?",
        "reference": "Software entities should be open for extension but closed for modification."
    },
    {
        "question": "What is the Liskov Substitution Principle?",
        "reference": "Objects of a derived class must be substitutable for objects of the base class without breaking the correctness of the program."
    },
    {
        "question": "What is the Interface Segregation Principle?",
        "reference": "No client should be forced to depend on methods it does not use; prefer several small, specific interfaces over one large, general one."
    },
    {
        "question": "What is the Dependency Inversion Principle?",
        "reference": "High-level modules should not depend on low-level modules; both should depend on abstractions."
    },
]


dataset = []
for case in test_cases:
    question = case["question"]
    retrieved_docs = retriever.invoke(question)
    response = rag_chain.invoke(question)
    dataset.append({
        "user_input": question,
        "retrieved_contexts": [doc.page_content for doc in retrieved_docs],
        "response": response,
        "reference": case["reference"],
    })

evaluation_dataset = EvaluationDataset.from_list(dataset)

client = OpenAI(
    api_key="ollama",  # Ollama no requiere una key real
    base_url="http://localhost:11434/v1"
)
evaluator_llm = llm_factory("llama3.1:8b", provider="openai", client=client)

result = evaluate(
    dataset=evaluation_dataset,
    metrics=[Faithfulness(), LLMContextRecall(), FactualCorrectness()],
    llm=evaluator_llm,
)

print(result)
result.to_pandas().to_csv("eval_results.csv", index=False)
print("\nResultados guardados en eval_results.csv")