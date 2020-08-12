import csv
from pb import db, session
from pb.models import Sponsor


class ExampleDataLoader:
    @staticmethod
    def clean_db():
        session.flush()  # Clear out any transactions before deleting it all to avoid spurious errors.
        for table in reversed(db.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
        session.flush()

    def load_all(self):
        self.load_sponsors()
        # self.load_studies()
        # self.load_investigators()

    def load_sponsors(self):
        # Load sponsors from csv
        with open('./pb/static/csv/sponsors.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            first_line = True
            sponsors = []
            for row in data:
                # Skip first line, which will be the column headings
                if first_line:
                    # row[0]: SPONSOR_ID
                    # row[1]: SP_NAME
                    # row[2]: SP_MAILING_ADDRESS
                    # row[3]: SP_TYPE
                    first_line = False
                elif int(row[0] or -1) is not -1:
                    print('row', row)
                    new_sponsor = Sponsor(SPONSOR_ID=int(row[0]), SP_NAME=row[1], SP_MAILING_ADDRESS=row[2], SP_TYPE=row[3])
                    new_sponsor.SP_TYPE_GROUP_NAME = Sponsor.get_type_group_name(new_sponsor.SP_TYPE)
                    sponsors.append(new_sponsor)

            session.add_all(sponsors)
            session.commit()




