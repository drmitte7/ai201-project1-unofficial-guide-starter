# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

The official City College of New York (CCNY) website lists courses and faculty but provides no insight into teaching style, exam difficulty, grading policies, or workload. This tool makes informal student knowledge — collected from Rate My Professors and Reddit — searchable through plain-language questions, giving students honest answers about Math Department professors that they cannot find through official channels.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 200 characters

**Overlap:** 30 characters

**Why these choices fit your documents:** Professor reviews are short and self-contained, typically 1-3 sentences. Rather than splitting by character count, the final implementation splits by review boundary using "Review #" as a delimiter, keeping each complete review as one chunk. This ensures no review is cut in half mid-sentence

**Final chunk count:** 57 chunks across 10 documents

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:** For a real deployment serving CCNY students, I would consider several tradeoffs. If international students write reviews in other languages, I would need a multilingual model like paraphrase-multilingual-MiniLM-L12-v2. If reviews were longer and more detailed, a model with a larger context window would capture more meaning per chunk. For higher accuracy on domain-specific academic text, a hosted API model like OpenAI's text-embedding-3-small would perform better.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** The system prompt explicitly instructs the LLM to answer using only the retrieved documents and to ignore any chunks not related to the professor being asked about:

"You are a helpful assistant that answers questions about professors at The City College of New York (CCNY). Answer the question using ONLY the information provided in the documents below. If a document is not about the professor mentioned in the question, ignore it completely. If the documents don't contain enough information to answer, say 'I don't have enough information on that.' Always be specific and reference what students said. Only cite sources that are actually relevant to your answer."

**How source attribution is surfaced in the response:** Source attribution is handled programmatically — not left to the LLM. After retrieval, the code collects the source filename from the metadata of every retrieved chunk and displays them in a separate "Retrieved from" box in the Gradio interface. This means every response is always accompanied by the list of source documents it drew from, regardless of what the LLM generates.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about Prof. Cheikhna's exams? | Exams are very similar to review sheets he provides | Exams are based on review sheets with 10 questions; same questions appear on the test with different numbers | Relevant | Accurate |
| 2 | Is attendance mandatory in Prof. Ethan Atkin's class? | No, attendance is optional except for test days | One student attended only 1 lecture and never went again, suggesting attendance is not mandatory | Partially relevant | Partially accurate |
| 3 | Does Prof. Cheikhna curve exams? | Yes, he adds 3-10 extra points on exams | I don't have enough information on that | Off-target | Inaccurate |
| 4 | What do students say about Prof. Ethan Atkin's grading? | Harsh grader, stingy with partial credit | Students say he is a harsh grader who takes off considerable points for minor mistakes | Relevant | Accurate |
| 5 | Do students recommend Prof. Cheikhna for Calc 1? | Yes, most students recommend him | Yes, students recommend him — described as best professor, kind, and explains concepts repeatedly | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** Does Prof. Cheikhna curve exams?

**What the system returned:** I don't have enough information on that. There is no mention of Prof. Cheikhna curving exams in the provided reviews.

**Root cause (tied to a specific pipeline stage):** This is a retrieval failure caused by a vocabulary mismatch at the embedding stage. The query used the word "curve" but the actual reviews describe the same concept using different words — "extra points", "adds 3-5 points", and "bonus points". The all-MiniLM-L6-v2 embedding model did not match the semantic meaning of "curve" to these phrases closely enough to retrieve the relevant chunks. As a result, the LLM never saw the evidence it needed to answer correctly and correctly reported that it had no information.

**What you would change to fix it:** There are two possible fixes. First, I could add synonyms to the query before retrieval — for example, expanding "curve" to "curve bonus extra points exams" to increase the chance of matching the right chunks. Second, I could use a larger and more powerful embedding model that better captures semantic equivalence between "curve" and "adds extra points", such as OpenAI's text-embedding-3-small, which handles paraphrase matching more accurately than all-MiniLM-L6-v2.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** Writing the chunking strategy in planning.md before writing any code forced me to think carefully about the structure of my documents. Because I had already noted that reviews are short and self-contained, I recognized quickly during Milestone 3 that splitting by character count was cutting reviews in half. The spec gave me a clear goal — one chunk per review — which led to switching to a delimiter-based splitting approach using "Review #" as the boundary marker. Without that spec decision written down, I might have kept the character-based approach without realizing it was producing bad chunks.

**One way your implementation diverged from the spec, and why:** The spec specified a chunk size of 200 characters with 30 character overlap. During implementation I discovered that character-based chunking was splitting reviews mid-sentence, which produced incomplete and unreadable chunks. I diverged from the spec by switching to review-boundary chunking using "Review #" as a delimiter instead. This produced 57 complete, self-contained chunks that were much more meaningful for retrieval. I updated planning.md to reflect this change.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* My Chunking Strategy section from planning.md, my Documents table, and the pipeline diagram. I asked Claude to implement a script that loads all 10 .txt files, cleans them, and splits them into chunks.
- *What it produced:* A complete ingest.py script that loaded documents, cleaned text, and split by character count with 200 character chunks and 30 character overlap
- *What I changed or overrode:* The character-based chunking was splitting reviews mid-sentence. I switched to delimiter-based chunking using "Review #" as the boundary marker, which kept each complete review as one chunk. I also reduced the overlap to 0 since reviews are self-contained and do not need overlap.

**Instance 2**

- *What I gave the AI:* My Retrieval Approach section, pipeline diagram, and grounding requirement. I asked Claude to implement embed.py using all-MiniLM-L6-v2 and ChromaDB, and app.py with a Groq generation step and Gradio interface.
- *What it produced:* A complete embed.py with embedding and retrieval functions, and app.py with a Gradio interface showing answer and sources boxes.
- *What I changed or overrode:* The initial retrieval was returning chunks from wrong professors because the embedding model did not connect short first names like "Cheikhna" to the full filename. I added a name mapping dictionary that expands short professor names into full name queries before retrieval, which significantly improved retrieval accuracy.
