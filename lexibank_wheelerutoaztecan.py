import pathlib

from pylexibank import FormSpec, Dataset as BaseDataset

# Website: https://wardwheeler.wordpress.com/data-sets/
URL = "https://www.dropbox.com/s/dbmb9myyk3r1zg4/supplementary_materials.zip?dl=1"

# "Our word lists were compiled for 37 well-described UA languages, drawing
# principally on Miller’s Uto- Aztecan Cognate Sets (Miller, 1967, 1988), as
# revised and expanded by Hill (2011b)."
SOURCES = ['Miller1967', 'Miller1988', 'Hill2011', 'Wheeler2014']


def concept2id(c):
    c = c.strip()
    for char in ' /(),.':
        c = c.replace(char, '_')
    return c


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "wheelerutoaztecan"
    form_spec = FormSpec(
        separators='|',
        replacements=[('\xad', '')],
    )

    def cmd_download(self, args):
        subdir = 'supplementary_materials'
        filelist = [
            # raw data
            'UA100wordlistLATEXandCharisSIL3252013.xls',
            # not used yet, but contains detailed source info
            'Notesondatabaseentries32013.pdf',
        ]
        self.raw_dir.download_and_unpack(
            URL, *[pathlib.Path(subdir, f) for f in filelist], log=args.log)
        self.raw_dir.xls2csv(filelist[0],)

    def cmd_makecldf(self, args):
        rows = self.raw_dir.read_csv('UA100wordlistLATEXandCharisSIL3252013.Sheet1.csv')
        concepts = [(i, concept2id(rows[0][i])) for i in range(1, len(rows[0]), 2)]
        languages = {l['Label']: l for l in self.languages}

        args.writer.add_sources()
        args.writer.add_concepts(id_factory=lambda c: concept2id(c.english))
        for row in rows[3:]:
            row = [col.strip() for col in row]
            if not row[0]:
                continue

            # language label is ugly, so we have manually constructed IDs
            label = row[0]
            assert label in languages, 'unknown language %s' % label

            args.writer.add_language(
                ID=languages[label]['ID'],
                Name=languages[label]['Name'],
                Glottocode=languages[label]['Glottocode'],
                Glottolog_Name=languages[label]['Name'],
                ISO639P3code=languages[label]['ISO639P3code']
            )

            for concept_id, concept in concepts:
                if row[concept_id]:
                    args.writer.add_lexemes(
                        Language_ID=languages[label]['ID'],
                        Parameter_ID=concept,
                        Value=row[concept_id],
                        Source=SOURCES
                    )
