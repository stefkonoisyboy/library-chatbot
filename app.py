import ollama
from fastapi import FastAPI, HTTPException
import chromadb
from chromadb.utils import embedding_functions
from chromadb.api.types import EmbeddingFunction
import uvicorn
from pydantic import BaseModel
from typing import List



app = FastAPI()

# Initialize ChromaDB
chroma_client = chromadb.Client()

ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    model_name="hf.co/CompendiumLabs/bge-base-en-v1.5-gguf"
)

# Create a collection for our books
collection = chroma_client.create_collection(
    name="books_collection",
    embedding_function=ollama_ef # type: ignore
)

# Book data
book_data = [
    {"title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "summary": "A comedy science fiction series that follows the adventures of Arthur Dent after the Earth is destroyed."},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "summary": "A novel of manners, following the Bennet sisters and their pursuit of love and social standing."},
    {"title": "1984", "author": "George Orwell", "summary": "A dystopian novel set in a totalitarian society under constant surveillance."},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "summary": "A story of racial injustice and childhood innocence in the Deep South."},
    {"title": "Moby-Dick", "author": "Herman Melville", "summary": "A sailor narrates the obsessive quest of Captain Ahab for revenge on the white whale."},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "summary": "A critique of the American Dream set in the Roaring Twenties."},
    {"title": "War and Peace", "author": "Leo Tolstoy", "summary": "A sweeping novel that interweaves the lives of several families during the Napoleonic Wars."},
    {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "summary": "A psychological drama of guilt and redemption following a young man who commits murder."},
    {"title": "Brave New World", "author": "Aldous Huxley", "summary": "A dystopian future where pleasure and conformity dominate society."},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "summary": "A teenage boy's disillusionment with the adult world."},
    {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "summary": "An epic fantasy quest to destroy a powerful ring and save Middle-earth."},
    {"title": "Jane Eyre", "author": "Charlotte Brontë", "summary": "A governess navigates love, independence, and moral challenges."},
    {"title": "Wuthering Heights", "author": "Emily Brontë", "summary": "A tale of intense and tragic love set on the Yorkshire moors."},
    {"title": "Frankenstein", "author": "Mary Shelley", "summary": "A scientist creates life with dire consequences in this gothic classic."},
    {"title": "Dracula", "author": "Bram Stoker", "summary": "A vampire count terrorizes England in this horror masterpiece."},
    {"title": "The Odyssey", "author": "Homer", "summary": "The long journey of Odysseus returning home from the Trojan War."},
    {"title": "The Iliad", "author": "Homer", "summary": "An epic poem about the Trojan War and the wrath of Achilles."},
    {"title": "Les Misérables", "author": "Victor Hugo", "summary": "The struggles of ex-convict Jean Valjean during a time of political upheaval in France."},
    {"title": "The Brothers Karamazov", "author": "Fyodor Dostoevsky", "summary": "A philosophical and psychological exploration of faith, doubt, and morality."},
    {"title": "The Count of Monte Cristo", "author": "Alexandre Dumas", "summary": "A story of betrayal, revenge, and redemption."},
    {"title": "Great Expectations", "author": "Charles Dickens", "summary": "The personal growth and development of an orphan named Pip."},
    {"title": "David Copperfield", "author": "Charles Dickens", "summary": "A semi-autobiographical novel about a young man's journey to maturity."},
    {"title": "The Grapes of Wrath", "author": "John Steinbeck", "summary": "A family's struggle during the Great Depression as they migrate westward."},
    {"title": "Of Mice and Men", "author": "John Steinbeck", "summary": "Two displaced ranch workers struggle to achieve their dream during the Great Depression."},
    {"title": "Animal Farm", "author": "George Orwell", "summary": "A satirical tale about farm animals rebelling against their human owner."},
    {"title": "Fahrenheit 451", "author": "Ray Bradbury", "summary": "In a future society, books are banned and burned to suppress dissent."},
    {"title": "Slaughterhouse-Five", "author": "Kurt Vonnegut", "summary": "A time-traveling soldier experiences the bombing of Dresden."},
    {"title": "Catch-22", "author": "Joseph Heller", "summary": "A satirical look at the absurdities of war and military bureaucracy."},
    {"title": "The Stranger", "author": "Albert Camus", "summary": "An existential novel about a man who is indifferent to social norms."},
    {"title": "Don Quixote", "author": "Miguel de Cervantes", "summary": "A delusional knight sets out to revive chivalry."},
    {"title": "A Tale of Two Cities", "author": "Charles Dickens", "summary": "A story of love and sacrifice set during the French Revolution."},
    {"title": "Lolita", "author": "Vladimir Nabokov", "summary": "A controversial novel about obsession and manipulation."},
    {"title": "Beloved", "author": "Toni Morrison", "summary": "A haunting story about a former slave and the ghost of her dead child."},
    {"title": "One Hundred Years of Solitude", "author": "Gabriel García Márquez", "summary": "A multigenerational saga set in the fictional town of Macondo."},
    {"title": "The Old Man and the Sea", "author": "Ernest Hemingway", "summary": "An aging fisherman struggles with a giant marlin in the Gulf Stream."},
    {"title": "The Sun Also Rises", "author": "Ernest Hemingway", "summary": "American expatriates search for meaning in post-WWI Europe."},
    {"title": "On the Road", "author": "Jack Kerouac", "summary": "A semi-autobiographical tale of cross-country adventures and Beat culture."},
    {"title": "Rebecca", "author": "Daphne du Maurier", "summary": "A young bride is haunted by the memory of her husband's first wife."},
    {"title": "A Clockwork Orange", "author": "Anthony Burgess", "summary": "A dystopian novel exploring free will and state control."},
    {"title": "The Handmaid's Tale", "author": "Margaret Atwood", "summary": "A chilling look at a theocratic society that subjugates women."},
    {"title": "Life of Pi", "author": "Yann Martel", "summary": "A boy survives a shipwreck and shares a lifeboat with a Bengal tiger."},
    {"title": "The Road", "author": "Cormac McCarthy", "summary": "A father and son journey through a post-apocalyptic wasteland."},
    {"title": "The Alchemist", "author": "Paulo Coelho", "summary": "A shepherd's journey to fulfill his personal legend."},
    {"title": "Gone with the Wind", "author": "Margaret Mitchell", "summary": "A sweeping romance set during the American Civil War."},
    {"title": "Memoirs of a Geisha", "author": "Arthur Golden", "summary": "A fictional tale of a Japanese girl's transformation into a geisha."},
    {"title": "The Kite Runner", "author": "Khaled Hosseini", "summary": "A story of friendship and redemption set in Afghanistan."},
    {"title": "Water for Elephants", "author": "Sara Gruen", "summary": "A young man joins a traveling circus during the Great Depression."},
    {"title": "The Book Thief", "author": "Markus Zusak", "summary": "A young girl finds solace in books during Nazi Germany."},
    {"title": "The Secret Garden", "author": "Frances Hodgson Burnett", "summary": "An orphan girl discovers a locked garden and transforms lives with it."},
    {"title": "Little Women", "author": "Louisa May Alcott", "summary": "The lives and growth of four sisters during the Civil War era."}
]

# Prepare data for ChromaDB
documents = [f"{book['title']} is about {book['summary']} It is written by: {book['author']}" for book in book_data]
ids = [str(i) for i in range(len(documents))]

# Add documents to the collection
collection.add(
    documents=documents,
    ids=ids
)

class Query(BaseModel):
    text: str
    top_k: int = 3

@app.post("/query")
async def query_books(query: Query):
    try:
        # Query the collection
        results = collection.query(
            query_texts=[query.text],
            n_results=query.top_k
        )

        documents_list = results.get("documents")
        distances_list = results.get("distances")

        # Handle missing or empty results safely
        if not documents_list or not isinstance(documents_list, list) or not documents_list[0]:
            return {
                "relevant_documents": [],
                "distances": [],
                "llm_response": "I couldn't find any relevant documents to answer your question."
            }

        documents = documents_list[0]
        distances = distances_list[0] if distances_list and isinstance(distances_list, list) else []
        
        # Get LLM response
        instruction_prompt = (
            "You are a helpful chatbot.\n"
            "Use only the following pieces of context to answer the question. Don't make up any new information:\n"
            + "\n".join([f" - {doc}" for doc in documents])
        )

        stream = ollama.chat(
            model="hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF",
            messages=[
                {'role': 'system', 'content': instruction_prompt},
                {'role': 'user', 'content': query.text},
            ]
        )

        return {
            "relevant_documents": documents,
            "distances": distances,
            "llm_response": stream['message']['content']
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
