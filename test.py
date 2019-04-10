
def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)


def test_languages(cldf_dataset, cldf_logger):
    assert len(list(cldf_dataset['LanguageTable'])) == 40


# Our word lists were compiled for 37 well-described UA languages, drawing
# principally on Miller’s Uto- Aztecan Cognate Sets (Miller, 1967, 1988), as
# revised and expanded by Hill (2011b).
def test_sources(cldf_dataset, cldf_logger):
    assert len(cldf_dataset.sources) == 4


def test_parameters(cldf_dataset, cldf_logger):
    assert len(list(cldf_dataset['ParameterTable'])) == 102


def test_forms(cldf_dataset, cldf_logger):
    assert len(list(cldf_dataset['FormTable'])) == 4728
    # NorthernPaiute-9-2,,NorthernPaiute,9,jɑi | jɑɁi,jɑɁi,,,Wheeler2014,,
    lex = [f for f in cldf_dataset['FormTable'] if f['ID'] == 'NorthernPaiute-9-2']
    assert lex[0]['Value'] == 'jɑi | jɑɁi'
    assert lex[0]['Form'] == 'jɑɁi'
