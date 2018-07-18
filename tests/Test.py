import test


def test_analize():
        
    log_line = "/root/file1/production.log 2018-06-25T03:40:24 [I|app|cc8ef] Completed 200 OK in 75ms (Views: 5.0ms | ActiveRecord: 45.8ms"
    line = "2018-06-25T03:40:24 [I|app|cc8ef] Completed 200 OK in 75ms (Views: 5.0ms | ActiveRecord: 45.8ms"
    result = test.analize(log_line, line, 0)
    expected_result = "ID:cc8ef Time:03:40:24 Totaltime:75ms  Views:5.0ms ActiveRecord:45.8ms"
    assert result == expected_result


def test_trace():
    line = ["""2018-06-25T04:14:44 [W|app|2a090] some executors are not responding, check /foreman_tasks/dynflow/status
    /opt/theforeman/tfm/root/usr/share/gems/gems/katello-3.7.0.rc1/app/models/katello/ping.rb:75:in `block in ping_foreman_tasks'
    /opt/theforeman/tfm/root/usr/share/gems/gems/katello-3.7.0.rc1/app/models/katello/ping.rb:83:in `exception_watch'""",
    """2018-06-25T04:14:45 [I|app|dfe37] Current user: foreman_admin (administrator)""", 
    """2018-06-25T04:14:45 [I|app|] Current user: foreman_admin (administrator) """]
    trace_line = []
    for i in range(len(line)):
        result = test.trace(line[i], trace_line)
    expected_result = """2018-06-25T04:14:44 [W|app|2a090] some executors are not responding, check /foreman_tasks/dynflow/status
    /opt/theforeman/tfm/root/usr/share/gems/gems/katello-3.7.0.rc1/app/models/katello/ping.rb:75:in `block in ping_foreman_tasks'
    /opt/theforeman/tfm/root/usr/share/gems/gems/katello-3.7.0.rc1/app/models/katello/ping.rb:83:in `exception_watch'"""
    assert result == expected_result


def test_all():
    line = ["2018-06-25 04:14:00,607 [thread=http-bio-8443-exec-28] [req=a6cb4228-42bf-4fd1-95a2-a517e07fd736, org=, csid=7fb3adba] INFO  org.candlepin.common.filter.LoggingFilter - Request: verb=GET, uri=/candlepin/consumers/feac10ac-2d5b-4388-a754-9d45eb10178a""",
    """2018-06-25 04:14:00,610 [thread=http-bio-8443-exec-3] [req=4dceb09d-f7ae-4cbb-9be8-0a5777c72798, org=, csid=9e6f355a] INFO  org.candlepin.common.filter.LoggingFilter - Request: verb=GET, uri=/candlepin/consumers/3fb768c7-105b-4f7b-a1b6-0eb9076a58ab""",
    """2018-06-25 04:14:00,618 [thread=http-bio-8443-exec-27] [req=e8ac9438-dd37-4df4-bd06-9b4806134812, org=, csid=fd9e7eb4] INFO  org.candlepin.common.filter.LoggingFilter - Request: verb=GET, uri=/candlepin/consumers/6314d478-0514-424d-860c-306afa7463fb""",
    """2018-06-25 04:14:00,618 [thread=http-bio-8443-exec-35] [req=f16bd757-a7a1-4b1f-8a18-b8d525bb5c85, org=, csid=aaa03560] INFO  org.candlepin.common.filter.LoggingFilter - Request: verb=GET, uri=/candlepin/consumers/f1292608-ff88-4301-b0c8-e62815716a44""",
    """2018-06-25 04:14:00,621 [thread=http-bio-8443-exec-28] [req=a6cb4228-42bf-4fd1-95a2-a517e07fd736, org=Default_Organization, csid=7fb3adba] INFO  org.candlepin.common.filter.LoggingFilter - Response: status=200, content-type="application/json", time=13"""]
    data = {}
    for i in range(len(line)):
        result = test.all(line[i], data)
    expected_result = str(result).find("7fb3adba") != -1
    assert expected_result


def test_consumer():
    line = ["2018-06-25 04:14:00,607 [thread=http-bio-8443-exec-28] [req=a6cb4228-42bf-4fd1-95a2-a517e07fd736, org=, csid=7fb3adba] INFO  org.candlepin.common.filter.LoggingFilter - Request: verb=GET, uri=/candlepin/consumers/feac10ac-2d5b-4388-a754-9d45eb10178a""",
    """2018-06-25 04:14:00,610 [thread=http-bio-8443-exec-3] [req=4dceb09d-f7ae-4cbb-9be8-0a5777c72798, org=, csid=9e6f355a] INFO  org.candlepin.common.filter.LoggingFilter - Request: verb=GET, uri=/candlepin/consumers/3fb768c7-105b-4f7b-a1b6-0eb9076a58ab""",
    """2018-06-25 04:14:00,618 [thread=http-bio-8443-exec-27] [req=e8ac9438-dd37-4df4-bd06-9b4806134812, org=, csid=fd9e7eb4] INFO  org.candlepin.common.filter.LoggingFilter - Request: verb=GET, uri=/candlepin/consumers/6314d478-0514-424d-860c-306afa7463fb""",
    """2018-06-25 04:14:00,618 [thread=http-bio-8443-exec-35] [req=f16bd757-a7a1-4b1f-8a18-b8d525bb5c85, org=, csid=aaa03560] INFO  org.candlepin.common.filter.LoggingFilter - Request: verb=GET, uri=/candlepin/consumers/f1292608-ff88-4301-b0c8-e62815716a44""",
    """2018-06-25 04:14:00,621 [thread=http-bio-8443-exec-28] [req=a6cb4228-42bf-4fd1-95a2-a517e07fd736, org=Default_Organization, csid=7fb3adba] INFO  org.candlepin.common.filter.LoggingFilter - Response: status=200, content-type="application/json", time=13"""]
    data = {}
    id = "feac10ac-2d5b-4388-a754-9d45eb10178a"
    for i in range(len(line)):
        result = test.consumer(line[i], data, id)
    expected_result = str(result).find("7fb3adba") != -1
    assert expected_result
