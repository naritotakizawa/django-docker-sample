import os
import datetime
import subprocess

from django.conf import settings
from django.urls import reverse_lazy
from django.views import generic

from .forms import EditorForm

file_dir = os.path.join(settings.BASE_DIR, 'history')
docker_cmd = 'docker run -i --rm --name my-running-script -v {}:/usr/src/myapp -w /usr/src/myapp python:3.7 python {}'


def start_docker(code):
    """dockerコンテナ内でPythonコードを実行する."""
    # historyディレクトリ内に、2019-07-29T22:58:24.1111.py のようなファイルを作り、中身は入力したコード
    file_name = '{}.py'.format(datetime.datetime.now().isoformat())
    file_path = os.path.join(file_dir, file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(code)

    # historyディレクトリを、コンテナにマウントするよう設定し、python 2019-07-29T22:58:24.1111.py のように実行
    cmd = docker_cmd.format(file_dir, file_name)
    ret = subprocess.run(
        cmd, timeout=15, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    return ret.stdout.decode()


class Home(generic.FormView):
    """/へのアクセスで呼ばれるトップページのビュー."""
    template_name = 'app/home.html'
    form_class = EditorForm
    success_url = reverse_lazy('app:home')

    def form_valid(self, form):
        """送信ボタンでよびだされる."""
        code = form.cleaned_data['code']
        output = start_docker(code)
        context = self.get_context_data(form=form, output=output)
        return self.render_to_response(context)
