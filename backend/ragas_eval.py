import requests
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from langchain_ollama import ChatOllama, OllamaEmbeddings

# Your FastAPI RAG pipeline endpoint
API_URL = "http://localhost:8000/query"

# Define a batch of evaluation queries with ground truth
# (You can extend this list)
eval_queries = [
    {
        "question": "Who wrote 1984?",
        "ground_truth": "George Orwell"
    },
    {
        "question": "What is The Great Gatsby about?",
        "ground_truth": "A critique of the American Dream set in the Roaring Twenties."
    },
    {
        "question": "Who is the author of Pride and Prejudice?",
        "ground_truth": "Jane Austen"
    },
    {
        "question": "What genre is The Hitchhiker's Guide to the Galaxy?",
        "ground_truth": "Comedy science fiction"
    },
]

results = []

# Loop through queries, call FastAPI pipeline, and collect results
for q in eval_queries:
    try:
        response = requests.post(API_URL, json={"text": q["question"]})
        response.raise_for_status()
        data = response.json()

        results.append({
            "question": q["question"],
            "contexts": data.get("relevant_documents", []),
            "answer": data.get("llm_response", ""),
            "ground_truth": q["ground_truth"]
        })

    except Exception as e:
        print(f"Error querying API for: {q['question']} -> {e}")

# Convert results into a HuggingFace dataset
dataset = Dataset.from_list(results)

# Define Ollama model to use for evaluation (must be running locally)
ollama_llm = ChatOllama(model="hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF")

# Define Ollama embeddings for evaluation
ollama_embeddings = OllamaEmbeddings(model="hf.co/CompendiumLabs/bge-base-en-v1.5-gguf")

# Run RAGAS evaluation
metrics = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
    llm=ollama_llm,
    embeddings=ollama_embeddings,
)

print("\nRAGAS Evaluation Results:\n")
print(metrics)

# First eval attempt: {'faithfulness': 0.7500, 'answer_relevancy': 0.6726, 'context_precision': 1.0000, 'context_recall': 0.8167}
# Second eval attempt (after prompt tuning): {'faithfulness': 0.6250, 'answer_relevancy': 0.8721, 'context_precision': 0.9583, 'context_recall': 0.9500}
# Third attempt: {'faithfulness': 0.8333, 'answer_relevancy': 0.6383, 'context_precision': 0.9722, 'context_recall': 1.0000}