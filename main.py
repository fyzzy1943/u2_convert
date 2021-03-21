# -*- coding: utf-8 -*-
import copy
import time

import bencode
import requests

path = './'
api = ''
batch_num = 50
new_base = ''


class Convert:
    def __init__(self):
        self._path = './'
        self._api = ''
        self._batch_num = batch_num

    def fire(self, s_api, s_path):
        self._api = s_api
        self._path = s_path
        self.handle()

    def request(self, req):
        req_info = []
        for i in req:
            req_info.append({"jsonrpc": "2.0", "method": "query", "params": i[1], "id": i[0]})

        sleep_time = 2
        print('ready send request, sleep %fs' % sleep_time)
        time.sleep(sleep_time)

        print(req_info)
        resp = requests.post(self._api, json=req_info)
        print(resp)
        resp = resp.json()
        print('request result: %s' % ''.join(str(resp)))

        res = []
        for resp_item in resp:
            print(resp_item)
            new_tracker = [new_base + resp_item['result']]
            res.append((resp_item['id'], new_tracker))
        return res

    def save(self, data):
        with open(self._path + "resume.dat.1", 'wb') as f:
            f.write(bencode.bencode(data))

    def handle(self):
        print('handle start')
        with open(self._path + "resume.dat", 'rb') as f:
            data = bencode.bdecode(f.read())
            ndata = copy.deepcopy(data)

            req_seq, req, key_map = 1, [], {}
            for key, item in (i for i in data.items() if i[0] != '.fileguard'):
                if str(item['trackers']).find('http://tracker.dmhy.org/') != -1:
                    print('add to req: %s, current tracker is:%s' % (str(item['caption']), str(item['trackers'])))
                    req.append((req_seq, str(item['info'].hex())))
                    key_map[req_seq] = key
                    req_seq = req_seq + 1

                    if len(req) >= self._batch_num:
                        for i in self.request(req):
                            ndata[key_map[i[0]]]['trackers'] = i[1]
                        req_seq, req, key_map = 1, [], {}

            if len(req) > 0:
                for i in self.request(req):
                    ndata[key_map[i[0]]]['trackers'] = i[1]

        self.save(ndata)


if __name__ == '__main__':
    Convert().fire(api, path)
