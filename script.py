from pprint import pprint
from tabulate import tabulate


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

def get_usefull_information(vote_sections):
    parsed = []
    for section in vote_sections:
        parsed.append({
            'localitate': section[2].strip(),
            'alegatori_inscrisi': int(section[4]),
            'alegatori_normali': int(section[6]),
            'alegatori_suplimentare': int(section[7]) + int(section[8]),
            'total_alegatori_care_au_votat': int(section[5]),
            'ponta': int(section[16]),
            'iohannis': int(section[14])
        })
    return parsed


def get_most_special_sections(data):
    sections = [{'localitate': x['localitate'],
                 'raport_speciali_votat': x['alegatori_suplimentare'] / x['total_alegatori_care_au_votat'] * 100,
                 'raport_votat_inscrisi': x['total_alegatori_care_au_votat'] / x['alegatori_inscrisi'] * 100,
                 'alegatori': x['total_alegatori_care_au_votat'],
                 'candidat_ponta': x['ponta'] / x['total_alegatori_care_au_votat'] * 100,
                 'candidat_iohannis': x['iohannis'] / x['total_alegatori_care_au_votat'] * 100,
                 'voturi_ponta': x['ponta']}
                for x in data]
    top_furt = sorted(sections, key=lambda x: x['raport_speciali_votat'], reverse=True)[:20]
    return sorted(top_furt, key=lambda x: x['voturi_ponta'], reverse=True)


def make_table(data):
    table = [['Localitate', 'Voturi Totale', 'Raport Suplimentare/Total',
             'Raport Votat/Inscrisi', 'Ponta', 'Iohannis', 'Voturi Ponta']]
    for row in data:
        table.append([row['localitate'], row['alegatori'], row['raport_speciali_votat'],
                     row['raport_votat_inscrisi'], row['candidat_ponta'], row['candidat_iohannis'], row['voturi_ponta']])
    return table

def main():
    vote_sections = []
    with open('raw_data.txt') as stream:
        lines = stream.readlines()
        vote_sections = chunks(lines, 27)
    data = get_usefull_information(vote_sections)
    special_data = get_most_special_sections(data)
    print(tabulate(make_table(special_data), headers="firstrow", numalign="right"))

if __name__ == "__main__":
    main()
