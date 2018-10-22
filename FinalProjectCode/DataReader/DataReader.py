import json
import pandas as pd
import csv


class DataProcessor:

    @staticmethod
    # Process the Mesh Block data to extract Mesh Block code, and SA2 code
    def process_meshblock(fname='../Data/Meshblock/data8844001472353983152_Melb.json',
                          target_fname='../ProcessedData/meshblock.json'):
        fhdle = open(fname)
        meshblock_data = json.load(fhdle)['features']
        fhdle.close()
        fhdle = open('../Data/Meshblock/data2434847221826108841_RestVic.json')
        meshblock_data_RestVic = json.load(fhdle)['features']
        meshblock_data += meshblock_data_RestVic

        processed_data = []

        sa2_mapper = DataProcessor.extract_sa2_pha()

        for data in meshblock_data:
            try:
                item = dict()
                item['mb_code_2016'] = data['properties']['mb_code_2016']
                sa2_code = int(data['properties']['sa2_maincode_2016'])
                item['resident'] = data['properties']['person']
                item['pha_code'] = sa2_mapper[sa2_code]

                processed_data.append(item)

            except:
                print('error data', data)
                exit()
        json_str = json.dumps(processed_data)

        fhdle = open(target_fname, 'w')
        fhdle.write(json_str)
        fhdle.flush()
        fhdle.close()

    @staticmethod
    # Return a mapping between Mesh Block code and PHA code
    def get_mb_pha_mapper():
        mapper = dict()
        sa2_pha_mapper = DataProcessor.extract_sa2_pha()
        with open('../Data/Meshblock/MB_2016_VIC.csv') as fhdl:
            reader = csv.reader(fhdl)
            next(reader, None)
            error_count = 0
            total_count = 0
            for row in reader:
                total_count += 1
                try:
                    mb_code = row[0]
                    sa2_code = row[4]
                    mapper[mb_code] = sa2_pha_mapper[int(sa2_code)]
                except:
                    error_count += 1
                    continue
            print(error_count, ' out of ', total_count)

        return mapper

    @staticmethod
    # Process the restaurant data
    def process_abr(fname='../Data/ABR/abr_takeaway_20170327.json', target_fname='../ProcessedData/abr.json'):
        fhdle = open(fname)
        abr_data = json.load(fhdle)['features']
        fhdle.close()
        processed_data = dict()

        mapper = DataProcessor.get_mb_pha_mapper()

        not_exit = 0
        total = 0
        for data in abr_data:
            total += 1
            item = {}
            try:
                item['coor'] = data['geometry']['coordinates']
            except:
                item['coor'] = None
                continue
            try:
                item['pha_code'] = str(mapper[data['properties']['gnaf_pid']])
                processed_data[data['properties']['abn']] = item
            except:
                not_exit += 1
                print(data['properties']['gnaf_pid'])
                continue

        print(not_exit, ' out of ', total)
        json_str = json.dumps(processed_data)

        fhdle = open(target_fname, 'w')
        fhdle.write(json_str)
        fhdle.flush()
        fhdle.close()

    @staticmethod
    # Process the obesity data
    def process_obesity_data():
        phn_obesity_collection = dict()

        # Reading Melb Adult Data
        fhdle = open('../Data/Obesity/data9126525194886453832_A.json')

        adult_data = json.load(fhdle)

        for phn in adult_data['features']:

            single_data = phn_obesity_collection.setdefault(phn['properties']['pha_code'], {})
            single_data['pha_name'] = phn['properties']['pha_name']

            try:
                single_data['female_adult'] = phn['properties']['est_f_18yrs_+_obese_2014_15_asr_100'] + phn['properties']['est_f_18yrs_+_ovrwht_2014_15_asr_100']
            except:
                single_data['female_adult'] = 0
            try:
                single_data['male_adult'] = phn['properties']['est_m_18yrs_+_obese_2014_15_asr_100'] + phn['properties']['est_m_18yrs_+_ovrwht_2014_15_asr_100']
            except:
                single_data['male_adult'] = 0
            try:
                single_data['adult'] = phn['properties']['est_ppl_18yrs_+_obese_2014_15_asr_100'] + phn['properties']['est_ppl_18yrs_+_ovrwht_2014_15_asr_100']
            except:
                single_data['adult'] = 0

        del adult_data

        # Reading Melb Child Data
        fhdle = open('../Data/Obesity/data1086268680170386009_C.json')

        child_data = json.load(fhdle)
        for phn in child_data['features']:
            single_data = phn_obesity_collection.setdefault(phn['properties']['pha_code'], {})
            single_data['pha_name'] = phn['properties']['pha_name']
            try:
                single_data['female_child'] = phn['properties']['est_f_2_17_yrs_obese_2014_15_asr_100'] + phn['properties']['est_f_2_17_yrs_ovrwht_2014_15_asr_100']
            except:
                single_data['female_child'] = 0
            try:
                single_data['male_child'] = phn['properties']['est_m_2_17_yrs_obese_2014_15_asr_100'] + phn['properties']['est_m_2_17_yrs_ovrwht_2014_15_asr_100']
            except:
                single_data['male_child'] = 0
            try:
                single_data['child'] = phn['properties']['est_chld_2_17_yrs_obese_2014_15_asr_100'] + phn['properties']['est_chld_2_17_yrs_ovrwht_2014_15_asr_100']
            except:
                single_data['child'] = 0

        del child_data

        fhdle = open('../ProcessedData/phn_result.json', 'w')
        fhdle.write(json.dumps(phn_obesity_collection))


    @staticmethod
    # Process the PHA geographical data
    def process_pha_geo(fname='../Data/SA2_GEO/data77917273352417469.json',
                        target_fname='../ProcessedData/PHA_GEO.json'):
        raw_data = json.load(open(fname))['features']
        geo_data = dict()
        for item in raw_data:
            geo = dict()
            pha_code = item['properties']['pha_code']
            geo['pha_name'] = item['properties']['pha_name']
            geo['coor'] = item['geometry']['coordinates'][0][0]
            geo_data[pha_code] = geo
        fhdle = open(target_fname, 'w')
        fhdle.write(json.dumps(geo_data))
        fhdle.flush()
        fhdle.close()

    @staticmethod
    # Return the mapping between SA2 and PHA
    def extract_sa2_pha():
        mapping_data = pd.read_excel('../Data/SA2-PHA/sa2_to_pha_concordance_2016_and_2011.xls', header=None,
                                     sheet_name='2016 SA2 to PHA concordance',
                                     usecols='A,C', skiprows=1, skipfooter=0)

        sa2_phn = dict()
        for row in mapping_data.iterrows():
            value = row[1].values
            sa2_phn[int(value[0])] = value[1]

        return sa2_phn





if __name__ == '__main__':
    # DataProcessor.get_mb_pha_mapper()
    # DataProcessor.process_meshblock()
    # DataProcessor.process_family_income()
    # DataProcessor.process_abr(fname='../Data/ABR/data4205622644226925080.json', target_fname='abr_V1.json')
    DataProcessor.process_abr()
    # DataProcessor.process_obesity_data()
    # DataProcessor.process_pha_geo()
    # DataProcessor.get_mb_pha_mapper()


