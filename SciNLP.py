import os
import scispacy
import spacy
import pandas as pd
from spacy import displacy
from scispacy.abbreviation import AbbreviationDetector
from scispacy.linking import EntityLinker
from openpyxl import load_workbook


dfs = pd.read_excel('xlsxfiles/biobankrepo.xlsx', sheet_name='biobank scraped pdfs')

# print('data = {}'.format(dfs))
# print(type(dfs))
tempdf = dfs.iloc[[2]]  # pulls out the 2nd index or 3rd row
# print(tempdf.iloc[0, 3])  # pulls out the 3rd index or 4th column of the 3rd row
# text = tempdf.iloc[0, 3]
# text = "specimens are prepared for electron microscopy and semi -thin sections stained with toluidine blue are reviewed prior to thin sectioning for ultrastructural examination . electron microscopy demonstrates patent capillary loops . the glomerular architecture demonstrates corrugation and thickening of basement membranes with no subepithelial deposits and no intramembranous deposits . the tubules show dilated mitochondria and injury . there is global effacement of foot processes . there are no subendothelial deposits . the mesangium shows an increase in matrix . mesangial electron dense deposits are not identified . "

word_bank = [['ifta', 'interstitial fibrosis tubular atrophy'], ['if/ta', 'interstitial fibrosis/tubular atrophy'], 'interstitial fibrosis/tubular atrophy', 'interstital fibrosis', 'tubular atrophy', 'fibrosis', 'tubular injury', 'tubulitis', 'infiltrate', 'crescents', ['ain', 'acute interstitial nephritis'],
             ['acute interstitial nephritis'], ['cin', 'contrast-induced nephropathy'], 'glomeruli', 'global glomerulosclerosis', 'segmental glomerulosclerosis', 'interstitial infiltrate', 'eosinophils', 'acute tubular injury', 'cores-michels', 'cores-zeus', 'arteriosclerosis', 'mesangial expansion', 'mesangial hypercellularity', 'cores-light']

# text = 'SBMA Rick has fibrosis, IFTA, IF, TA. There is extrememe interstital fibrosis and tubular atrophy with little fibrosis. Sarah has tubular injury with moderate infiltrate and wide crescents.'
text = 'aki with possible vanco toxicity -atn versus ain '

# nlp_sm = spacy.load('en_core_sci_sm')  # download/load scispacy medical verbage library
# nlp_sm.add_pipe("scispacy_linker", config={"linker_name": "umls", "max_entities_per_mention": 3})
# linker = nlp_sm.get_pipe("scispacy_linker")
# nlp_large = spacy.load('en_core_sci_lg')
# nlp = spacy.load('en_ner_bionlp13cg_md')
# nlp_large.add_pipe("abbreviation_detector")
# nlp_large.add_pipe("abbreviation_detector")
# doc_sm = nlp_sm(text)  # generate nlp processed doc
# doc_large = nlp_large(text)

# print('Entered text = {}\n\n'.format(list(doc.sents)))
# print('Entries = {}'.format(doc.ents))


# GETS ABBREVIATIONS OUT OF TEXT
# print(f"{abrv} \t ({abrv.start}, {abrv.end}) {abrv._.long_form}")

# GETS ENTITIES OUT OF TEXT (pulling out verbs/adjectives out of EM)
# for ent in doc_large.ents:
#     print('"{}" has label {}'.format(ent.text, ent.label_))

# GETS TOKENS OUT OF TEXT
# for token in doc_sm:
#     print('token = {}\t\t head = {}\t\t children = {}'.format(
#         token.text, token.head.text, list(token.children)))

# GET ENTITIES OUT OF TEXT
# for ent in doc_med.ents:
#     print('entity = "{}"'.format(ent.text))

# DISPLAY ENTITIES USING DISPLACY
# displacy.serve(doc_large, style="ent")


# for chunk in doc_med.noun_chunks:
#     print('text = "{}"\t\troot = {}\t\tdep = {}'.format(
#         chunk.text, chunk.root.text, chunk.root.dep_))
# for chunk in doc_large.noun_chunks:
#     print('text = "{}"\t\troot = {}\t\tdep = {}'.format(
#         chunk.text, chunk.root.text, chunk.root.dep_))


# display sentence structure/relations in webpage
# displacy.serve(doc, style='dep')

# homepath = '/Users/anshulgowda/Documents/CODE/KUH2022/xlsfiles'
# processedpath = '/Users/anshulgowda/Documents/CODE/KUH2022/xlsxfiles'
# # for doc in os.listdir(os.getcwd()):
# for doc in os.listdir('/Users/anshulgowda/Documents/CODE/KUH2022/xlsxfiles'):
#     print(doc)
#     os.rename('{}/{}'.format(processedpath, doc, ), '{}/{}'.format(processedpath, doc))

# Add the abbreviation pipe to the spacy pipeline.
# nlp_sm.add_pipe("abbreviation_detector")
# doc = nlp_sm("(CLL), autoimmune hemolytic anemia, and oral ulcer. The patient was diagnosed with chronic lymphocytic leukemia and was noted to have autoimmune hemolytic anemia at the time of his CLL diagnosis.")
# fmt_str = "{:<6}| {:<30}| {:<6}| {:<6}"
# print(fmt_str.format("Short", "Long", "Starts", "Ends"))
# for abrv in doc._.abbreviations:
#     print(fmt_str.format(abrv.text, str(abrv._.long_form), abrv.start, abrv.end))

# Entity Linker
# fmt_str = "{:<20}| {:<10}| {:<32}| {:<20}"
# print(fmt_str.format("Entity", "1st CUI", "Canonical Name", "Definition"))
# for entity in doc_sm.ents:
#     first_cuid = entity._.kb_ents[0][0]
#     kb_entry = linker.kb.cui_to_entity[first_cuid]
#     print(fmt_str.format(entity.text, first_cuid,
#                          kb_entry.canonical_name, kb_entry.definition[0:15] + "..."))

nlp = spacy.load("en_core_sci_sm")
nlp.add_pipe("scispacy_linker", config={"resolve_abbreviations": True, "linker_name": "umls"})
doc = nlp(" worsening renal insufficiency since 1 /2021, history of systemic therapy for metastatic pancreatic cancer. kidney , biopsy : - focal and segmental glomerulosclerosis , favor primary - diffuse acute tubular injury. - severe arterionephrosclerosis - acute tubular injury")
linker = nlp.get_pipe("scispacy_linker")

fmt_str = "{:<32} | {:<15} | {:<30} | {:<40}"
print(fmt_str.format("Entity", "1st CUI", "Canonical Name", "Definition"))

for entity in doc.ents:
    try:  # WEIRD error where ATI is repeated, but a CUI is only generated for the repeat instance
        first_cuid = entity._.kb_ents[0][0]
        kb_entry = linker.kb.cui_to_entity[first_cuid]
    except IndexError:
        print(fmt_str.format(entity.text, 'CUI INDERROR', 'NO ENTRY FOUND', 'NO DEF'))
    # CUI generated but not found in db, examine word parts inside?
    if(None in [kb_entry.canonical_name, kb_entry.definition]):
        print(fmt_str.format(entity.text, 'xxxxxxxx', 'NO ENTRY FOUND', 'NO DEF'))

        # further resolves entities without a match, by analyzing dependencies, possibly redo CUI search on the HEAD
        # if the HEAD is not the same as the entity (insinuating actual dependency)
        subtext = entity.text
        sub_doc = nlp(subtext)
        sub_fmt_str = "\t{:<15} ~ {:<15} ~ {:<35}"
        for token in sub_doc:
            print(sub_fmt_str.format(
                token.text, token.head.text, '{}'.format(list(token.children))))
    else:
        print(fmt_str.format(entity.text, first_cuid,
                             kb_entry.canonical_name, kb_entry.definition[0:40] + "..."))

# entity = doc.ents[1]
# for umls_ent in entity._.kb_ents:
#     print(linker.kb.cui_to_entity[umls_ent[0]])
