import shlex
import subprocess

import pytest
import requests


@pytest.fixture(scope="session")
def image():
    name = 'k'
    cmd = shlex.split('docker build -f Dockerfile.1.27 -t {} .'.format(name))
    subprocess.check_call(cmd)
    yield name


class TestContainer:
    @pytest.fixture(scope="class")
    def container(self, image):
        container_id = subprocess.check_output(
            shlex.split('docker run -d -p 8000:8000 {}'.format(image))
        ).rstrip(b'\n').decode('utf-8')
        yield container_id
        subprocess.check_call(shlex.split('docker rm -f {}'.format(container_id)))

    def test_healthz(self, container):
        resp = requests.get('http://localhost:8000/healthz')
        resp.raise_for_status()
        assert resp.text == 'OK'


class TestFUNCPORT:
    @pytest.fixture(scope="class")
    def container(self, image):
        funcport = '4242'
        cmd = shlex.split('docker run -d -e "FUNC_PORT={funcport}" -p 8000:{funcport} {image}'
            .format(funcport=funcport, image=image)
        )
        container_id = subprocess.check_output(cmd).rstrip(b'\n').decode('utf-8')
        yield container_id
        subprocess.check_call(shlex.split('docker rm -f {}'.format(container_id)))

    def test_healthz(self, container):
        resp = requests.get('http://localhost:8000/healthz')
        resp.raise_for_status()
        assert resp.text == 'OK'


# def test_failing_function():
#     pass

# def test_
if __name__ == '__main__':
    import sys
    pytest.main([__file__] + sys.argv[1:])
