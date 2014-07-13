import md
import os
import json
from datetime import datetime

class GeneratedRainbowCoder(object):
  post_dir = './post'

  def __init__(self):
    handle = open('cfg.json', 'r')
    self.cfg = json.loads(handle.read())
    handle.close()

  def _get_head_md(self):
    handle = open(self.cfg['head_md'], 'r')
    data = handle.read()
    handle.close()
    return data.decode('UTF-8')

  def _get_css(self):
    css = self.cfg['css']
    return '<link rel="stylesheet" type="text/css" href="%s">' % (css)

  def _get_filename(self, path):
    base = os.path.basename(path)
    return os.path.splitext(base)[0]

  def _get_file(self, file):
    handle = open(file, 'r')
    data = handle.read()
    handle.close()
    return data.decode('UTF-8')

  def _save_file(self, file, str):
    handle = open(file, 'w')
    handle.write(str.encode('UTF-8'))
    handle.close()

  def _get_title(self, title):
    if title:
      return "<title>"+title+"</title>"
    return ""

  def _get_html_filename(self, md_file):
    title = self._get_filename(md_file)
    return "html/" + title + ".html"


  def get_html(self, md_file):
    title = self._get_filename(md_file)
    conv = md.MarkDownConvert(self._get_file(md_file))

    html =  u'<!DOCTYPE html>'
    html += '<html><head><meta charset="utf-8">'
    html += self._get_css()
    html += self._get_title(title)
    html += "</head><body>"
    html += conv.md2html().decode('UTF-8')
    html += "</body>"
    html += "</html>"
    return html

  def gen_post(self, md_file):
    print "building: " + md_file
    html = self.get_html(md_file)
    html_file = self._get_html_filename(md_file)
    self._save_file(html_file, html)
    return html_file

  def get_post_list(self):
    ret = []
    list_post = os.listdir(self.post_dir)
    for line in list_post:
      md_file = os.path.join(self.post_dir, line)
      if os.path.isfile(md_file):
        title = self._get_filename(md_file)
        if title != 'index':
          ret.append({
              'title': title,
              'md_file': md_file,
              'html_file': title + ".html",
              'create_date': os.path.getctime(md_file),
            })

    ret.sort(key=lambda item: item['create_date'], reverse = True)
    return ret

  def _format(self, title, html, date):
    # date = datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
    return '[%s](%s)\n' % (title, html)

  def building_index_md(self):
    post_list = self.get_post_list()
    head = self._get_head_md() + '\n\n\n'
    for v in post_list:
      head += self._format(v['title'], v['html_file'], v['create_date'])
    
    index_md = self.cfg['index_md']
    self._save_file(index_md, head)
    self.gen_post(index_md)

  def building_all(self):
    post_list = self.get_post_list()
    self.building_index_md()
    for v in post_list:
      self.gen_post(v['md_file'])



rainbow = GeneratedRainbowCoder()
rainbow.building_all()




