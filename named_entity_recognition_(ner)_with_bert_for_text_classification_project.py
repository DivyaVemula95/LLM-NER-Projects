# -*- coding: utf-8 -*-
"""Named Entity Recognition (NER) with BERT for Text Classification Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_HUWtDkpWJ-397mrLXZ04c1MAbNZCS0Q

# **Title**: **Named Entity Recognition (NER) with BERT for Text Classification**

### **Objective**:
**This project demonstrates the application of a pre-trained BERT model to perform Named Entity Recognition (NER) on text data, identifying entities such as locations, organizations, and persons in a given corpus.**

## **Install Required Libraries**
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install transformers datasets

"""## **Import required libraries and dataset**"""

from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
from datasets import load_dataset

"""## **Load the pre-trained model and tokenizer for NER**"""

# Load the pre-trained model and tokenizer for NER
model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

"""**Initialize the NER pipeline**"""

# Initialize the NER pipeline
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)

"""## **Load the dataset**"""

# Load the CoNLL-03 dataset
dataset = load_dataset("conll2003")

# Preview a sample from the dataset
print(dataset['train'][0])

"""## **Perform NER**"""

# Extract text from the dataset and perform NER
num_samples_to_print = 5  # Set the number of samples to print
count = 0

for sample in dataset['test']:
    if count >= num_samples_to_print:
        break  # Stop after printing the specified number of samples

    text = " ".join(sample['tokens'])
    print(f"Text: {text}")

    # Perform Named Entity Recognition (NER) on the text
    entities = ner_pipeline(text)

    # Clean up entity tokens to merge subwords
    cleaned_entities = []
    current_entity = ''
    current_label = ''
    current_score = 0.0

    for entity in entities:
        word = entity['word']
        label = entity['entity']
        score = entity['score']

        # Skip empty or irrelevant tokens (like '-')
        if word in ['-', ''] or score < 0.5:  # Adjust the threshold score as needed
            continue

        # If it's a subword token (i.e., starting with "##"), append to the current entity
        if word.startswith('##'):
            current_entity += word[2:]
        else:
            # If there is a previous entity, save it
            if current_entity:
                cleaned_entities.append({'word': current_entity, 'label': current_label, 'score': current_score})

            # Reset for the new entity
            current_entity = word
            current_label = label
            current_score = score

    # Don't forget to add the last entity
    if current_entity:
        cleaned_entities.append({'word': current_entity, 'label': current_label, 'score': current_score})

    # Print the cleaned entities with score
    for entity in cleaned_entities:
        print(f"Entity: {entity['word']} | Label: {entity['label']} | Score: {entity['score']}")
    print("\n")

    count += 1  # Increment the count

"""## **save the model and tokenizer**"""

model.save_pretrained("./ner_model")
tokenizer.save_pretrained("./ner_model")

"""## **Sampling the dataset**"""

from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import pipeline

# Load the NER model (Hugging Face's pipeline for NER)
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

# Initialize a list to store the entity types
entity_labels = []

# Sample the first 100 samples or another subset of the dataset to test
sample_size = 5
subset = dataset['test'][:sample_size]
# Print a single sample from the dataset to inspect its structure
print(dataset['test'][0])

"""## **Visulaizations**"""

from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import pipeline

# Load the NER model (Hugging Face's pipeline for NER)
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

# Initialize a list to store the entity types
entity_labels = []

# Sample the first 5 samples or another subset of the dataset to test
sample_size = 5
subset = [dataset['test'][i] for i in range(sample_size)]

# Print the first sample to inspect its structure
print("Sample 0:", dataset['test'][0])  # Check the structure of the first sample

# Process the subset and collect entity labels
for i, sample in enumerate(subset):
    print(f"Processing sample {i}: {sample}")
    # Ensure 'sample' is a dictionary and contains the 'tokens' key
    if isinstance(sample, dict) and 'tokens' in sample:
        text = " ".join(sample['tokens'])  # Join the tokens into a single string
        entities = ner_pipeline(text)  # Apply the NER pipeline to extract entities

        print(f"Entities for sample {i}: {entities}")  # Debugging: print the entities

        # Collect the labels of the recognized entities
        for entity in entities:
            label = entity['entity']
            entity_labels.append(label)
    else:
        print(f"Skipping invalid sample: {sample}")  # Debugging step to handle invalid samples

# Count the occurrences of each entity label
entity_counts = Counter(entity_labels)
print("Entity counts:", entity_counts)  # Debugging: print the entity counts

# Plot the distribution of entity labels (Bar plot)
plt.figure(figsize=(10, 6))
sns.barplot(x=list(entity_counts.keys()), y=list(entity_counts.values()), palette='viridis')
plt.title('Entity Type Distribution')
plt.xlabel('Entity Type')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.show()

# The percentage distribution as a pie chart
plt.figure(figsize=(8, 8))
plt.pie(entity_counts.values(), labels=entity_counts.keys(), autopct='%1.1f%%', startangle=140, colors=sns.color_palette('Set3', len(entity_counts)))
plt.title('Entity Type Distribution (Pie Chart)')
plt.show()

"""**Plot Explanation**

The dominant entity type in your dataset is locations (I-LOC), which makes up
more than half of the entities.

* Persons (I-PER) form nearly a quarter of the entities, which signifies a    
  substantial presence of names of individuals.

* Miscellaneous entities (I-MISC) also have a significant presence, suggesting
  diverse types of entities that don't fall into standard categories.

* Organizations (I-ORG), while present, form a smaller part of the dataset
  compared to the other categories.
"""