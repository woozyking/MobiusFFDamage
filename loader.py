import tablib


els = {
    'F': 'Fire',
    'A': 'Wind',
    'E': 'Earth',
    'W': 'Water',
    'L': 'Light',
    'D': 'Dark',
}
job_stats = [
    'HP',
    'Attack',
    'Break',
    'Magic',
    'Crit',
    'Spd',
    'Def',
    'Fire',
    'Water',
    'Wind',
    'Earth',
    'Light',
    'Dark',
    'Fire Res',
    'Water Res',
    'Wind Res',
    'Earth Res',
    'Light Res',
    'Dark Res',
    'Exploit Weakness',
    'Painful Break',
    'Improved Crits',
    'Ability/Attuned Chain',
    'Piercing Break',
    'Flash Break',
    'Quick Break',
    'Scourge',
    'Steel-guard',
    'Base Attributes',
    'Boost Ultimate',
    'Attack Limit Break',
]


def jobs(filename: str = None):
    if filename is None:
        filename = './data/jobstats2.csv'

    raw = tablib.Dataset().load(open(filename).read())
    ds = tablib.Dataset()
    ds.headers = raw.headers

    for row in raw:
    	r = list(row)
    	for i in list(range(7, 10)) + list(range(16, 22)) + list(range(22, 41)):
    		r[i] = r[i] or 0

    	ds.append(r)

    data = ds.dict

    for row in data:
        row['Orb Sets'] = [
            [els.get(row.pop('Orb 1'), ''), els.get(row.pop('Orb 2'), ''), els.get(row.pop('Orb 3'), '')],
        ]
        o4, o5, o6 = els.get(row.pop('Orb 4'), ''), els.get(row.pop('Orb 5'), ''), els.get(row.pop('Orb 6'), '')
        if o4 and o5 and o6:
            row['Orb Sets'].append([o4, o5, o6])

        row['Types'] = [row.pop('Type')]
        lore = row.pop('Lore')
        if lore:
            row['Types'].append(lore)

        for key in job_stats:
            row[key] = int(row[key])

    ds.dict = data
    return ds


if __name__ == '__main__':
    data = jobs()

    with open('./data/jobs.json', 'w') as f:
        f.write(data.export('json'))
