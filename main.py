import csv
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Parse registration source UTM parameters')
    parser.add_argument('input_file', type=open)
    parser.add_argument('-o', '--output-file',
                        default='parse-res.csv',
                        help='result output file name')
    args = parser.parse_args()
    in_file = csv.DictReader(args.input_file, delimiter=';')
    res = dict()
    for line in in_file:
        if line['utm_source'] not in res.keys():
            res[line['utm_source']] = {line['utm_medium']: {line['utm_campaign']: 1}}
        else:
            if line['utm_medium'] not in res[line['utm_source']].keys():
                res[line['utm_source']][line['utm_medium']] = {line['utm_campaign']: 1}
            else:
                if line['utm_campaign'] not in res[line['utm_source']][line['utm_medium']].keys():
                    res[line['utm_source']][line['utm_medium']][line['utm_campaign']] = 1
                else:
                    res[line['utm_source']][line['utm_medium']][line['utm_campaign']] += 1

    with open(args.output_file, 'w') as out_file:
        field_names = ['utm_source', 'utm_medium', 'utm_campaign', 'count']
        writer = csv.DictWriter(out_file, fieldnames=field_names, delimiter=';')
        writer.writeheader()
        for utm_source in res.keys():
            for utm_medium in res[utm_source].keys():
                for utm_campaign in res[utm_source][utm_medium].keys():
                    writer.writerow({'utm_source': utm_source, 'utm_medium': utm_medium, 'utm_campaign': utm_campaign,
                                     'count': res[utm_source][utm_medium][utm_campaign]})

    print(f'Parsing complete in file: {args.output_file}')
