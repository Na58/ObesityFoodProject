import json


class JsonProcessor:

    @staticmethod
    def map_mb_sa3(fname='../ProcessedData/meshblock.json'):
        mapping = dict()
        mb_data = json.load(open(fname))
        for data in mb_data:
            print(data)
            exit()
            mapping[data['mb_code_2016']] = (data['sa3_code'], data['sa3_name'])

        return mapping

    @staticmethod
    def map_mb_phn():
        mb_fname = '../ProcessedData/meshblock.json'
        mb_data = json.load(open(mb_fname))
        phn_mapping = JsonProcessor.get_sa3_phn_mapping()
        for item in mb_data:
            item['phn'] = phn_mapping[item['sa3_code']][1]

        result = json.dumps(mb_data)
        fhdle = open('../ProcessedData/Merged/meshblock_phnmarked.json', 'w') # meshblock data with phn
        fhdle.write(result)
        fhdle.flush()
        fhdle.close()

    @staticmethod
    def count_mb_resident():
        mb_fname = '../ProcessedData/Merged/meshblock_phnmarked.json'
        mb_data = json.load(open(mb_fname))

        phn_data = json.load(open('../ProcessedData/phn_result.json'))
        phn_code = phn_data.keys()

        for item in mb_data:
            try:
                record = phn_data[item['phn']]
                record['resident'] = record.setdefault('resident', 0) + item['resident']
            except:
                print('meshblock not in PHN record')
                continue

        result = json.dumps(phn_data)
        fhdle = open('../ProcessedData/Merged/phn_withTotalResident.json', 'w')
        fhdle.write(result)
        fhdle.flush()
        fhdle.close()


    @staticmethod
    def get_sa3_phn_mapping():
        phn_mapping = json.load(open('../ProcessedData/mapping.json'))
        return phn_mapping

    @staticmethod
    def map_abr_sa3():
        notexit_count = 0
        mapping = JsonProcessor.map_mb_sa3()

        phn_mapping = json.load(open('../ProcessedData/mapping.json'))

        abr_json = json.load(open('../ProcessedData/abr.json'))
        abr_with_sa3 = list()
        for item in abr_json:
            try:
                sa3 = mapping[item['mb_id']]
                item['sa3_code'] = sa3[0]
                item['sa3_name'] = sa3[1]
                try:
                    item['phn_code'] = phn_mapping[sa3[0]][1]
                    abr_with_sa3.append(item)
                except:
                    print('PHN not found: ', sa3[0])
            except:
                notexit_count += 1
                print('MB not found: ', item['abn'], ', ', item['mb_id'])
        result = json.dumps(abr_with_sa3)
        fhdle = open('../ProcessedData/Merged/abr_with_sa3.json', 'w')
        fhdle.write(result)
        fhdle.flush()
        fhdle.close()
        print(notexit_count)



if __name__ == '__main__':
    # JsonProcessor.map_abr_sa3()
    # JsonProcessor.map_mb_phn()
    # JsonProcessor.count_mb_resident()
    JsonProcessor.map_mb_sa3()