from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import SpacyNlpEngine, NlpEngineProvider

# Initialize the SpaCy NLP Engine
spacy_nlp_engine = SpacyNlpEngine({"en": "en_core_web_lg"})

# Create the NlpEngineProvider with the SpaCy engine
provider = NlpEngineProvider(nlp_engines={"en": spacy_nlp_engine})
nlp_engine = provider.create_engine()

# Initialize AnalyzerEngine with the custom NLP engine
analyzer = AnalyzerEngine(nlp_engine=nlp_engine)

# Test analyzer with some sample text
results = analyzer.analyze(text="My phone number is 555-555-5555", entities=["PHONE_NUMBER"], language="en")
print(results)
