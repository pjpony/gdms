#! /usr/bin/env python

from time import sleep
import datetime
import win32com.client as win32


def fromrow():
    app = 'Excel'
    xl = win32.gencache.EnsureDispatch('%s.Application' % app)
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    # wb = excel.Workbooks.Add()
    wb = excel.Workbooks.Open(r'c:\web2py\ProjectCharterWorkbookv5.xlsx')
    ws = wb.Worksheets("Template")
    xl.Visible = True
    sleep(1)

    # so lets change to get one record at a time - however maybe transferring the whole list
    # is better and then we just slice the big list into rows
    myplan = ws.Range("Plan")
    startrow = myplan.Rows(1).Row
    startcolumn = myplan.Columns(1).Column

    # So we will have a list of tuples which will allow rows to map to corresponding value
    # in a dictionary when we retrieve corresponding values from row to write back then
    # for writing back we just write in the order
    SourceColumns = [('w2pid', 'id'), ('Level', 'None'), ('Number', 'None'), ('Classification', 'None'),
                     ('Start', 'Startdate'), ('EndDate', 'Enddate'), ('Description', 'questiontext'),
                     ('Owner', 'Responsible'), ('Status', 'Execstatus'), ('Actstart', 'None'), ('Actend', 'None'),
                     ('Dependency', 'None'), ('Notes', 'Notes')]

    #below is repeated as possible status not currently the same but may need to be
    SourceColumns = [('w2pid', 'id'), ('Level', 'None'), ('Number', 'None'), ('Classification', 'None'),
                     ('Start', 'startdate'), ('EndDate', 'enddate'), ('Description', 'questiontext'),
                     ('Owner', 'responsible'), ('Status', 'None'), ('Actstart', 'None'), ('Actend', 'None'),
                     ('Dependency', 'None'), ('Notes', 'notes'), ('Percomplete', 'perccomplete') ]

    rowlength = len(SourceColumns)
    numrows = len(myplan) / rowlength
    groupid = None

    myrow = []
    rowcounter = 0
    for i, x in enumerate(myplan):
        myrow.append(x.Value)
        if (i + 1) % rowlength == 0:
            rowdict = dict()
            for i, y in enumerate(myrow):
                if SourceColumns[i][1] != 'None':
                    rowdict[SourceColumns[i][1]] = y
            #if rowdict['startdate'] <= 0 or rowdict['enddate'] <= 0:
            #    myrow = []
            #    rowcounter += 1
            #    continue
            rowdict['qtype'] = 'action'
            rowdict['status'] = 'Agreed'
            if rowdict['startdate'] > 0:
                rowdict['startdate'] = datetime.datetime.fromtimestamp(int(rowdict['startdate']))
            else:
                rowdict['startdate'] = None
            if rowdict['enddate'] > 0:    
                rowdict['enddate'] = datetime.datetime.fromtimestamp(int(rowdict['enddate']))
            else:
                rowdict['enddate'] = None
            rowdict['actiongroup'] = groupid

            selectedrows = None
            if myrow[1] == 1: # header row
                if rowdict['id'] is not None:
                    selectedrows = db(db.actiongroup.id == rowdict['id']).select()
                if selectedrows:
                    selectedrow = selectedrows.first()
                    selectedrow.update_record(grouptext=rowdict['questiontext'], startdate=rowdict['startdate'],
                                              enddate=rowdict['enddate'])
                    groupid = rowdict['id']
                else:
                    # does the id matter here - lets remove anyway before doing insert
                    del rowdict['id']
                    groupid = db.actiongroup.insert(grouptext=rowdict['questiontext'], startdate=rowdict['startdate'],
                                              enddate=rowdict['enddate'])
                    ws.Cells(startrow + rowcounter, startcolumn).Value = groupid
            else: #insert normal item
                if rowdict['id'] is not None:
                    selectedrows = db(db.question.id == rowdict['id']).select()
                if selectedrows:
                    selectedrow = selectedrows.first()
                    selectedrow.update_record(**rowdict)
                else:
                    if rowdict['questiontext'] is not None:
                        del rowdict['id']
                        newid = db.question.insert(**rowdict)
                        ws.Cells(startrow + rowcounter, startcolumn).Value = newid
            myrow = []
            rowcounter += 1

    wb.Save()
    excel.Application.Quit()
    return locals()

def export():
    # so this is opposite of import and plan would be to update matching excel rows with changes to dates, actions
    # text and responsibility
    app = 'Excel'
    xl = win32.gencache.EnsureDispatch('%s.Application' % app)
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(r'c:\web2py\applications\gdms\private\ProjectMappingTest1.xlsx')
    ws = wb.Worksheets("Sheet2")
    xl.Visible = True
    sleep(1)

    # so lets change to get one record at a time - however maybe transferring the whole list
    # is better and then we just slice the big list into rows
    myplan = ws.Range("Plan")
    startrow = myplan.Rows(1).Row
    startcolumn = myplan.Columns(1).Column

    # So we will have a list of tuples which will allow rows to map to corresponding value
    # in a dictionary when we retrieve corresponding values from row to write back then
    # for writing back we just write in the order
    SourceColumns = [('w2pid', 'id'), ('Level', 'None'), ('Number', 'None'), ('Classification', 'None'),
                     ('Start', 'Startdate'), ('EndDate', 'Enddate'), ('Description', 'questiontext'),
                     ('Owner', 'Responsible'), ('Status', 'Execstatus'), ('Actstart', 'None'), ('Actend', 'None'),
                     ('Dependency', 'None'), ('Notes', 'Notes')]

    SourceColumns = [('w2pid', 'id'), ('Level', 'None'), ('Number', 'None'), ('Classification', 'None'),
                     ('Start', 'startdate'), ('EndDate', 'enddate'), ('Description', 'questiontext'),
                     ('Owner', 'responsible'), ('Status', 'None'), ('Actstart', 'None'), ('Actend', 'None'),
                     ('Dependency', 'None'), ('Notes', 'notes')]

    rowlength = len(SourceColumns)
    numrows = len(myplan) / rowlength

    myrows = []
    myrow = []
    for i, x in enumerate(myplan):
        myrow.append(x.Value)
        if (i + 1) % rowlength == 0:
            myrows.append(myrow)
            myrow = []

    for rowcounter, x in enumerate(myrows):
        rowdict = dict()
        for i, y in enumerate(x):
            if SourceColumns[i][1] != 'None':
                rowdict[SourceColumns[i][1]] = y
        rowdict['startdate'] = datetime.datetime.fromtimestamp (int(rowdict['startdate']))
        rowdict['enddate'] = datetime.datetime.fromtimestamp(int(rowdict['enddate']))

        selectedrows = None
        if rowdict['id'] is not None:
            selectedrows = db(db.question.id == rowdict['id']).select()
        if selectedrows:
                selectedrow=selectedrows.first()
                # but maybe go with one way link for now
                # now we just compare the values and update any that have changed - we never right back if no
                # matching records possibly this could be a standard for everythig in the dict but dates will be a
                # problem - so do longhand for now??

    wb.Save()
    excel.Application.Quit()
    return locals()