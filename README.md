# NL-to-FOL-Converter

**Bachelor's Thesis — University of Messina (2018/2019)**  
A parser for converting natural language sentences into First-Order Logic (FOL) predicates.

---

## 📖 Abstract

This thesis explores the design and implementation of a Python-based parser that translates sentences written in natural language into formal First-Order Logic representations.

The system integrates modern NLP tools such as **spaCy** and **NeuralCoref** for linguistic analysis and coreference resolution, combined with a **MongoDB** database to store the processed sentences and extracted FOL terms.

Key features include:
- Dependency parsing and semantic role detection.
- Predicate and variable extraction.
- Coreference resolution.
- Storing results in a structured NoSQL database.

---

## 🏗️ Project Structure
├── src/    \
│ ├── dependency_switcher.py \
│ ├── entity.py\
│ ├── library.py \
│ ├── mongo.py \
│ ├── named_entity_recognition.py \
│ ├── parser.py \
│ ├── predicate.py \
│ ├── spacy_interaction.py \
│ └── variable.py \
├── A_parser_for_text_to_First_order_Logic_c.pdf (thesis report) \
└── README.md

## 🛠 Main Components

- `parser.py`: Main script orchestrating the parsing workflow.
- `dependency_switcher.py`: Handles various dependency relations.
- `spacy_interaction.py`: Interfaces with spaCy and NeuralCoref.
- `mongo.py`: Manages MongoDB interactions.
- `entity.py` & `predicate.py`: Define core data structures.
- `library.py`: Shared utility functions.

---

## 🧪 Example Flow

1️⃣ **Input sentence** →  
2️⃣ Processed by spaCy & NeuralCoref →  
3️⃣ Converted into FOL predicates & variables →  
4️⃣ Stored in MongoDB collections (`Sentences` and `Terms`).

## ⚙️ Technologies

- Python 3.x
- spaCy + NeuralCoref
- MongoDB
- pymongo

---

## 🎓 Acknowledgments

**Supervisors:**  
- Prof. Antonio Puliafito  
- Prof. Francesco Longo  
- Dott. Carmelo Fabio Longo