import re
import json
import itertools


street_regex = r'([Ss][Oo][Kk]([\.\s])*)|([Ss][Oo][Kk][Aa][Kk][\.\s])|([Ss][Kk][\.\s])'
boulevard_regex = r'([Bb][Uu][Ll][Vv][Aa][Rr][Iı])|([Bb][Uu][Ll][Vv]([\.\s])*)|((\s)+[Bb][Ll][Vv]([\.\s])+)'
district_regex = r'([Mm][Aa][Hh]([\.\s])+)|([Mm][Hh]([\.\s])+)|(\s)+([Mm][\.\s])'
avenue_regex = r'([Cc][Aa][Dd][Dd][Ee][Ss][İiIı]([\.\s])*)|([Cc][Aa][Dd]([\.\s])*)|([Cc][Dd][\.\s])|([Cc][\.\s])'
apt_regex = r'([Aa][Pp][Aa][Rr][Tt][Mm][Aa][Nn][Iı][\.\s])|([Aa][Pp][Tt][\.\s])'
no_regex = r'[Nn][Oo][:\.\s]'
my_regex = '|'.join([street_regex, boulevard_regex, district_regex, avenue_regex, no_regex, apt_regex, r'(\/\s)'])

# CHANGE TO YOUR FILE NAME
INPUT_FILE_NAME = 'adres.txt'

label_regex_dict = {
	'street': street_regex,
	'boulevard': boulevard_regex,
	'district': district_regex,
	'avenue': avenue_regex,
	'apartment': apt_regex
}

invalid = [None, '.', '/', '/ ', ' ']


def grouper(L, n):
	args = [iter(L)] * n
	return ([e for e in t if e != None] for t in itertools.zip_longest(*args))


def get_lines(f_name):
	res = []

	with open(f_name, 'r') as f:
		for line in f:
			res.append([e.strip() for e in re.split(my_regex, line[:-1]) if not e in invalid])

	return res
	

def make_dict_from_line(r):
	d = {}
	splitted = re.split(r' ', r[-2])

	for e in grouper(r[:-2], 2):
		if e[0] != '' and e[0] != ' ':
			label = ([ l for l, regex in label_regex_dict.items() if re.search(regex, " ".join(e)) != None] + ['other'])[0]
			d[label] = e[0]

	no_or_desc = " ".join(splitted[:-1]).strip()
	if no_or_desc != '':
		d['no' if re.search(r'[0-9]', no_or_desc) != None else 'desc'] = no_or_desc

	d['county'] = splitted[-1].strip()
	d['province'] = r[-1]

	return d


def write_to_file(f_name, data):
	with open(f_name, 'w') as f:
		f.write(json.dumps({'data': data}, indent=2, ensure_ascii=False))


lines = get_lines(INPUT_FILE_NAME)
result = [make_dict_from_line(line) for line in lines]
write_to_file('output.json', result)
