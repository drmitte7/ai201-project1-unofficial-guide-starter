# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

The official college website at The City College of New York list courses and faculty at the Math Department. However, it contains no information about teaching style, exam dificulty, or grading. This system would make that information searchable by plain-language questions.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate My Professors | Reviews of Prof. Cheikhna Mahawa Diagana | https://www.ratemyprofessors.com/professor/1179010 - Cheikhna_Mahawa_Diagana_Rate_My_Professors.txt|
| 2 | Reddit | Reddit Reviews of Prof. Cheikhna Mahawa Diagana | https://www.reddit.com/r/CCNY/comments/1dgmol6/best_prof_for_calc_1/ - Cheikhna_Mahawa_Diagana_Reddit.txt |
| 3 | Rate My Professors | Reviews of Prof. Ethan Atkin | https://www.ratemyprofessors.com/professor/186989 - Ethan_Atkin_Rate_My_Professors.txt |
| 4 | Reddit | Reddit Reviews of Prof. Ethan Atkin | https://www.reddit.com/r/CCNY/comments/1ko6srh/comment/mssd2sv/ - Ethan_Atkin_Reddit.txt |
| 5 | Rate My Professors | Reviews of Prof. Jania Begum | https://www.ratemyprofessors.com/professor/2276465 - Jania_Begum_Rate_My_Professors.txt |
| 6 | Reddit | Reddit Reviews of Prof. Jania Begum | https://www.reddit.com/r/CCNY/comments/1oxcqv9/jania_begum_for_differential_equations/ - Jania_Begun_Reddit.txt |
| 7 | Rate My Professors | Reviews of Prof. Souad_Ajarar | https://www.ratemyprofessors.com/professor/2670073 - Souad_Ajarar_Rate_My_Professors.txt |
| 8 | Reddit | Reddit Reviews of Prof. Souad_Ajarar | https://www.reddit.com/r/CCNY/comments/1tcilvw/calc_2_with_souad_ajarar/ - Souad_Ajarar_Reddit.txt |
| 9 | Rate My Professors | Reviews of Prof. Thea Pignataro | https://www.ratemyprofessors.com/professor/631569 - Thea_Pignataro_Rate_My_Professors.txt |
| 10 | Reddit | Reddit Reviews of Prof. Thea Pignataro | https://www.reddit.com/r/CCNY/comments/1o5zkn5/exam_and_grading_of_prof_pignataro/ - Thea_Pignataro_Reddit.txt |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 200 characters

**Overlap:** 30 characters

**Reasoning:** Each professor review is typically 1-3 sentences long. A chunk size of 200 characters keeps one review together as a single chunk without merging multiple reviews. A small overlap of 30 characters ensures that if a review is slightly longer and gets split, the key opinion at the boundary is not lost.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers. Runs locally with no API key or rate limits.

**Top-k:** 5 chunks per query.

**Production tradeoff reflection:** For a real deployment, I would consider: multilingual support if international students write reviews in other languages; a larger context window model if reviews were longer; and a hosted API model like OpenAI's text-embedding-3-small for better accuracy on domain-specific text, at the cost of paying per API call and sending data to an external server.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about Prof. Cheikhna's exams? | Exams are very similar to the review sheets he gives out. Practice exams are almost identical to real exams. |
| 2 | Is attendance mandatory in Prof. Ethan Atkin's class? | No, attendance is optional except for test days |
| 3 | Does Prof. Cheikhna curve exams? | Yes, he adds 3-5 extra points on exams. |
| 4 | What do students say about Prof. Ethan Atkin's grading? | He is a harsh grader, stingy with partial credit, and does not drop exams. |
| 5 | Do students recommend Prof. Cheikhna for Calc 1? | Yes, most students recommend him, saying he is caring and his exams are fair. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Professor names may appear differently across documents — for example "Cheikhna", "Diagana" and the embedding model may not connect these as the same person, causing retrieval to miss relevant chunks.

2. Some reviews are very short (one sentence like "Nahhhhhhhh") and may not carry enough meaning for the embedding model to match them to a specific query, making retrieval unreliable for those chunks.

---

## Architecture

.txt files --> Document Ingestion(Python/ope()) --> Text Cleaning(remove extra spaces, blank line) --> Chunking(200 char, 30 overlap) --> Embedding(sentence-transformers / all-MiniLM-L6-v2) --> Vector Store(ChromaDB) --> Retrival(ChromaDB similarity search — top 5 chunks) --> Generation(Groq / llama-3.3-70b-versatile) -->  Answer + Sources(Gradio web interface)

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:** I will give Claude my Domain section, Documents table, and Chunking Strategy section and ask it to implement a script that loads all 10 .txt files, cleans them, and splits them into 200 character chunks with 30 character overlap. I will verify the output by printing 5 chunks and checking they are readable and self-contained.

**Milestone 4 — Embedding and retrieval:** I will give Claude my Architecture diagram and ask it to implement the embedding step using all-MiniLM-L6-v2 and store the chunks in ChromaDB with source metadata. I will verify by running 3 test queries and checking that the returned chunks are relevant.

**Milestone 5 — Generation and interface:** I will give Claude my Architecture diagram and grounding requirement and ask it to implement the generation step using Groq llama-3.3-70b-versatile and build a Gradio interface with an input box for questions and output boxes for the answer and sources. I will verify by checking that every response includes a source citation.
