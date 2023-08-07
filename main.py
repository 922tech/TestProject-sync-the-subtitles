from modules import DialogFactory

if __name__ == '__main__':
  print('working...')
  
  de_dialogs = DialogFactory('de_70105212.vtt')
  en_dialogs = DialogFactory('en_70105212.vtt')

  dic = {(de_dialogs.dialogs[i],):[] for i in range(len(de_dialogs.dialogs))}

  for i in dic:
    for e in en_dialogs.dialogs:
      if  i[0].start <= e.start < i[0].end:
        dic.get(i).append(e.to_dict()['text'])
      elif i[0].start < e.start:
        break 

  final_edit =  [
      {
        'de':i[0].to_dict()['text'],
        'en':dic[i][0],
        'start':i[0].to_dict()['start']
      }
      for i in dic if dic[i]
      ]

  pd.DataFrame(final_edit).to_csv('final_edit.csv')