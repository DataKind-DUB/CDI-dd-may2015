def parse_cdi_csv(csvfile):
    '''
      Returns pandas frame where 
      * Age, Prison_History, Schooling are converted to numerical ranks
      * family_in_prison sums the ranks of sibling/parent in prison
      * children - binary 0/1 (has children or doesn't)
    '''
    col_names = ['Wing',
             'Participant',
             'Gender',
             'Age',
             'Schooling',
             'Prison_History',
             'Parent_in_prison',
             'Sibling_in_prison',
             'Children',
             'Partner',
             'Married',
             'Child_age',
             'Child_gender',
             'Child_visit',
             'Child_home',
             'How_satisfied_visit',
             'How_satisfied_contact',
             'Feeling_about_visits',
             'Other_thoughts',
             'Suggestions_for_improvement',
             'Date_Completed',
             'Questionnaire_helper']

    col_idx = {c:i for (i,c) in enumerate(col_names)}

    # conversion dicts
    dage = defaultdict(int)
    drecur = defaultdict(int)
    dschool = defaultdict(int)
    dyesno = defaultdict(int)
    
    dage.update({'18-25': (18+25)/2,
            '26-35': (26+35)/2,
            '36-50': (36+50)/2,
            '51+': 51})
    
    drecur.update({'I\'ve been in prison 5 times or more': 5,
       'This is my first time in prison': 1,
       'I\'ve been to prison 2-5 times': 2.5
    })
    
    dschool.update({"I didn’t go to secondary school": 1,
       "I left school after Junio/Inter Cert": 2,
       "I left after Leaving Cert": 3,
       "I have gone to College/University": 4}
    )
    
    dyesno.update({'Yes': 1, 'No': 0})
    
    c = csv.reader(open(csvfile))
    # first row is col
    c.next()
    out = []
    uniqueids = set([])
    
    for row in c:
        if row[col_idx['Participant']] in uniqueids:
            continue
        
        uniqueids.update([row[col_idx['Participant']]])
        txt_age = row[col_idx['Age']]
        row[col_idx['Age']] = dage[txt_age]
        
        rec_txt = row[col_idx['Prison_History']]
        row[col_idx['Prison_History']] = drecur[rec_txt]
        
        school_txt = row[col_idx['Schooling']]
        row[col_idx['Schooling']] = dschool[school_txt]

        # for these questions we assume "No" is the default
        pin_txt = row[col_idx['Parent_in_prison']]
        if pin_txt == '': pin_txt = 'No'
        row[col_idx['Parent_in_prison']] = dyesno[pin_txt]
        
        pin_txt = row[col_idx['Sibling_in_prison']]
        if pin_txt == '': pin_txt = 'No'
        row[col_idx['Sibling_in_prison']] = dyesno[pin_txt]

        pin_txt = row[col_idx['Children']]
        if pin_txt == '': pin_txt = 'No'
        row[col_idx['Children']] = dyesno[pin_txt]

        pin_txt = row[col_idx['Partner']]
        if pin_txt == '': pin_txt = 'No'
        row[col_idx['Partner']] = dyesno[pin_txt]

        out.append(row)

    p =  pd.DataFrame(out, columns=col_names)
    p['Family_in_prison'] = p['Parent_in_prison'] + p['Sibling_in_prison']
    return p
