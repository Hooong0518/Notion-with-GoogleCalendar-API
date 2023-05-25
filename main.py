import quickstart
import notion
# 同步notion資料至Google Calendar
def Notion_to_Calendar():
  """新增事件"""
  insert_data = notion.query_insertData()
  if len(insert_data)!=0:
    for page in insert_data:
      # 事件類別判斷
      type = page['properties']['優先程度']['select']['name']
      if type == '行程':
          calendar_id = '93fe8cf9a4bda21779837f0b32f70ecef2ad9551c784115c1772fedee4724518@group.calendar.google.com'
      elif type in ['第一優先', '第二優先', '第三優先', '第四優先']:
          calendar_id = '2cb91bb33983e220e7afb002e54731897f43342c561f3b329e0e1d9f121b21f3@group.calendar.google.com'
      elif type == '日常':
          calendar_id = '62b17855bfd46c4e90772622769afe0cc50b5dfb5fe9a946ee35c803be234822@group.calendar.google.com'
      else:
          calendar_id = '0b98e349d86319bb42465ef08f92855c536c1365ea714b206854914f8cec2c2d@group.calendar.google.com'
      # 備註欄
      if len(page['properties']['備註']['rich_text'])!=0:
        description = page['properties']['備註']['rich_text'][0]['plain_text']
      else:
        description = ''
      # 事件無結束時間
      if page['properties']['實行時間']['date']['end']==None:
        event = {
          'summary': page['properties']['行動項目']['title'][0]['plain_text'],
          'description': description,
          'start': {
            'date': page['properties']['實行時間']['date']['start'],
            'timeZone': 'Asia/Taipei',
          },
          'end': {
            'date': page['properties']['實行時間']['date']['start'],
            'timeZone': 'Asia/Taipei',
          },
          'reminders': {
            'useDefault': False,
          },
        }
      # 事件有結束時間
      else:
        event = {
          'summary': page['properties']['行動項目']['title'][0]['plain_text'],
          'description': description,
          'start': {
            'dateTime': page['properties']['實行時間']['date']['start'],
            'timeZone': 'Asia/Taipei',
          },
          'end': {
            'dateTime': page['properties']['實行時間']['date']['end'],
            'timeZone': 'Asia/Taipei',
          },
          'reminders': {
            'useDefault': False,
          },
        }
      # 建立
      pageId = page['id']
      calendarID = quickstart.new_event(calendar_id, event)
      properties = {
          "calendarID": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": calendarID
                    }
                }
            ]
        },
      }
      notion.update_page(pageId, properties)
      #回傳
      event_name = event['summary']
      print('Event Created: %s' % event_name)
    print('Event Create Finish')
  else:
    print('No Event To Create')
  
  """更新事件"""
  update_data = notion.query_updateData()
  if len(update_data)!=0:
    for page in update_data:
      # 事件類別判斷
      type = page['properties']['優先程度']['select']['name']
      if type == '行程':
          calendar_id = '93fe8cf9a4bda21779837f0b32f70ecef2ad9551c784115c1772fedee4724518@group.calendar.google.com'
      elif type in ['第一優先', '第二優先', '第三優先', '第四優先']:
          calendar_id = '2cb91bb33983e220e7afb002e54731897f43342c561f3b329e0e1d9f121b21f3@group.calendar.google.com'
      elif type == '日常':
          calendar_id = '62b17855bfd46c4e90772622769afe0cc50b5dfb5fe9a946ee35c803be234822@group.calendar.google.com'
      else:
          calendar_id = '0b98e349d86319bb42465ef08f92855c536c1365ea714b206854914f8cec2c2d@group.calendar.google.com'
      # 備註處理
      if len(page['properties']['備註']['rich_text'])!=0:
        description = page['properties']['備註']['rich_text'][0]['plain_text']
      else:
        description = ''
      if page['properties']['實行時間']['date']['end']==None:
        event = {
          'summary': page['properties']['行動項目']['title'][0]['plain_text'],
          'description': description,
          'start': {
            'date': page['properties']['實行時間']['date']['start'],
            'timeZone': 'Asia/Taipei',
          },
          'end': {
            'date': page['properties']['實行時間']['date']['start'],
            'timeZone': 'Asia/Taipei',
          },
          'reminders': {
            'useDefault': False,
          },
        }
      else:
        event = {
          'summary': page['properties']['行動項目']['title'][0]['plain_text'],
          'description': description,
          'start': {
            'dateTime': page['properties']['實行時間']['date']['start'],
            'timeZone': 'Asia/Taipei',
          },
          'end': {
            'dateTime': page['properties']['實行時間']['date']['end'],
            'timeZone': 'Asia/Taipei',
          },
          'reminders': {
            'useDefault': False,
          },
        }
      eventId = page['properties']['calendarID']['rich_text'][0]['plain_text']
      quickstart.update_event(calendar_id, eventId, event)
      #回傳
      event_name = event['summary']
      print('Event Updated: %s' % event_name)
    print('Event Update Finish')
  else:
    print('No Event To Update')
  
  """刪除事件"""
  delete_data = notion.query_deleteData()
  calandar_list = ['93fe8cf9a4bda21779837f0b32f70ecef2ad9551c784115c1772fedee4724518@group.calendar.google.com',
                  '2cb91bb33983e220e7afb002e54731897f43342c561f3b329e0e1d9f121b21f3@group.calendar.google.com',
                  '62b17855bfd46c4e90772622769afe0cc50b5dfb5fe9a946ee35c803be234822@group.calendar.google.com',
                  '0b98e349d86319bb42465ef08f92855c536c1365ea714b206854914f8cec2c2d@group.calendar.google.com']
  page_list = {}
  for page in delete_data:
    type = page['properties']['優先程度']['select']['name']
    if type == '行程':
      calendar_id = '93fe8cf9a4bda21779837f0b32f70ecef2ad9551c784115c1772fedee4724518@group.calendar.google.com'
    elif type in ['第一優先', '第二優先', '第三優先', '第四優先']:
      calendar_id = '2cb91bb33983e220e7afb002e54731897f43342c561f3b329e0e1d9f121b21f3@group.calendar.google.com'
    elif type == '日常':
      calendar_id = '62b17855bfd46c4e90772622769afe0cc50b5dfb5fe9a946ee35c803be234822@group.calendar.google.com'
    else:
      calendar_id = '0b98e349d86319bb42465ef08f92855c536c1365ea714b206854914f8cec2c2d@group.calendar.google.com'
    id = page['properties']['calendarID']['rich_text'][0]['plain_text']
    page_list[id] = calendar_id

  for calandar_id in calandar_list:
    event_list = quickstart.get_event_list(calandar_id)
    if len(event_list)!=0:
      for event_id in event_list:
        if event_id not in list(page_list.keys()):
          event_name = quickstart.get_event(calandar_id, event_id)['summary']
          quickstart.delete_event(calandar_id, event_id)
          print("Event Delete: %s" % event_name)
  print('Event Deleted Finish')

Notion_to_Calendar()