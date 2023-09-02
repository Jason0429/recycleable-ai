import pandas as pd
from sqlalchemy import create_engine
from difflib import SequenceMatcher
from flask_restful import Resource
from flask import request
import xlrd


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# read by default 1st sheet of an excel file

class RecycleInstructionResource(Resource): 
    def get(self):
        """
        Returns the instructions for recycling an item given the item

        Ex query:
        {root_url}/api/recycle-instruction?item=acids

        Ex response:
        {
            "item": "ACIDS",
            "category": "Hazardous Waste",
            "instruction": "There is no curbside collection for this hazardous waste item. This is a hazardous waste item. The City of Boston hosts 5 Hazardous Waste drop-off days each year."
        }
        """
        item = request.args["item"]
        item = item.lower()
        max = 0
        matched_item = None
        default_query = {"item": item, "category": "Regular trash", "instruction": "Throw away"}
        filename = 'src/services/recycle_instruction/recyclingDatabase.xls'
        workbook = xlrd.open_workbook(filename)
        worksheet = workbook.sheet_by_index(0)
        rows = worksheet.nrows
        for row in range(rows):
            similarity = similar(worksheet.cell(row, 0).value.lower(), item)
            if similarity > max:
                max = similarity
                matched_item = worksheet.row(row)
        if not matched_item:
            return default_query
        return {"item": matched_item[0].value, "category": matched_item[1].value, "instruction": matched_item[2].value}