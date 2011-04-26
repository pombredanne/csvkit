#!/usr/bin/env python

from csvkit import CSVKitReader
from csvkit.cli import parse_column_identifiers

class CSVCutReader(CSVKitReader):
    """
    A CSVKitReader which also cuts data down to specific columns.
    """
    def __init__(self, f, column_ids, header=True, **kwargs):
        super(CSVCutReader, self).__init__(f, **kwargs)
        self.header = header 
        self._header = None 

        self._column_ids = column_ids

        if not header:
            self.columns = parse_column_identifiers(column_ids, None)

    def next(self):
        row = super(CSVCutReader, self).next()

        # If reading the header row, update 
        if self.header and not self._header:
            self._header = row
            self.columns = parse_column_identifiers(self._column_ids, self._header)

        return [row[c] if c < len(row) else None for c in self.columns]

