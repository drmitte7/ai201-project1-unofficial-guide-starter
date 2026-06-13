import os
import gradio as gr
from groq import Groq
from embed import retrieve
from dotenv import load_dotenv

load_dotenv()

# Load Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def ask(question):
    # Extract professor name keywords to improve retrieval
    search_query = question
    name_mappings = {
        "cheikhna": "Cheikhna Mahawa Diagana calc professor reviews",
        "diagana": "Cheikhna Mahawa Diagana calc professor reviews",
        "ethan": "Ethan Atkin professor reviews math",
        "atkin": "Ethan Atkin professor reviews math",
        "jania": "Jania Begum professor reviews math",
        "begum": "Jania Begum professor reviews math",
        "souad": "Souad Ajarar professor reviews math",
        "ajarar": "Souad Ajarar professor reviews math",
        "thea": "Thea Pignataro professor reviews math",
        "pignataro": "Thea Pignataro professor reviews math",
    }
    for keyword, expanded in name_mappings.items():
        if keyword in question.lower():
            search_query = expanded
            break

    # Retrieve relevant chunks
    results = retrieve(search_query, top_k=5)

    # Build context from retrieved chunks
    context_parts = []
    sources = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        context_parts.append(doc)
        if meta["source"] not in sources:
            sources.append(meta["source"])

    context = "\n\n".join(context_parts)

    # Build prompt
    prompt = f"""You are a helpful assistant that answers questions about professors at The City College of New York (CCNY).
Answer the question using ONLY the information provided in the documents below.
If a document is not about the professor mentioned in the question, ignore it completely.
If the documents don't contain enough information to answer, say "I don't have enough information on that."
Always be specific and reference what students said.
Only cite sources that are actually relevant to your answer.

Documents:
{context}

Question: {question}

Answer:"""

    # Generate response
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": sources
    }


def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

# Build Gradio interface
with gr.Blocks(title="CCNY Unofficial Guide") as demo:
    gr.Markdown("# CCNY Unofficial Professor Guide")
    gr.Markdown("Ask questions about Math professors at City College of New York based on real student reviews.")
    
    inp = gr.Textbox(label="Your question", placeholder="e.g. What do students say about Prof. Cheikhna's exams?")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()