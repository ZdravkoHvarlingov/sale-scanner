class Utils:

    @staticmethod
    def month_to_number(month_str):
        month_dict = {
            'януари': 1,
            'февруари': 2,
            'март': 3,
            'април': 4,
            'май': 5,
            'юни': 6,
            'юли': 7,
            'август': 8,
            'септември': 9,
            'октомври': 10,
            'ноември': 11,
            'декември': 12
        }

        return month_dict.get(month_str)
