import fixpath
fixpath.FixPath()
import prettytable

# print as table.
def printAsTable(headerRow, bodyRows):
    formatter = prettytable.PrettyTable(headerRow)
    for h in headerRow: formatter.align[h] = 'r'
    for row in bodyRows: formatter.add_row(row)
    
    print formatter
        
if __name__ == '__main__':
    printAsTable(['syam', '13983'], [[10, 13], [10000, 784789789]])
