# rst_lib

These codes are the product of my scientific initiation.

I am adapting them to create a library that helps in the work of evaluating agreement between annotators who use the Rhetorical Structure Theory (RST) to annotate the same corpus.

### Tokenization.py: 

Extracts all tokens from a text, with token being the smallest unit of a text (words, commas, periods,...).

### rs3_treatment.py: 

Treats the rs3 file, an XML-based file that is the product of text annotation, so that the agreement analysis process between different annotations are made easier.

### agreement_analysis:

Analyzes the agreement of annotators when choosing tokens, based on two proposed metrics:

Gold Metric: Two annotators agree on choosing a token only if they annotated that token.

Silver Metric: Two annotators agree on the choice of a token if one of them selected the token, and the other selected another token within an "agreement window" of 5 tokens to the right or left (For example, if one annotator selected token 60, and the other selected token 57, they agree because 57 is within the token agreement window 60).

From these 2 analyzes a Krippendorf Alpha value is generated, which is a measure of agreement between annotations.