import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL


from WebApplication.dbCreater import PHA, Obesity, ABR
# from dbCreater import PHA, Obesity, ABR

class DataFetcher:
    def __init__(self):
        configs = {
            'drivername': 'sqlite',
            'database': 'pikachu.db',
        }

        engine = create_engine(URL(**configs), echo=False)
        Session = sessionmaker()
        Session.configure(bind=engine)
        self.session = Session()
        self.child_bound = [20, 30, 40, 100]
        self.adult_bound = [40, 50, 60, 70, 100]
        self.food_bound = [0, 100, 200, 300, 1000]
        self.step = 0.2

    # Return the ABR - Obesity tuple for child and adults
    def get_abr_obesity(self):
        acc_data = {}

        for pha_code, child, adult in self.session.query(Obesity.pha, Obesity.child_obesity, Obesity.adult_obesity):
            acc_data[pha_code] = [[child, adult]]

        for pha in acc_data.keys():
            abr_count = self.session.query(ABR).filter_by(pha_code=pha).count()
            acc_data[pha].append(abr_count)

        adult_data = []
        child_data = []
        for item in acc_data.items():
            child_data.append([item[1][1], round(item[1][0][0], 1)])
            adult_data.append([item[1][1], round(item[1][0][1], 1)])

        return child_data, adult_data

    # Return the information on the top 10 areas with highest obesity
    def get_obesity(self, num=10):
        acc_data = []

        for pha_code, child, adult in self.session.query(Obesity.pha, Obesity.child_obesity, Obesity.adult_obesity):
            pha_name = self.get_locale_name(pha_code)
            acc_data.append([pha_name, round(child, 1), round(adult, 1)])

        acc_data.sort(key=lambda ele: ele[1]+ele[2], reverse=True)

        return acc_data[:num]

    # Return the information on the top 10 areas with the largest count of restaurants
    def get_abr(self, num=10):
        acc_data = []

        pha_code = [x[0] for x in self.session.query(PHA.pha_code)]
        for pha in pha_code:
            abr_count = self.session.query(ABR).filter_by(pha_code=pha).count()
            pha_name = self.get_locale_name(pha)
            acc_data.append([pha_name, abr_count])

        acc_data.sort(key=lambda ele: ele[1], reverse=True)
        return acc_data[:num]

    # Return a full list of locale code
    def get_locale_list(self):
        return [x[0] for x in self.session.query(PHA.pha_code)]

    # Return information on a location according to the locale code
    def get_locale_summary(self, loc_code, if_obesity=True):

        result = [[x.pha_name, x.coor] for x in self.session.query(PHA).filter_by(pha_code=loc_code)]
        result[0][1] = eval(result[0][1])
        if if_obesity:
            db_obj = self.session.query(Obesity).filter_by(pha=loc_code)[0]
            result[0].append((db_obj.child_obesity + db_obj.adult_obesity)/2.0)
        else:
            abr_count = self.session.query(ABR).filter_by(pha_code=loc_code).count()
            result[0].append(abr_count)

        return result

    # Return the name of the location based on the locale code
    def get_locale_name(self, loc_code):
        return self.session.query(PHA).filter_by(pha_code=loc_code)[0].pha_name

    # Generate the GEO json for the Google Map API
    def generate_obesity_geo_json(self, fname='../Data/SA2_GEO/data77917273352417469.json'):
        json_with_ob = json.load(open(fname))
        data_pool = json_with_ob['features']
        for data in data_pool:

            try:
                property = {}
                db_obj = self.session.query(Obesity).filter_by(pha=data['properties']['pha_code'])[0]
                child_opacity = round(self.calculate_opacity(db_obj.child_obesity, 1), 1)
                print(child_opacity)
                adult_opacity = round(self.calculate_opacity(db_obj.adult_obesity, 3), 1)

                property['color'] = 'red'
                property['child_op'] = str(child_opacity)
                property['adult_op'] = str(adult_opacity)

                name = self.get_locale_name(data['properties']['pha_code'])
                property['name'] = str(name)

                fast_food = self.session.query(ABR).filter_by(pha_code=data['properties']['pha_code']).count()
                property['food_op'] = round(self.calculate_opacity(fast_food, 2),1)
                data['properties'] = property

            except:
                print('not exist in db')
                continue

        result_str = json.dumps(json_with_ob)
        fhdle = open('Web/GEO.json', 'w')
        fhdle.write(result_str)
        fhdle.flush()
        fhdle.close()

    # Calculate opacity based on the input number for GEO json
    def calculate_opacity(self, num, op_type=1):
        if op_type == 1:
            bounds = self.child_bound
            print('child', num)
        elif op_type == 2:
            bounds = self.food_bound
        else:
            bounds = self.adult_bound
            print('adult', num)

        for i in range(len(bounds)-1):
            if num >= bounds[i] and num < bounds[i+1]:
                return self.step*(i+1)
        return 0

    # Count the PHA data record for obesity
    def count(self):
        a = self.session.query(Obesity.pha).count()
        return a



# Code Block for Report

## ABR-Obesity Plot ###

# a = DataFetcher()
# child, adults = a.get_abr_obesity()
# x = [i[0] for i in child]
# print(x)
# y = [i[1] for i in child]
#
# import matplotlib.pyplot as plt
# plt.scatter(x, y)
# plt.show()

### Calculate Opacity ###

# a = DataFetcher()
# child = [0, 20, 25, 30, 31, 40, 49]
# adult = [0, 40, 49, 50, 58, 60, 65, 72, 80]
#
# for i in adult:
#     print(a.calculate_opacity(i, False))

# a = DataFetcher()
# print(len(a.get_abr()))
# print(a.get_locale_summary(20012, False))

a = DataFetcher()
a.get_abr()
