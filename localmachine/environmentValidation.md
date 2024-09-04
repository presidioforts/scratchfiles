from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import SpacyNlpEngine, NlpEngineProvider

# Initialize SpacyNlpEngine with the local model
spacy_nlp = SpacyNlpEngine({"en": "en_core_web_lg"})
provider = NlpEngineProvider(nlp_engine=spacy_nlp)
nlp_engine = provider.create_engine()

# Initialize AnalyzerEngine with the custom NLP engine
analyzer = AnalyzerEngine(nlp_engine=nlp_engine)


results = analyzer.analyze(text="My phone number is 555-555-5555", entities=["PHONE_NUMBER"], language="en")
print(results)
