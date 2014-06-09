def inferWidthBasedOnType(cell):
    return len('%r' % cell)

def printToWidth(cell, width):
    if isinstance(cell, int):
        return str('%' + str(width) + 'd') % cell
    else:
        return ('%-' + str(width) + 's') % cell
# print as table.
def printAsTable(headerRow, bodyRows, separator=''):
    columnWidths = [0] * len(headerRow)
    # First pass, compute widths

    for row in [headerRow] + bodyRows:
        for i, cell in enumerate(row):
            width = inferWidthBasedOnType(cell)
            if width > columnWidths[i]:
                columnWidths[i] = width

    # Second pass, actually print the values.
    for row in [headerRow] + bodyRows:
        for i, cell in enumerate(row):
            cellData = printToWidth(cell, columnWidths[i])
            print cellData,
            if separator: print separator,
        print
        
if __name__ == '__main__':
    printAsTable(['syam', 13983], [[10, 13]], '|')
