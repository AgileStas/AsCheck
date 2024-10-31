from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import UpdateView

import io
import json
import os
import random
import re
import sys
import zipfile

from datetime import datetime

#from .models import UsbStor
from .models import Host
from .forms import HostForm

def index(request):
    html_resp = """<html>
    <body>
        <dl>
            <dt><a href="usbstor/">UsbStor</a></dt>
            <dd>Зареєстровані зовнішні носії інформації</dd>
            <dt><a href="host/">Host</a></dt>
            <dd>Обліковані АС, АРМ, ПЕОМ</dd>
            <dt><a href="host/upload">Upload host check data</a></dt>
            <dd>Завантажити дані перевірки АС, АРМ, ПЕОМ</dd>
            <dt><a href="/static/AsCheck.ps1">Windows AS data collector</a></dt>
            <dd>Скрипт збирання інформації АС, АРМ, ПЕОМ</dd>
        </dl>
    </body>
</html>
"""
    return HttpResponse(html_resp)

def enum_usb_to_json(hizip: zipfile.ZipFile, filename: str) -> str:
    filedata = hizip.read(filename)
    eu_io = io.StringIO(filedata.decode('utf-16'))

    lines = eu_io.readlines()
    curitem = {}
    items = []
    for line in lines:
        if '--- Item-Break ---' == line.strip():
            if curitem:
                items.append(curitem)
                curitem = {}
        elif not line.strip():
            continue
        elif ':' not in line:
            # TODO throw error?
            print('--- Unable to parse line, skipping: "' + line + '"', file=sys.stderr)
            continue
        else:
            kvlist = line.split(':', 1)
            if len(kvlist) != 2:
                # TODO throw error?
                print('--- Unable to parse line to KV pair, skipping: "' + line + '"', file=sys.stderr)
                continue
            curitem[kvlist[0].strip()] = kvlist[1].strip()

    return json.dumps(items)

def kv_info_from_zip(hizip: zipfile.ZipFile, filename: str) -> dict[str, str]:
    kv_data = {}
    csi_bytes = hizip.read(filename)
    csi_io = io.StringIO(csi_bytes.decode('utf-16'))
    lines = csi_io.readlines()
    for line in lines:
        # print(line)
        found = re.search(r"([^:]+)\s*:\s*(.*)$", line)
        # found = re.search(r"(.+):(.*)", line)
        # print(found)
        if found:
            csi_key = found.group(1).strip()
            csi_value = found.group(2).strip()
            kv_data[csi_key] = csi_value
    return kv_data

def host_info_form(request):
    '''Get computer system information as ZIP file, try to match existing host record, store updated host information'''
    # TODO skip storage to file system, handle chunked upload
    if request.method == 'POST' and request.FILES['uploaded_file']:
        uploaded_file = request.FILES['uploaded_file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        # filename = fs.url(filename)

        if not zipfile.is_zipfile(filename):
            return HttpResponseBadRequest()

        # check zipwalk https://stackoverflow.com/questions/66181180/perform-an-os-walk-through-a-zip-compressed-file-using-the-zipfile-module
        #    for zinfo in hizip.infolist():
        #        ....
        # ziplist = ''
        csi_data = {}
        avi_data = {}
        eset_data = {}
        wai_data = {}
        usb_json: str
        hostname = ''
        with zipfile.ZipFile(filename) as hizip:
            ziplist = hizip.namelist()
            if not ziplist:
                return HttpResponseBadRequest()
            hostdir = ziplist[0]
            if not hostdir.endswith('/'):
                return HttpResponseBadRequest()
            e = hizip.infolist()
            check_date = e[0].date_time
            hostname = hostdir.rstrip('/')
            for zipentry in ziplist:
                if zipentry.endswith('/ComputerInfo.txt'):
                    csi_data = kv_info_from_zip(hizip, zipentry)
                elif zipentry.endswith('/AntivirusProductInfo.txt'):
                    avi_data = kv_info_from_zip(hizip, zipentry)
                elif zipentry.endswith('/EsetInfo.txt'):
                    eset_data = kv_info_from_zip(hizip, zipentry)
                elif zipentry.endswith('/WindowsActivationInfo.txt'):
                    wai_data = kv_info_from_zip(hizip, zipentry)
                elif zipentry.endswith('/EnumUsb.txt'):
                    usb_json = enum_usb_to_json(hizip, zipentry)

        fs.delete(filename)

        csdict = {}
        csdict['hostname'] = hostname
        csdict['serialnumber'] = csi_data['BiosSeralNumber']
        csdict['manufacturer'] = csi_data['CsManufacturer']
        csdict['model'] = csi_data['CsModel']
        csdict['systemfamily'] = csi_data['CsSystemFamily']
        csdict['check_date'] = datetime(*check_date).isoformat()
        csdict['cs_json'] = json.dumps(csi_data)
        csdict['av_json'] = json.dumps(avi_data)
        csdict['wa_json'] = json.dumps(wai_data)
        csdict['eset_json'] = json.dumps(eset_data)
        csdict['usb_json'] = usb_json
        cssiid = 'csentry%s' % random.randint(0, 999999)
        # request.session[session_key] = csentry
        request.session[cssiid] = csdict
        return redirect('hostInfoUpdate', cssiid)
        # return redirect('hostInfoUpdate')
        # return redirect('host/update')

        # filename = usb_json
        # filename = ziplist
        # filename = json.dumps(csi_data)
        # filename = json.dumps(list(csentry))
        return render(request, os.path.join('checks','host_info_form.html'), {
             'filename': filename
        })
    else:
        return render(request, os.path.join('checks','host_info_form.html'), {})

"""
        csentries = Host.objects.filter(hostname=hostname)

        create_record = False
        update_record = False
        if not csentries:
            filename = "Computer system with '" + hostname + "' name does not exist"
            create_record = True
        elif len(csentries) == 1:
            filename = "Serial number for computer system '" + hostname + "' is '" + csentries[0].serialnumber + "'"
            update_record = True
        else:
            filename = "Multiple computer systems found for name '" + hostname + "'!"

        # ---
        csentry: Host = None
        if create_record:
            csentry = Host(hostname=hostname)
            # csentry.save()
        if update_record:
            csentry = csentries[0]
            # csentry.hostname = hostname
        if create_record or update_record:
            # Parsed entry:
            pe_serialnumber = csi_data['BiosSeralNumber']
            pe_manufacturer = csi_data['CsManufacturer']
            pe_model = csi_data['CsModel']
            pe_systemfamily = csi_data['CsSystemFamily']
            check_date_dt = datetime(*check_date)
            csentry.serialnumber = pe_serialnumber
            csentry.cs_manufacturer = pe_manufacturer
            csentry.cs_model = pe_model
            csentry.cs_systemfamily = pe_systemfamily
            csentry.cs_json = json.dumps(csi_data)
            csentry.av_json = json.dumps(avi_data)
            csentry.wa_json = json.dumps(wai_data)
            csentry.eset_json = json.dumps(eset_data)
            csentry.usb_json = usb_json
            csentry.check_date = check_date_dt.isoformat()
            # csentry.save()
"""

from django.http import Http404
def host_update_info_form(request, cssiid=None):
    csdict: dict
    if not cssiid:
        raise Http404
    csdict = request.session.get(cssiid)
    if not csdict:
        raise Http404

    csitems = {}
    csentries = Host.objects.filter(hostname=csdict['hostname'])
    for i in csentries:
        it = {}
        it['id'] = i.id
        it['hostname'] = i.hostname
        it['serialnumber'] = i.serialnumber
        csitems[i.id] = it
    csentries = Host.objects.filter(serialnumber=csdict['serialnumber'])
    for i in csentries:
        it = {}
        it['id'] = i.id
        it['hostname'] = i.hostname
        it['serialnumber'] = i.serialnumber
        csitems[i.id] = it

    csdict['csitems'] = csitems.values()

    csdict['httpmethod'] = request.method

    if request.method == 'POST':
        print(request.POST)
        cs_id = int(request.POST['cs_id'])
        if not cs_id:
            del request.session[cssiid]
            return redirect('hostInfoUpload')

        csentry: Host = None
        if cs_id == -1:
            csentry = Host(hostname=csdict['hostname'])
            # csentry.save()
        elif cs_id > 0:
            # TODO check if id is in the list of correct ids
            csentry = Host.objects.get(pk=cs_id)

        if not csentry:
            raise Http404

        # Entry data from session storage:
        csentry.hostname = csdict['hostname']
        csentry.serialnumber = csdict['serialnumber']
        csentry.cs_manufacturer = csdict['manufacturer']
        csentry.cs_model = csdict['model']
        csentry.cs_systemfamily = csdict['systemfamily']
        csentry.check_date = csdict['check_date']
        csentry.cs_json = csdict['cs_json']
        csentry.av_json = csdict['av_json']
        csentry.wa_json = csdict['wa_json']
        csentry.eset_json = csdict['eset_json']
        csentry.usb_json = csdict['usb_json']
        csentry.save()
        del request.session[cssiid]
        return redirect('hosts')

    return render(request, os.path.join('checks','host_update_info_form.html'), {
        'csdict': csdict
    })

class HostUpdateView(UpdateView):
    model = Host
    form_class = HostForm
    template_name_suffix = "_update_form"
    success_url = '.'

#class UsbStorView(ListView):
#    model = UsbStor