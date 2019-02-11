# -*- coding: utf-8 -*-
from bottle import HTTPResponse
from bottle import post
from bottle import request
from bottle import route
from bottle import run
from bottle import static_file
from bottle import template
import base64
from datetime import datetime
import json
import os
import shutil
import subprocess
from subprocess import check_output
import sys

imgs = [".png", ".jpg", ".jpeg", ".pdf" ".eps"]


@route('/')
def index_html():
    return template("index")


@route('/static/<file_path:path>')
def static(file_path):
    return static_file(file_path,
                       root="./static")


@route('/static/tmp/<file_path:path>')
def pdf(file_path):
    return static_file(file_path,
                       root="./static/tmp")


def res_json(data):
    """
    body: dictionary
    """
    body = json.dumps(data)
    r = HTTPResponse(status=200, body=body)
    r.set_header('Content-Type', 'application/json')
    return r


def req_to_dict(request):
    """
    vueから送信されてくるデータを辞書にする
    """
    path_list = request.json["files"]
    path_dict = {}
    for item in path_list:
        path_dict.update(item)
    return path_dict


def save_img(file_name, content):
    content = content.split(',')[1]
    with open(file_name, 'wb') as f:
        f.write(base64.b64decode(content))


def save_txt(file_name, content):
    with open(file_name, 'w') as f:
        f.write(base64.b64decode(content).decode('utf-8'))


def savefile(dir_name, file_name, content):
    os.makedirs(dir_name, exist_ok=True)
    ext = os.path.splitext(file_name)[1]

    if ext in imgs:
        save_img(file_name, content)
    else:
        save_txt(file_name, content)


def download(path_dict, tmpdir):
    for k, v in path_dict.items():
        dir_name = tmpdir + os.path.split(k)[0]
        # テキスト・画像ファイルを保存
        file_name = tmpdir + k
        savefile(dir_name, file_name, v)


def make_work_dir():
    # 後で一気に消せるようにする
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    tmpdir = ''.join(["static/", now, '/'])
    os.makedirs(tmpdir, exist_ok=True)
    return tmpdir, now


def typeset(request):
    # カレントディレクトリを記録
    current = os.getcwd()
    work_dir, now = make_work_dir()
    path_dict = req_to_dict(request)
    # コンパイルスクリプトを動かすディレクトリ
    topdir = work_dir + list(path_dict.keys())[0].split('/')[0]
    # ファイルをサーバへ
    download(path_dict, work_dir)

    # コンパイルを行うディレクトリへ移動
    os.chdir(topdir)
    # shell=Trueで文字列で渡せる
    cmd = "grep documentclass -rl src/"
    target = check_output(cmd, shell=True).decode()[:-1]

    # \rを除去
    check_output('sed "s/\r//g" compile > compile_u', shell=True)

    ext = ".pdf"
    # コンパイルしてみる
    try:
        subprocess.check_call(["bash", "compile_u"])
    # 失敗したらlogを返す
    except subprocess.CalledProcessError:
        ext = ".log"
    except KeyboardInterrupt:
        pass
    finally:
        path = target.replace("src", "build")
        target = os.path.splitext(path)[0] + ext
        result = ''.join([topdir, "/", target])

    # 元のディレクトリ(app)へ戻る
    os.chdir(current)

    # 一時保存
    tmp = "./static/tmp/"
    os.makedirs(tmp, exist_ok=True)
    output = ''.join([tmp, now, os.path.split(result)[1]])
    shutil.copy(result, output)

    # ダウンロードしたものを消去
    shutil.rmtree(work_dir)

    return output


@post('/compile')
def compile():
    result = typeset(request)
    body = {"url": result}
    return res_json(body)


if __name__ == '__main__':
    run(host='0.0.0.0', port=5000, debug=True, reloader=True)
