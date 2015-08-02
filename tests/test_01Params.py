import pytest, coverage
import unittest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import protobix

class TestParams:

    @classmethod
    def setup_class(cls):
        cls.zbx_container = protobix.DataContainer()

    @classmethod
    def teardown_class(cls):
        cls.zbx_container = None

    def test_default_params(self):
        assert self.zbx_container.zbx_host == '127.0.0.1'
        assert self.zbx_container.zbx_port == 10051
        assert self.zbx_container.data_type == None
        assert self.zbx_container.log_level == 3
        assert self.zbx_container.dryrun == False
        assert self.zbx_container.items_list == []
        assert self.zbx_container._config == {
            'server': '127.0.0.1',
            'port': 10051,
            'log_level': 3,
            'log_output': '/tmp/zabbix_agentd.log',
            'dryrun': False,
            'data_type': None,
            'timeout': 3,
        }

    def test_custom_params(self):
        self.zbx_container = protobix.DataContainer(
                        data_type  = 'items',
                        zbx_file   = './test/zabbix_agentd.conf',
                        zbx_host   = 'localhost',
                        zbx_port   = 10052,
                        log_level  = 4,
                        dryrun     = True
        )
        assert self.zbx_container.zbx_host == 'localhost'
        assert self.zbx_container.zbx_port == 10052
        assert self.zbx_container.data_type == 'items'
        assert self.zbx_container.log_level == 4
        assert self.zbx_container.dryrun == True
        assert self.zbx_container._config == {
            'server': 'localhost',
            'port': 10052,
            'log_level': 4,
            'log_output': '/tmp/zabbix_agentd.log',
            'dryrun': True,
            'data_type': 'items',
            'timeout': 3,
        }
        assert self.zbx_container.items_list == []

    def test_data_type_param(self):
        for value in ['items', 'lld']:
            self.zbx_container.data_type = value
            assert self.zbx_container.data_type == \
                   self.zbx_container._config['data_type'] == value
        # Wrong value
        with pytest.raises(ValueError):
            self.zbx_container.data_type = 'bad'
        # Check value didn't change
        assert self.zbx_container.data_type == \
               self.zbx_container._config['data_type'] == 'lld'

    def test_zbx_host_param(self):
        self.zbx_container.zbx_host = 'localhost'
        assert self.zbx_container.zbx_host == \
               self.zbx_container._config['server'] == 'localhost'

    def test_zbx_port_param(self):
        self.zbx_container.zbx_port = 10052
        assert self.zbx_container.zbx_port == \
               self.zbx_container._config['port'] ==10052

    def test_log_level_param(self):
        for value in [0, 1, 2, 3, 4]:
            self.zbx_container.log_level = value
            assert self.zbx_container.log_level == \
                   self.zbx_container._config['log_level'] == value
        with pytest.raises(ValueError):
            self.zbx_container.log_level = 'bad'
        with pytest.raises(ValueError):
            self.zbx_container.log_level = 5

    def test_dryrun_param(self):
        self.zbx_container.dryrun = True
        assert self.zbx_container.dryrun == \
               self.zbx_container._config['dryrun'] == True
        with pytest.raises(ValueError):
            self.zbx_container.dryrun = 'bad'
        self.zbx_container.dryrun = False
        assert self.zbx_container.dryrun == \
               self.zbx_container._config['dryrun'] == False